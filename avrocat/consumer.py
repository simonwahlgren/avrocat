import json
import os
import uuid

import structlog

from avrocat.utils import format_extra_config

from confluent_kafka_helpers.consumer import AvroConsumer
from confluent_kafka_helpers.loader import AvroMessageLoader

logger = structlog.get_logger(__name__)


class Consumer:
    def __init__(self, **kwargs):
        self._broker = os.getenv('KAFKA_BROKERS', kwargs['--broker'])
        self._registry = os.getenv('SCHEMA_REGISTRY_URL', kwargs['--registry'])
        self._topic = kwargs['--topic']
        self._num_partitions = kwargs['--partitions']
        self._group = kwargs['--group'] or str(uuid.uuid4())
        self._key = kwargs['--key']
        self._exit = kwargs['--exit']
        self._enable_timestamps = kwargs['--enable-timestamps']
        self._remove_null_values = kwargs['--remove-null-values']

        self.consumer_config = {
            'bootstrap.servers': self._broker,
            'schema.registry.url': self._registry,
            'topics': [self._topic],
            'group.id': self._group,
            'enable.auto.commit': True,
            'default.topic.config': {
                'auto.offset.reset': 'earliest'
            }
        }
        self.loader_config = {
            'bootstrap.servers': self._broker,
            'schema.registry.url': self._registry,
            'topic': self._topic,
            'num_partitions': self._num_partitions,
            'consumer': {
                'bootstrap.servers': self._broker,
                'schema.registry.url': self._registry
            }
        }
        self.extra_config = format_extra_config(kwargs.get('--extra-config') or {})

    def consume(self):
        if self._key:
            self.loader = AvroMessageLoader({**self.loader_config, **self.extra_config})
            for message in self.loader.load(self._key):
                data = {
                    'datetime': str(message._meta.datetime),
                    'partition': message._meta.partition,
                    'key': message._meta.key,
                    'value': message.value
                }
                print(json.dumps(data))
        else:
            self.consumer = AvroConsumer({**self.consumer_config, **self.extra_config})
            with self.consumer as consumer:
                for message in consumer:
                    data = {
                        'datetime': str(message._meta.datetime),
                        'partition': message._meta.partition,
                        'key': message._meta.key,
                        'value': message.value
                    }
                    print(json.dumps(data))
