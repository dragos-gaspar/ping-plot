import logging
import signal
from argparse import ArgumentParser

from config import Config
from src.logger import setup_logging
from src.pinger import Pinger
from src.plotter import Plotter


logger = logging.getLogger('ping-plot')

# Workaround to KeyboardInterrupt getting stuck in tkinter code
signal.signal(signal.SIGINT, signal.SIG_DFL)


def main():
    parser = ArgumentParser()
    parser.add_argument('ip', default='192.168.0.1', help='IPv4 address to ping')
    parser.add_argument('--frame-size', '-n', help='Maximum number of data points. Overrides FRAME_SIZE in config.py')
    parser.add_argument(
        '--log-level', '-l', default='ERROR',
        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
        help='Level for log filtering in python loggers'
    )
    args = parser.parse_args()

    if args.frame_size:
        Config.FRAME_SIZE = args.frame_size

    setup_logging(args.log_level)

    pinger = Pinger(args.ip, Config.FRAME_SIZE)
    plotter = Plotter(pinger.frame)

    logger.debug('Starting pinger thread...')
    pinger.start()

    logger.debug('Starting plotter...')
    plotter.plot()

    logger.debug(f'Setting stop flag for {pinger}')
    pinger.set_stop(True)


if __name__ == '__main__':
    main()
