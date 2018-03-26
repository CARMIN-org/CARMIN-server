import os

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'brief': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'brief'
        },
        'request-context': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(log_dir, 'requests.log')
        },
        'unexpected-crash': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(log_dir, 'critical.log')
        }
        #  'email':
        #      'level': 'ERROR',
        #      'class': 'logging.handlers.SMTPHandler',
        #      'mailhost': 'localhost',
        #      'fromaddr': 'localhost@domain.com',
        #      'toaddrs': 'carmin@googlegroups.com',
        #      'subject': 'Server Error'
        #  }
    },
    'loggers': {
        'request-response': {
            'propagate': False,
            'handlers': ['request-context']
        },
        'server-error': {
            'propagata': False,
            'handlers': ['unexpected-crash']
        }
    }
}
