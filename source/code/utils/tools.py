# Other often used functions
import random
import threading
import os
import difflib
import datetime

from PyQt5 import QtWidgets, QtGui

from .ENV_VARS import PATH
from .file import DataFile


def random_id(type='N'):
    """
    Generate id with type and 10 random digits:
    [type]XXXXXXXXXX (type = 'N'/'P')
    """

    sequence = [str(random.randint(0, 9)) for _ in range(10)]
    return type+''.join(sequence)


def now():
    """Get current date in a string format YYYY-MM-DD HH-mm-SS."""

    return datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")


def run_periodically(function, period=5.0):
    """
    Use threading.Timer to run function repeatedly
    with delay while not affecting the runtime of an app.
    """

    background_timer = threading.Timer(float(period), function)
    background_timer.start()
    return background_timer


def str_price(price: float, amount=1):
    """Return total price string - with 2 decimal places."""

    return "%.2f" % abs(price*amount)


def find_image(image_name: str):
    """Return absolute path of root/assets/images/[image_name]."""

    return os.path.join(PATH, "assets", "images", image_name)


def find_icon(icon_name: str):
    """Return absolute path of root/assets/icons/[icon_name]."""

    return os.path.join(PATH, "assets", "icons", icon_name)


def validate_int(input_field, invalid_cmd=None):
    """
    Return input text if it is integer 
    else run invalid_cmd() function.
    """

    if input_field.text().isdigit():
        return input_field.text()
    elif invalid_cmd != None:
        invalid_cmd()


def validate_price(input_field, invalid_cmd=None):
    """
    Return input text if it is valid price 
    format else run invalid_cmd() function.
    """

    try:
        price = float(input_field.text())
    except:
        if invalid_cmd != None:
            invalid_cmd()
    else:
        return "%.2f" % price


def search_items(query: str, data: dict, category=0):
    """
    Return items from data dictionary matching with search
    term (query) and of the given category (0 = all).
    """

    result = {}
    data = filter_category(data, category)

    for k, v in data.items():
        for term in query.split():
            match = get_match(term, k, v)
            if match:
                result[k] = v

    return result


def sort_items(sort_state, price_type='sell', category=0):
    """
    Return list of item codes sorted by prices
    according to sort_state. Change price_type to
    sort buy prices except of sell prices.
    """

    data = DataFile('cennik').data
    prices = filter_category(data, category)
    n = 1 if price_type == 'sell' else 0

    if sort_state == 1:
        return sorted(prices.keys())
    elif sort_state == 2:
        return sorted(prices,
                      key=lambda key: prices.get(key)[n],
                      reverse=True)
    else:
        return sorted(prices, key=lambda key: prices.get(key)[n])


def get_match(term, key, val):
    """
    Compare string similarity with items properties
    and return True or False if term does not match.
    """

    code = len(term)/6 if term.isdigit() else 0.2
    ratio = difflib.SequenceMatcher(
        None, term, key if term.isdigit() else val[0]).ratio()

    return ratio > 0.2+code


def filter_category(data, category):
    """
    Return dictionary contaning only items of specific 
    category (0 = all categories).
    """

    result = {}
    for k, v in data.items():
        if k[0] == str(category) or category == 0:
            result[k] = v

    return result


def camelify(input_string: str):
    """
    Make the input string camelCased so that 
    it is valid PyQt5 object name.
    """

    camel = input_string.title().replace(" ", "")
    return ''.join([camel[0].lower(), camel[1:]])


def receipt_template(id, cashier_name, contents, total_price):
    """
    Template for common receipt. Requires receipt id, cashier
    name, cart contents and total cart price parameters.
    """

    output = ['Camels E-shop s.r.o.',
              '\nCislo uctenky: '+id,
              '\nVytvorene dna: '+now(),
              '\nVystavil pokladnik: '+cashier_name,
              '\n\n===================================\n']
    output += [
        item.display_name+'\n\t'+str(item.amount)+'ks x ' +
        str_price(item.price)+'\t\t' +
        str_price(item.price, item.amount)+' €\n'
        for item in list(contents.values())
    ]
    output += ['\n==================================',
               '\nSpolu cena: '+str_price(total_price)+' €',
               '\nDPH(20%): '+str_price(total_price*0.2)+' €']

    return output
