import datetime
import logging
import os
import re
import signal
import threading
from typing import Any, Tuple, List
from subprocess import Popen, PIPE


ping_re = re.compile(r'.*time=(\d.*?).*')
timeout_re = re.compile(r'.*(Request timed out\.).*')


logger = logging.getLogger('ping-plot')


def get_time():
    return datetime.datetime.now()


class Buffer:
    """
    Series container with data rotation.
    Upon calling, it will return the containing list.
    Its `push` method will insert a new element, and it will also remove
    the first element if the list reaches its maximum size.

    :param size: Maximum size for the internal list.
    """
    def __init__(self, size: int):
        self.size = size
        self._lst = []

    def __call__(self):
        """
        :return: The internal list.
        """
        return self._lst

    def push(self, value: Any) -> None:
        """
        Add a new element to the internal list. If the list reaches its
        maximum size, also remove the first element to achieve data rotation,
        within the specified list size.

        :param value: Object to be added to the list
        """
        if len(self._lst) >= self.size:
            self._lst = self._lst[1:] + [value]
        else:
            self._lst.append(value)


class Frame:
    """
    Class that holds plot data along with the timestamps at which
    each sample was added. Uses `Buffer` for rotation. Is thread-safe.
    """
    def __init__(self, size):
        self.size = size
        self.x = Buffer(self.size)
        self.y = Buffer(self.size)
        self._lock = threading.Lock()

    def __call__(self) -> Tuple[List, List]:
        """
        :return: The lists contained by the two buffer attributes: `x` and `y`.
        """
        with self._lock:
            return self.x(), self.y()

    def add(self, val) -> None:
        """
        Add a value to the `y` Buffer and store the time of calling
        in the `x` Buffer. Print the added data.

        :param val:
        """
        t = get_time()

        with self._lock:
            self.x.push(t)
            self.y.push(val)

        if val is not None:
            print(f'{t.replace(microsecond=0)} - ping: {val} ms')


class Pinger(threading.Thread):
    def __init__(self, target: str, window: int):
        super().__init__()
        self._lock = threading.Lock()
        self.thread = threading.current_thread()
        self.target = target
        self.frame = Frame(window)
        self.stop = False

    def _get_stop(self):
        with self._lock:
            return self.stop

    def set_stop(self, stop):
        logger.debug(f'Setting stop flag in {self}')
        with self._lock:
            self.stop = stop
        logger.debug(f'Stop flag is now {self.stop}')

    def _ping_read(self, process) -> None:
        """
        Read lines from the stdout of a `Popen` process and look
        for the ping value using the `ping_re` regex. Should run
        in a separate thread. Loops until a `stop` attribute is
        set on its thread.
        """
        # Check stop condition
        while not self._get_stop():
            # Read line
            line = str(process.stdout.readline())
            if line != '' and not process.poll():
                # Check timeout
                timeout_match = timeout_re.match(line)
                if timeout_match:
                    print(timeout_match[1])
                    self.frame.add(None)
                else:
                    # Check if line contains ping value
                    ping_match = ping_re.match(line)
                    if ping_match is not None:
                        # Add ping value to frame
                        self.frame.add(int(ping_match[1]))

    def run(self) -> None:
        logger.debug(f'Starting ping subprocess to target {self.target}...')
        ping = Popen(['ping', self.target, '-t'], stdout=PIPE)

        logger.debug(f'Success - ping subprocess has PID {ping.pid}. Starting to read...')
        self._ping_read(ping)

        logger.debug(f'Stopped reading. Sending CTRL+C signal to {ping.pid}...')
        os.kill(ping.pid, signal.CTRL_C_EVENT)
