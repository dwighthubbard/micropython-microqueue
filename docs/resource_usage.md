# Resource usage

The microqueue module tries to keep memory utilization to a minimum.

The module currently uses 2240 bytes to import and 4064 bytes to create 
a microqueue object on the ESP8266 port.

Which means the following code uses 6304 bytes:

    from microqueue import MicroQueue
    q=MicroQueue('repl')

The redis protocol is binary safe which means the returned data doesn't
have to be copied or processed before being returned.  As  a result the
queue worker just needs sufficient memory to create the object being
returned from the redis queue.  Which means the queue worker does not
require a significant amount of resouces while in use.

Here is an example function to show the memory free and a queue worker
that displays the message returned and the amount of free memory:

    >>> def free():
    ...     gc.collect()
    ...     return gc.mem_free()
    ... 
    >>> free()
    14224
    >>> @q.worker
    ... def print_free(message):
    ...     print("Received", message)
    ...     print(free())
    ... 
    >>> print_free()
    Received hello
    13664
    Received hello
    13632
    Received hello
    13632
    Received hello
    13632
    Received hello
    13632
