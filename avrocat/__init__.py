from avrocat import log_config

log_config.setup()

from avrocat.consumer import Consumer  # isort: skip  # noqa
from avrocat.producer import Producer  # isort: skip  # noqa
from avrocat.validate import Validate  # isort: skip  # noqa


class AvroCat:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def consume(self):
        Consumer(**self.kwargs).consume()

    def produce(self):
        Producer(**self.kwargs).produce()

    def validate(self):
        Validate(**self.kwargs).validate()
