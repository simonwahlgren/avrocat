import uuid
import structlog

from confluent_kafka_helpers.loader import AvroMessageLoader
from confluent_kafka_helpers.consumer import AvroConsumer

logger = structlog.get_logger(__name__)


class Consumer:
    def __init__(self, **kwargs):
        self._broker = kwargs['--broker']
        self._registry = kwargs['--registry']
        self._topic = kwargs['--topic']
        self._num_partitions = kwargs['--partitions']
        self._group = kwargs.get('group', str(uuid.uuid4()))
        self._key = kwargs['--key']
        self._exit = kwargs['--exit']
        self._enable_timestamps = kwargs['--enable-timestamps']

        self.consumer_config = {
            'bootstrap.servers': self._broker,
            'schema.registry.url': self._registry,
            'topics': [self._topic],
            # 'stop_on_eof': True,
            # 'poll_timeout': 0.1,
            'group.id': self._group,
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
                'schema.registry.url': self._registry,
            }
        }

    def consume(self):
        if self._key:
            self.loader = AvroMessageLoader(self.loader_config)
            for message in self.loader.load(self._key):
                if self._enable_timestamps:
                    print(f"{message._meta.datetime} {message.value}")
                else:
                    print(f"{message.value}")
        else:
            self.consumer = AvroConsumer(self.consumer_config)
            with self.consumer as consumer:
                for message in consumer:
                    if self._enable_timestamps:
                        print(f"{message._meta.datetime} {message._meta.partition}:{message._meta.key}:{message.value}")
                    else:
                        print(f"{message._meta.partition}:{message._meta.key}:{message.value}")
