import logging


def create_logger_factory(class_name,):
    logger = logging.getLogger(class_name)
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter for console handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to console handler
    ch.setFormatter(formatter)
    # create file handler and set level to warn
    fh = logging.FileHandler('spam.log')
    fh.setLevel(logging.WARN)
    # create formatter for file handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(userid)s - %(message)s')

    # add formatter to file handler
    fh.setFormatter(formatter)

    # add ch、fh to logger
    logger.addHandler(ch)
    logger.addHandler(fh)