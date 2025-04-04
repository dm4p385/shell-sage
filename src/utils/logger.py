import logging


def setup_logger(name="shellsage", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # Avoid duplicated logs

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(level)

        formatter = logging.Formatter("[*] [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
