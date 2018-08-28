import json
import os
import sys
import uuid

from confluent_kafka_helpers.producer import AvroProducer


class InvalidJSON(Exception):
    pass


class Producer:
    DEFAULT_CONFIG = {}

    def __init__(self, producer=AvroProducer, **kwargs):
        self.broker = os.getenv('KAFKA_BROKER', kwargs['--broker'])
        self.registry = os.getenv('SCHEMA_REGISTRY_URL', kwargs['--registry'])
        self.topic = kwargs['--topic']
        self.key = kwargs['--key']
        self.value, self.stdin = kwargs['--value'], sys.stdin
        self.num_messages = int(kwargs['--num-messages'])
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

        for i in range(0, self.num_messages):
            key = self.key or str(uuid.uuid4())
            self.producer.produce(key=key, value=self.value, topic=self.topic)
            self.producer.poll(0)

        self.producer.flush()
