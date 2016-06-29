import json


class MicroQueue(object):
    def __init__(self, name=None, host=None, port=6379, redis=None):
        self.__connection = redis
        if not name:
            name = 'defaultqueue'
        if not host:
            try:
                from bootconfig.config import get
                host = get('redis_server')
                if port==6379:
                    port = get('redis_port')
                del get
            except ImportError:
                pass
        if not redis:
            from uredis_modular.client import Client
            if host:
                self.__connection = Client(host, port)
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
            message = self.__connection.execute_command('BLPOP', self.key_name.encode(), timeout)
            if message is not None:
                message = message[1]
        else:
            message = self.__connection.execute_command('LPOP', self.key_name.encode())
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
        self.__connection.execute_command('RPUSH', self.key_name.encode(), *messages)

    def worker(self, *args, **kwargs):
        def decorator(worker):
            def wrapper(*args):
                for msg in self.consume(**kwargs):
                    worker(*args + (msg,))
            return wrapper
        if args:
            return decorator(*args)
        return decorator
