# Usage
The microqueue module creates queues that are stored in redis lists.  In
order to establish a queue you will need a running redis server.

If the redis server host and port are not specified and the bootconfig
module was used to configure the device with a redis_server and
redis_port, that redis server willl be used by default.

## Creating a queue worker on an esp8266

The queue.worker decorator runs the decorated function with the value 
from the queue passed as the argument to the function.

    MicroPython v1.8.1-87-g7ddd85f-dirty on 2016-06-27; ESP module with ESP8266
    Type "help()" for more information.
    >>> from microqueue import MicroQueue
    >>> queue = MicroQueue('queuename', host='192.168.1.183', port=6666)
    >>> 
    >>> @queue.worker
    ... def print_message(message):
    ...     print(message)
    ... 
    >>> print_message()
    Micropython Rocks!!!


## Writing to the queue

The resulting queue is compatible with the python 
redis-hotqueue/hotqueue modules available.  As long
as the json serializer is used (pickle is not supported on micropython)

    Python 2.7.11+ (default, Apr 17 2016, 14:00:29) 
    [GCC 5.3.1 20160413] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import json
    >>> from hotqueue import HotQueue
    >>> queue = HotQueue('queuename', host='192.168.1.183', port=6666, serializer=json)
    >>> queue.put('Micropython Rocks!!!')
    >>>
