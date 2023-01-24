"""
Tests for the python-zabbix logging shim.

TODO
----
* Check to see if the logs are actually recorded by zabbix

Copyright
---------

Copyright © 2023 Sierra Anderson <sierrajwanderson@gmail.com>. 
This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://www.wtfpl.net/ or the LICENSE file for more details.
"""
# test with python `logging` module
import unittest

class TestSupport():
    def __init__(self) -> None:
        self.ip = "localhost"
        self.port = 22
        self.key = "key"
        self.username = "admin"
        self.password = "admin"
    
    def _setUpZabbix():
        pass

    def _cleanUpZabbix():
        pass

class TestZabbixLogging(unittest.TestCase):
    def setUp(self) -> None:
        # verify connection to zabbix 
        pass

    def test_logging(self):
        import logging
        from ZabbixHandler import ZabbixLoggingHandler

        ZabbixHandler = ZabbixLoggingHandler("localhost", 22, "key", "admin", "admin")
        ZabbixHandler.setLevel("ERROR")
        myLogger = logging.getLogger("myLogger")
        myLogger.addHandler(ZabbixHandler)

        myLogger.critical("Hello, Zabbix")


    # def test_other logging_libraries


if __name__ == "__main__":
    TestSupport()._setUpZabbix()
    unittest.main()
    TestSupport()._cleanUpZabbix()