try:
    import ujson as json
except ImportError:
    import json

import uredis_modular.list


class MicroQueue(object):
    def __init__(self, name, host=None, port=6379, redis=None):
        self.__connection = redis
        if not host:
            host = '127.0.0.1'
        if not redis:
            if host:
                self.__connection = uredis_modular.list.List(host, port)
        self.name = name
        self.key_name = 'hotqueue:' + name

    def clear(self):
        """ Clear the Queue """
        # We send this directly with the client API so we don't waste memory
        # pulling in the entire Key command group.
        self.__connection.execute_command('DEL', self.key_name.encode())

    def consume(self, **kwargs):
        """
        A blocking generator that gets an item from the queue, blocking if the queue is empty

        Parameters
        ----------
        **kwargs
        """
        kwargs.setdefault('block', True)
        message = self.get(**kwargs)
        while message:
            yield message
            message = self.get(**kwargs)

    def get(self, block=False, timeout=0):
        """
        Get a message from the queue

        Parameters
        ----------
        bool : block
            If True, will block until a message is available.  default=False

        timeout : int
            When block is True, this specifies a timeout value for the maximum time it will block

        Returns
        -------
        object
            The deserialized object from the queue
        """
        if block:
            message = self.__connection.blpop(self.key_name, timeout=timeout)
            if message is not None:
                message = message[1]
        else:
            message = self.__connection.lpop(self.key_name)
        if message:
            message = json.loads(message.decode())
        return message

    def put(self, *messages):
        """
        Put one or more messages on the queue

        Parameters
        ----------
        *messages
            Messages to put on the queue
        """
        messages = [json.dumps(m) for m in messages]
        self.__connection.rpush(self.key_name, *messages)

    def worker(self, *args, **kwargs):
        def decorator(worker):
            def wrapper(*args):
                for msg in self.consume(**kwargs):
                    worker(*args + (msg,))
            return wrapper
        if args:
            return decorator(*args)
        return decorator
