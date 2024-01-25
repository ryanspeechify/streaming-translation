import logging
import colorlog
import sys


def initialize_logger(name, level=logging.WARNING):
    logger = logging.getLogger(name)
    # logger.propagate = False
    handler = colorlog.StreamHandler(stream=sys.stdout)
    formatter = colorlog.ColoredFormatter(
        "%(log_color)s[%(asctime)s][%(levelname)s][%(module)s]:%(reset)s %(message)s",
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger
