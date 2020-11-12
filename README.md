## Avrocat

CLI tool for consuming and producing Avro messages from Kafka.

## Installation

    pip install -e .

## Usage

### Consume

#### Find all events with given key

    avrocat consume -t <topic> -b <broker> -r <schema_registry> --enable-timestamps -k <key> -P <num_partitions>

#### Load all events for a topic

    avrocat consume -t <topic> -b <broker> -r <schema_registry> --enable-timestamps

### Produce

    cat << EOF > CreateFoo.json
    {
        "class": "CreateFoo",
        "data": {
            "id": "",
            "foo": "foo"
        }
    }
    EOF
    UUID=$(uuidgen)

#### Produce a message using JSON input

    jq --arg uuid $UUID '.data.id=$uuid' CreateFoo.json | avrocat produce -t <topic> -n <num_messages> -k $UUID

#### Produce 10 events every second

    jq --arg uuid $UUID '.data.id=$uuid' CreateFoo.json | avrocat produce -t <topic> -n <num_messages> -k $UUID -s 10
