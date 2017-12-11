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
        "confluent-kafka-helpers>=0"
    ],
    dependency_links=[
        "git+https://github.com/fyndiq/confluent_kafka_helpers#egg=confluent-kafka-helpers-1"
    ],
    zip_safe=False
)
