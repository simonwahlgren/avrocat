import json
import os
import sys
import uuid
from time import sleep

from confluent_kafka_helpers.producer import AvroProducer

from avrocat.utils import format_extra_config, parse_headers


class Producer:
    DEFAULT_CONFIG = {}

    def __init__(self, producer=AvroProducer, **kwargs):
        self.broker = os.getenv("KAFKA_BROKERS", kwargs["--broker"])
        self.registry = os.getenv("SCHEMA_REGISTRY_URL", kwargs["--registry"])
        self.topic = kwargs["--topic"]
        self.key = kwargs["--key"]
        self.num_messages = int(kwargs["--num-messages"])
        self.per_second = int(kwargs.get("--per-second", 0) or 0)
        self.value, self.stdin = kwargs["--value"], sys.stdin
        self.file = kwargs["--file"]
        self.headers = parse_headers(kwargs.get("--header", []))
        if self.file:
            with open(self.file) as json_file:
                self.value = json_file.read()

        config = {
            "bootstrap.servers": self.broker,
            "schema.registry.url": self.registry,
            "topics": [self.topic],
            "linger.ms": 1000,
            **self.DEFAULT_CONFIG,
        }
        extra_config = format_extra_config(kwargs.get("--extra-config") or {})
        config = {**config, **extra_config}

        self.producer = producer(config)

    def produce(self):
        if not self.value and self.stdin.isatty():
            raise ValueError("You must pass a value using -v or std input")
        try:
            if self.value:
                self.value = json.loads(self.value)
            else:
                self.value = json.load(self.stdin)
        except ValueError:
            raise ValueError("Value is not valid JSON")

        for i in range(0, self.num_messages):
            key = self.key or str(uuid.uuid4())
            produce_kwargs = {
                "key": key,
                "value": self.value,
                "topic": self.topic,
                "headers": self.headers,
            }
            self.producer.produce(**produce_kwargs)
            self.producer.poll(0)
            if self.per_second:
                sleep(1 / self.per_second)

        self.producer.flush()
