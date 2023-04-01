from argparse import ArgumentParser
import logging
import signal

from config import Config
from src.pinger import Pinger
from src.plotter import Plotter
from src.logger import setup_logging

logger = logging.getLogger('ping-plot')

# Workaround to KeyboardInterrupt getting stuck in tkinter code
signal.signal(signal.SIGINT, signal.SIG_DFL)


def main():
    parser = ArgumentParser()
    parser.add_argument('--ip', '-i', default='192.168.0.1', help='IPv4 address to ping')
    parser.add_argument(
        '--log-level', '-l', default='ERROR',
        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
        help='Level for log filtering in python loggers'
    )
    args = parser.parse_args()

    setup_logging(args.log_level)

    pinger = Pinger(args.ip, Config.TIMEFRAME)
    plotter = Plotter(pinger.frame)

    logger.debug('Starting pinger thread...')
    pinger.start()

    logger.debug('Starting plotter...')
    plotter.plot()

    logger.debug(f'Setting stop flag for {pinger}')
    pinger.set_stop(True)


if __name__ == '__main__':
    main()
