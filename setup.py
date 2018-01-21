from setuptools import find_packages, setup

setup(
    name="avrocat",
    version="0.1",
    description="Kafka Avro consumer and producer",
    url="https://github.com/simonwahlgren/avrocat",
    author="Simon Wahlgren",
    author_email="simon.wahlgren@gmail.com",
    license="MIT",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "avrocat=avrocat.__main__:main"
        ]
    },
    install_requires=[
        "docopt>=0.6.2",
        "ujson>=1.35",
        "structlog==17.2.0",
        "confluent-kafka-helpers>=0.4.3"
    ],
    dependency_links=[
        "git+https://github.com/fyndiq/confluent_kafka_helpers@v0.4.3#egg=confluent-kafka-helpers-0.4.3"
    ],
    zip_safe=False
)
