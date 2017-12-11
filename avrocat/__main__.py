"""
Kafka Avro producer and consumer.

Usage:
  avrocat produce -t <topic> [-v <value>] [-k <key>] [-b <broker>]
                             [-r <registry>]
  avrocat consume -t <topic> [--exit] [-g <group>]

Commands:
    produce                 Produce Avro message to a topic.
    consumer                Consume Avro messages from one or multiple topics.

Options:
  -t --topic=<topic>        One (P) or multiple (C) comma separated topics.
  -v --value=<value>        Message value (JSON).
  -k --key=<key>            Message key.
  -b --broker=<broker>      Kafka broker address [default: localhost:9092].
  -r --registry=<registry>  Schema registry URL [default: http://localhost:8081].
  -g --group=<group>        Consumer group.
  --exit                    Exit after last message is consumed.
"""
from docopt import docopt

from avrocat import AvroCat

arguments = docopt(__doc__)


def main():
    consume = arguments.pop('consume')
    produce = arguments.pop('produce')
    avrocat = AvroCat(**arguments)
    if consume:
        avrocat.consume()
    elif produce:
        avrocat.produce()


if __name__ == "__main__":
    main()
