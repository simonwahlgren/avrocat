import os
import uuid

import structlog
from confluent_kafka_helpers.loader import AvroMessageLoader
from confluent_kafka_helpers.producer import AvroProducer

from avrocat.utils import format_extra_config

logger = structlog.get_logger(__name__)


class Reproduce:
    def __init__(self, **kwargs):
        self._broker = os.getenv("KAFKA_BROKERS", kwargs["--broker"])
        self._registry = os.getenv("SCHEMA_REGISTRY_URL", kwargs["--registry"])
        self._topic = kwargs["--topic"]
        self._partition = int(kwargs["--partitions"])
        self._key = kwargs["--key"]
        self._offset = int(kwargs["--offset"])
        self._reproduce_topic = kwargs.get("--reproduce-topic") or self._topic

        extra_config = format_extra_config(kwargs.get("--extra-config") or {})

        # Consumer config for reading the specific message
        self.consumer_config = {
            "bootstrap.servers": self._broker,
            "schema.registry.url": self._registry,
            "topics": [self._topic],
            "group.id": f"avrocat-reproduce-{uuid.uuid4()}",
            "enable.auto.commit": False,
            "default.topic.config": {"auto.offset.reset": "earliest"},
            **extra_config,
        }

        # Producer config for reproducing the message
        self.producer_config = {
            "bootstrap.servers": self._broker,
            "schema.registry.url": self._registry,
            "topics": [self._reproduce_topic],
            "linger.ms": 1000,
            **extra_config,
        }

    def reproduce(self):
        """Reproduce a specific message from Kafka."""
        # First, read the specific message
        message = self._read_specific_message()

        if not message:
            logger.error(
                "Message not found",
                topic=self._topic,
                partition=self._partition,
                key=self._key,
                offset=self._offset,
            )
            return

        # Then produce it to the target topic
        self._produce_message(message)

        logger.info(
            "Message reproduced successfully",
            from_topic=self._topic,
            to_topic=self._reproduce_topic,
            key=self._key,
            offset=self._offset,
        )

    def _read_specific_message(self):
        """Read a specific message using the loader."""
        loader_config = {
            "bootstrap.servers": self._broker,
            "schema.registry.url": self._registry,
            "topic": self._topic,
            "num_partitions": self._partition + 1,  # Ensure we have enough partitions
            "consumer": {
                "bootstrap.servers": self._broker,
                "schema.registry.url": self._registry,
            },
        }

        loader = AvroMessageLoader(loader_config)

        # Find the specific message by key and offset
        for message in loader.load(self._key):
            if (
                message._meta.partition == self._partition
                and message._meta.offset == self._offset
            ):
                return message

        return None

    def _produce_message(self, message):
        """Produce the message to the target topic."""
        producer = AvroProducer(self.producer_config)

        # Use the original key and value from the message
        key = message._meta.key
        value = message.value

        producer.produce(key=key, value=value, topic=self._reproduce_topic)
        producer.poll(0)
        producer.flush()

