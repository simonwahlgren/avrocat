from setuptools import find_packages, setup

setup(
    name="avrocat",
    version="0.3",
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
        "structlog>=17.2.0",
        "requests",
        "confluent_kafka_helpers>=0.6.1"
    ],
    zip_safe=False
)
