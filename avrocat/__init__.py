import pkg_resources

from avrocat.consumer import Consumer
from avrocat.producer import Producer

__version__ = pkg_resources.require("avrocat")[0].version


class AvroCat:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def consume(self):
        Consumer(**self.kwargs).consume()

    def produce(self):
        Producer(**self.kwargs).produce()
