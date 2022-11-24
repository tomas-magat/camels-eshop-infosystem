# Other often used functions
import random
import threading
import time
import os

from .ENV_VARS import PATH


def random_id(type='N'):
    """
    Generate id with type and 10 random digits:
    [type]XXXXXXXXXX (type = 'N'/'P')
    """

    sequence = [str(random.randint(0, 9)) for _ in range(10)]
    return type+''.join(sequence)


def run_periodically(function, period=5):
    """
    Use threading and time.sleep() to run function
    with delay while not affecting the runtime of an app.
    """

    background_thread = threading.Thread(
        target=lambda: callback(function, period))
    background_thread.start()


def callback(function, delay):
    """Run function forever with delays between each run."""

    while True:
        function()
        time.sleep(delay)


def str_price(price: float, amount: int):
    """Return string of total price for given amount with EUR sign."""

    return ("%.2f" % abs(price*amount))+" €"


def find_image(image_name: str):
    """Return absolute path from root/assets/image_name."""

    return os.path.join(PATH, "assets", "images", image_name)
