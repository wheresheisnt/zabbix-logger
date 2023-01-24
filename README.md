Defines a `logging.Handler` child class used to send logs to a Zabbix server via the trapper functionality.

NB that to make use of this handler a Trapper-type item must be preconfigured on the Zabbix server. See
https://www.zabbix.com/documentation/current/en/manual/config/items/itemtypes/trapper.

The key entered will be used to initialise the handler so make sure to note it down.

**Installing**

PyPi/pip option coming soon, once I have a good CI/CD routine setup.

In the meantime, clone the repository & rip `ZabbixHandler.py` into your own codebase.


**Usage**
```
>>> import logging
>>> from zabbix-logger import ZabbixHandler

>>> ZabbixHandler = ZabbixHandler(ip, port, key, zabbix_username, zabbix_password)
... # the credentials used must belong to a user that is in the API Access group!
>>> ZabbixHandler.setLevel("ERROR")

>>> myLogger = logging.getLogger("myLogger")
>>> myLogger.addHandler(ZabbixHandler)
... # log things as per usual!
```

**License**

Copyright © 2023 Sierra Anderson <wheresheisnt@gmail.com>.

This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. 

See http://www.wtfpl.net/ or the LICENSE file for more details.