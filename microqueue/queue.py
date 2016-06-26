try:
    import ujson as json
except ImportError:
    import json


class MicroQueue(object):
    def __init__(self, name, connection):
        self.__connection = connection
        self.name = name
        self.key_name = 'microqueue:' + name

    def clear(self):
        """ Clear the Queue """
        self.__connection.delete(self.key_name)

    def consume(self, **kwargs):
        """
        A blocking generator that gets an item from the queue, blocking if the queue is empty

        Parameters
        ----------
        **kwargs
        """
        kwargs.setdefault('block', True)
        while True:
            message = self.get(**kwargs)
            if message is None:
                break
            yield message

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
            message = json.loads(message)
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
