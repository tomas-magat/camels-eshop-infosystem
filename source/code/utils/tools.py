import random
import threading
import time


# ID Generating

def random_id(type='N'):
    """
    Simplify generating random ids in format:
    [type]XXXXXXXXXX (type = 'N'/'P')
    """

    return type + str(random.randint(1000000000, 9999999999))


# Background periodical function calling

def run_periodically(function, delay=5):
    """
    Use threading and time.sleep() to run function
    with delay while not affecting the runtime of app.
    """

    background_thread = threading.Thread(
        target=lambda: callback(function, delay))
    background_thread.start()


def callback(function, delay):
    """Run function forever with delays between each run."""

    while True:
        function()
        time.sleep(delay)
