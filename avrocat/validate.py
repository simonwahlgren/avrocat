import json
import os

import fastavro
from confluent_kafka.schema_registry import SchemaRegistryClient
from fastavro.validation import validate


class Validate:
    def __init__(self, client=SchemaRegistryClient, **kwargs):
        self.registry = os.getenv('SCHEMA_REGISTRY_URL', kwargs['--registry'])
        self.topic = kwargs['--topic']
        self.file = kwargs['--file']
        with open(self.file) as file:
            self.value = json.load(file)

        self.client = client(conf={"url": self.registry})

    def validate(self):
        subject = f"{self.topic}-value"
        schema = self.client.get_latest_version(subject_name=subject)
        try:
            validate(self.value, json.loads(schema.schema.schema_str), raise_errors=True)
        except fastavro._validate_common.ValidationError as e:
            print(e)
            print("Fix errors from the bottom and up")
