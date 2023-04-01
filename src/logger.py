import sys
import logging
from typing import Union, AnyStr


def setup_logging(level: Union[int, AnyStr] = 'WARNING') -> None:
    formatter = logging.Formatter('%(levelname)s | [%(threadName)s] %(filename)s :: %(funcName)s | %(message)s')
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger = logging.getLogger('ping-plot')
    logger.addHandler(handler)
    logger.setLevel(level)
