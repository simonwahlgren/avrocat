## Avrocat
CLI tool for consuming and producing Avro messages from Kafka.

## Installation
```sh
pip install -e .
```

## Usage
#### Find all events with given key
```sh
avrocat consume -t <topic> -b <broker> -r <schema_registry> --enable-timestamps -k <key> -P <num_partitions>
```
#### Load all events for a topic
```sh
avrocat consume -t <topic> -b <broker> -r <schema_registry> --enable-timestamps
```
#### Produce a message using JSON input
```sh
UUID="${2:-$(uuidgen)}"
jq --arg uuid $UUID '.data.id=$uuid' CreateFoo.json | avrocat produce -t <topic> -n <num_messages> -k $UUID
```
```json
{
    "class": "CreateFoo",
    "data": {
        "id": "",
        "foo": "foo"
    }
}
```
