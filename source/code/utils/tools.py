# Other often used functions
import random
import threading
import time


def random_id(type='N'):
    """
    Generate id with type and 10 random digits:
    [type]XXXXXXXXXX (type = 'N'/'P')
    """

    sequence = [str(random.randint(0, 9)) for _ in range(10)]
    return type+''.join(sequence)


def run_periodically(function, delay=5):
    """
    Use threading and time.sleep() to run function
    with delay while not affecting the runtime of an app.
    """

    background_thread = threading.Thread(
        target=lambda: callback(function, delay))
    background_thread.start()


def callback(function, delay):
    """Run function forever with delays between each run."""

    while True:
        function()
        time.sleep(delay)
