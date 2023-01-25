"""
Defines a `logging.Handler` child class used to send logs
to a Zabbix server via the trapper functionality.
NB that to make use of this handler a Trapper-type item 
must be preconfigured on the Zabbix server. See
https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/trapper
The key entered will be used to initialise the handler so make sure to note it down.


Usage
-----
>>> import logging
>>> from ZabbixHandler import ZabbixHandler

>>> ZabbixHandler = ZabbixHandler(ip, port, key, zabbix_username, zabbix_password)
... # the credentials used must belong to a user that is in the API Access group!
>>> ZabbixHandler.setLevel("ERROR")

>>> myLogger = logging.getLogger("myLogger")
>>> myLogger.addHandler(ZabbixHandler)
... # log things as per usual!

Copyright
---------

Copyright © 2023 Sierra Anderson <wheresheisnt@gmail.com>. 
This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://www.wtfpl.net/ or the LICENSE file for more details.

"""

# TODO handle type hinting etc in older versions of python
from logging import Handler, LogRecord
from http.client import HTTPConnection
from struct import pack
import json

class ZabbixHandler(Handler):
    """
    A class that sends records to a Zabbix server
    
    Only the `__init__()` method is designed to be used in
    other code. All other functions should not be called by
    user code.

    """
    def __init__(self, ip: str, port: int, key: str, zabbix_username: str, zabbix_password: str) -> None:
        Handler.__init__(self)
        self.z_ip = ip
        self.z_port = port
        self.z_username = zabbix_username
        self.z_password = zabbix_password
        self.z_auth_key = None
        self.key = key
        try:
            self.connection = HTTPConnection(self.z_ip, self.z_port, 60)
            self._login()
        except:
            self.handleError()

    def _login(self) -> None:
        data = json.dumps({"jsonrpc": "2.0", "method": "user.login",  "params": {"username": self.z_username, "password": self.z_password}, "id": 1})
        packet = b"ZBXD\1" + pack("<II", len(data), 0) + data.encode('utf-8')
        self.connection.request("PUT", "/", packet)
        response = self.connection.getresponse()
        self.z_auth_key = response.read()["result"]
        assert len(self.z_auth_key) != 0, "Login unsucessful"

    def _logout(self) -> None:
        data = json.dumps({"jsonrpc": "2.0", "method": "user.logout", "params": [], "id": 1, "auth": self.z_auth_key})
        packet = b"ZBXD\1" + pack("<II", len(data), 0) + data.encode('utf-8')
        self.connection.request("PUT", "/", packet)
        response = self.connection.getresponse()
        returnedData = json.load(response.read())
        assert returnedData["result"] == True, "Logout unsucessful."

    def _mapLogRecord(self, record: LogRecord) -> dict:
        return record.__dict__

    def emit(self, record: LogRecord) -> None:
        """
        Send `record` to the Zabbix server.
        """
        self.acquire()
        try:
            # send log to Zabbix server
            """<hostname> test value record.?"""
            self._login()
            data = json.dumps({"request":"sender data","data":[{"host":record.pathname, "key":self.key, "value":record.getMessage()}]})
            packet = b"ZBXD\1" + pack("<II", len(data), 0) + data.encode('utf-8')
            self.connection.request("PUT", "/", packet)
            response = self.connection.getresponse()
            response.read() # free up the buffer for future use
            self._logout() # don't leave a large number of open connections to the server

        except Exception as e:
            raise e("Zabbix log handler unable to send log entry to server")

        finally:
            self.release()

    def flush(self) -> None:
        """
        the `flush()` method is required to be implemented but we
        don't buffer logs before they are sent, so we can just pass
        """
        pass

    def close(self) -> None:
        """
        Tidy up any resources used by the handler.
        """
        # close & clean up connection to Zabbix server
        self._logout()
        super().close()


def main():
    import logging
    from ZabbixHandler import ZabbixHandler
    try:
        ZabbixHandler = ZabbixHandler("localhost", 1, "1", "1234", "1234")
        # the credentials used must belong to a user that is in the API Access group!
        ZabbixHandler.setLevel("ERROR")
        myLogger = logging.getLogger("myLogger")
        myLogger.addHandler(ZabbixHandler)
    except:
        raise

if __name__ == "__main__":
    main()