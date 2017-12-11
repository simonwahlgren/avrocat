class Consumer:
    def __init__(self, **kwargs):
        self._broker = kwargs['broker']
        self._registry = kwargs['registry']
        self._topic = kwargs['--topic']
        self._exit = kwargs['--exit']

    def consume(self):
        pass
