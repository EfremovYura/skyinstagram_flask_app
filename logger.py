import logging
from config import LOG_FILE_PATH, LOG_FORMAT


def log_config():
    api_logger = logging.getLogger('api_logger')
    api_logger.setLevel(logging.DEBUG)

    api_logger_handler = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
    api_logger_handler.setLevel(logging.DEBUG)
    api_logger.addHandler(api_logger_handler)

    api_logger_format = logging.Formatter(LOG_FORMAT)
    api_logger_handler.setFormatter(api_logger_format)
