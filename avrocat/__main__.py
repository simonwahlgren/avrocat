"""
Kafka Avro producer and consumer.

Usage:
  avrocat produce -t <topic> [-v <value>] [-k <key>] [-b <broker>]
                             [-r <registry>] [-n <num_messages>]
  avrocat consume -t <topic> [--exit] [-g <group>] [-b <broker>] [-r <registry]
                             [(-P <partitions> -k <key>)]
                             [--enable-timestamps]

Commands:
    produce                             Produce Avro message to a topic.
    consumer                            Consume Avro messages from one or multiple topics.

Options:
  -t --topic=<topic>                    One (P) or multiple (C) comma separated topics.
  -v --value=<value>                    Message value (JSON).
  -k --key=<key>                        Message key.
  -n --num-messages=<num_messages>      Number of messages to produce [default: 1].
  -b --broker=<broker>                  Kafka broker address [default: localhost:9094].
  -r --registry=<registry>              Schema registry URL [default: http://localhost:8081].
  -g --group=<group>                    Consumer group.
  -P --partitions=<partitions>          Number of partitions on topic. Must be set when using --key
                                        [default: 8].
  --enable-timestamps                   Display message timestamps [default: False].
  --exit                                Exit after last message is consumed.
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
