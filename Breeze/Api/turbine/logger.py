import logging
from io import StringIO


class StepLogger:
    def __init__(self, name: str):
        stream = StringIO()
        formatter = logging.Formatter('%(asctime)s - %(levelname)-8s: %(message)s', datefmt='%H:%M:%S')

        handler = logging.StreamHandler()
        handler.setStream(stream)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.addHandler(handler)

        self.logger = logger
        self.stream = stream

    def info(self, msg: str):
        self.logger.info(msg)

    def debug(self, msg: str):
        self.logger.debug(msg)

    def warning(self, msg: str):
        self.logger.warning(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def critical(self, msg: str):
        self.logger.critical(msg)
