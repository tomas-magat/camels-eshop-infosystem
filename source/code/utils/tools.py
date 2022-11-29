# Other often used functions
import random
import threading
import time
import os

from .ENV_VARS import PATH
from .ui_commands import UI_Commands
from .file import DataFile


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


def str_price(price: float, amount=1):
    """Return string of total price for given amount with EUR sign."""

    return ("%.2f" % (price*amount))+" €"


def find_image(image_name: str):
    """Return absolute path from root/assets/images/image_name."""

    return os.path.join(PATH, "assets", "images", image_name)


def find_icon(icon_name: str):
    """Return absolute path from root/assets/icons/image_name."""

    return os.path.join(PATH, "assets", "icons", icon_name)


def validate_int(field_input: str):
    """Return value if it is integer else display error message."""

    if field_input.isdigit():
        return field_input
    else:
        UI_Commands.error_message("Entered value must be an integer!")


def validate_price(field_input: str):
    """Return if input is valid price else display error message."""

    try:
        price = float(field_input)
    except:
        UI_Commands.error_message(
            "Entered value must be valid price!", additional_text="Please enter integer or float")
    else:
        return "%.2f" % price


def search_items(query: str):
    """Search items in TOVAR.txt matching with query."""

    tovar = DataFile('tovar')
    data = tovar.read()
    result = []

    for item in data:
        if query in (item[0] if query.isdigit() else item[1].lower()):
            result.append(item)

    return result
