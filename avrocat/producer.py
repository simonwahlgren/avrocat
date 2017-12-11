import sys

import ujson as json

from confluent_kafka_helpers.producer import AvroProducer


class InvalidJSON(Exception):
    pass


class Producer:
    DEFAULT_CONFIG = {}

    def __init__(self, producer=AvroProducer, **kwargs):
        self.broker = kwargs['--broker']
        self.registry = kwargs['--registry']
        self.topic = kwargs['--topic']
        self.key = kwargs['--key']
        self.value, self.stdin = kwargs['--value'], sys.stdin
        self.config = {
            'bootstrap.servers': self.broker,
            'schema.registry.url': self.registry,
            'topics': [self.topic],
            **self.DEFAULT_CONFIG
        }
        self.producer = producer(self.config)

    def produce(self):
        if not self.value and self.stdin.isatty():
            raise RuntimeError("You must pass a value using -v or std input")
        try:
            if self.value:
                self.value = json.loads(self.value)
            else:
                self.value = json.load(self.stdin)
        except ValueError:
            raise InvalidJSON("Value is not valid JSON")

        self.producer.produce(key=self.key, value=self.value, topic=self.topic)
        self.producer.poll(0)
        self.producer.flush()
