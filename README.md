# Avrocat

CLI tool for consuming and producing Avro messages from Kafka.

## Installation

    pip install -e .

## Usage

### Consume all messages

    avrocat consume -t <topic> -b <broker> -r <schema_registry>

### Consume messages with given key

    avrocat consume -t <topic> -b <broker> -r <schema_registry> -k <key> -P <num_partitions>

### Produce message

    cat << EOF > CreateFoo.json
    {
        "class": "CreateFoo",
        "data": {
            "id": "12345",
            "foo": "foo"
        }
    }
    EOF

    cat CreateFoo.json | avrocat produce -t <topic> -n <num_messages>

### Validate JSON against schema

    avrocat validate -t <topic> -f CreateFoo.json
