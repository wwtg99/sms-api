from logging.config import dictConfig


def config_logger(enable_console_handler=True, enable_file_handler=True, log_file='app.log', log_level='ERROR',
                  log_file_max_bytes=5000000, log_file_max_count=5):
    console_handler = {
        'class': 'logging.StreamHandler',
        'formatter': 'default',
        'level': log_level,
        'stream': 'ext://flask.logging.wsgi_errors_stream'
    }
    file_handler = {
        'class': 'logging.handlers.RotatingFileHandler',
        'formatter': 'detail',
        'filename': log_file,
        'level': log_level,
        'maxBytes': log_file_max_bytes,
        'backupCount': log_file_max_count
    }
    default_formatter = {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    }
    detail_formatter = {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    }
    handlers = []
    if enable_console_handler:
        handlers.append('console')
    if enable_file_handler:
        handlers.append('file')
    d = {
        'version': 1,
        'formatters': {
            'default': default_formatter,
            'detail': detail_formatter
        },
        'handlers': {
            'console': console_handler,
            'file': file_handler
        },
        'root': {
            'level': log_level,
            'handlers': handlers
        }
    }
    dictConfig(d)
