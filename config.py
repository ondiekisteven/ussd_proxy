import logging.config
import os

LOGGING_CONFIG = None
LOGLEVEL = os.getenv('LOGGING_LEVEL', 'info').upper()
BASE_DIR = os.path.dirname(__file__)

if not os.path.exists(os.path.join(BASE_DIR, 'logs')):
    os.mkdir(os.path.join(BASE_DIR, 'logs'))


def configure_logger(log_file_name):
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,  # bool(int(os.getenv('DISABLE_EXISTING_LOGGERS', '1'))),
        'formatters': {
            'console': {
                "format": "%(asctime)s\t%(levelname)s\t%(filename)s\t%(message)s"
            },
            'tiny': {
                "format": "%(levelname)s\t- %(message)s"
            },
            "standard": {
                "class": "logging.Formatter",
                'format': '%(asctime)s\t%(levelname)s\t[%(name)s:%(lineno)s]\t%(message)s',
                "datefmt": "%d %b %y %H:%M:%S"
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'tiny',
                "level": "INFO",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "standard",
                "level": "INFO",
                "filename": os.path.join(BASE_DIR, f'logs/{log_file_name}.log'),
                "mode": "a",
                "encoding": "utf-8",
                "maxBytes": 5000000,
                "backupCount": 100
            },
            "timed": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "standard",
                "level": "INFO",
                "filename": os.path.join(BASE_DIR, f'logs/{log_file_name}.log'),
                "when": "midnight",
                "interval": 1,
                "backupCount": 100
            }
        },

        'loggers': {
            '': {
                'level': LOGLEVEL,
                'handlers': ['timed', 'console'] if os.getenv('USE_TIMED_LOGS', 1) else ['file', 'console'],
            },
        },
    })
