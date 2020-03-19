import logging
import logging.config
import os

import structlog

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_VERBOSITY_LEVEL = int(os.getenv('LOG_VERBOSITY_LEVEL', '0'))


def setup():
    timestamper = structlog.processors.TimeStamper(
        fmt="%Y-%m-%d %H:%M:%S", utc=False
    )
    pre_chain = [
        structlog.stdlib.add_log_level,
        timestamper,
    ]

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'dev': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.dev.ConsoleRenderer(colors=True),
                'foreign_pre_chain': pre_chain,
            }
        },
        'handlers': {
            'console': {
                'level': LOG_LEVEL,
                'class': 'logging.StreamHandler',
                'formatter': 'dev'
            }
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False
            },
            'confluent_kafka_helpers': {
                'handlers': ['console'],
                'level': 'DEBUG' if LOG_VERBOSITY_LEVEL >= 1 else 'WARNING',
                'propagate': False,
            },
            'datadog': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False,
            }
        }
    })
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            timestamper,
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
