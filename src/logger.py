import os   # noqa

from loguru import logger as log


os.environ[
    "LOGURU_FORMAT"
] = "{time:DD.MM.YY HH:mm:ss} [<lvl>{level:^10}</lvl>] <lvl>{message}</lvl>"  # noqa
os.environ["LEVEL"] = "DEBUG"  # noqa


class Logger:
    logger: log

    def __init__(self):
        self.logger = log

        self.debug = log.debug
        self.info = log.info
        self.warning = log.warning
        self.error = log.error
        self.success = log.success


logger = Logger()