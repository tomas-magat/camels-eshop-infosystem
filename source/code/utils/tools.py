# Other often used functions
import random
import os
import re
import difflib
import io
from datetime import datetime
from PIL import Image, ImageCms

from .ENV_VARS import PATH, IMGPATH
from .file import DataFile


def camelify(input_string: str):
    """
    Make the input string camelCased so that 
    it is valid PyQt5 object name.
    """

    camel = input_string.title().replace(' ', '')
    return ''.join([camel[0].lower(), camel[1:]])


def change_img_profile(icc, img):
    """
    Change PIL image profile from icc to sRGB color space 
    (if possible) to prevent problems in UI image displaying.
    """

    io_handle = io.BytesIO(icc)
    src_profile = ImageCms.ImageCmsProfile(io_handle)
    dst_profile = ImageCms.createProfile('sRGB')

    img_conv = ImageCms.profileToProfile(img, src_profile, dst_profile)
    icc_conv = img_conv.info.get('icc_profile', '')
    return icc_conv, img_conv


def filter_category(data: dict, category: int = 0):
    """
    Return dictionary contaning only items of specific 
    category (0 = all categories).
    """

    result = {}
    for k, v in data.items():
        if k[0] == str(category) or category == 0 or category > 5:
            result[k] = v

    return result


def filter_statistics_category(data_list: list, category: int = 0):
    """
    Return list contaning only purchases of items of specific 
    category (0 = all categories).
    """

    if category != 0:
        result = []
        for purchase in data_list:
            if purchase[3][0] == str(category):
                result.append(purchase)
        return result

    return data_list


def find_image(image_name: str):
    """Return absolute path of root/assets/images/[image_name]."""

    if IMGPATH == '':
        return os.path.join(PATH, 'assets', 'images', image_name)
    else:
        return os.path.join(IMGPATH, image_name)


def find_icon(icon_name: str):
    """Return absolute path of root/assets/icons/[icon_name]."""

    return os.path.join(PATH, 'assets', 'icons', icon_name)


def find_code(category):
    """Finds the first free item code of specific category."""

    data = DataFile('tovar').data
    codes = filter_category(data, category)
    int_codes = [int(code) for code in codes.keys()]

    if len(int_codes) < 1:
        int_codes.append(int(str(category)+'000'))

    return str(max(int_codes)+1)


def get_match(term, key, val):
    """
    Compare string similarity with items properties
    and return True or False if term does not match.
    """

    code = len(term)/6 if term.isdigit() else 0.4

    if term.isdigit():
        ratio = difflib.SequenceMatcher(None, term, key).ratio()
    else:
        ratios = []
        for name_part in val[0].split():
            rat = difflib.SequenceMatcher(None, term, name_part).ratio()
            ratios.append(rat)
        ratio = max(ratios)

    return ratio > 0.2+code


def now():
    """Get current date in a string format YYYY-MM-DD HH-mm-SS."""

    return datetime.now().strftime('%Y-%m-%d %H-%M-%S')


def random_id(type='N'):
    """
    Generate id with type and 10 random digits:
    [type]XXXXXXXXXX (type = 'N'/'P')
    """

    sequence = [str(random.randint(0, 9)) for _ in range(10)]
    return type+''.join(sequence)


def receipt_template(
    id: str, contents: dict, total_price: float, cashier_name: str = ''
):
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
    output += ['\n===================================',
               '\nSpolu cena: '+str_price(total_price)+' €',
               '\nDPH(20%): '+str_price(total_price*0.2)+' €']

    return output


def str_price(price: float, amount: int = 1):
    """Return total price string - with 2 decimal places."""

    return '%.2f' % abs(price*amount)


def search_items(query: str, data: dict, category: int = 0):
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


def sort_items(
    sort_state: int, price_type: str = 'sell', category: int = 0
):
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
                      key=lambda key: float(prices.get(key)[n]),
                      reverse=True)
    else:
        return sorted(prices, key=lambda key: float(prices.get(key)[n]))


def sort_counts(category: int = 0):
    """
    Return list of item codes sorted by prices
    according to sort_state. Change price_type to
    sort buy prices except of sell prices.
    """

    data = DataFile('sklad').data
    counts = filter_category(data, category)

    return sorted(
        counts, key=lambda key: int(counts.get(key)[0])
    )


def validate_int(input_field, invalid_cmd=None):
    """
    Return input text if it is integer 
    else run invalid_cmd() function.
    """

    if input_field.text().isdigit():
        return input_field.text()
    elif invalid_cmd != None:
        invalid_cmd()


def convert_price(input_field):
    """
    Return input text if it is valid price format.
    """

    try:
        text = re.sub(',|;', '.', input_field.text())
        price = float(text)
    except:
        if '-' in input_field.text():
            return '----'

    return '%.2f' % price


def valid_image(file_path):
    """
    If image on file_path is not a valid icc profile
    convert it to PNG format in lower quality.
    """
    try:
        img = Image.open(file_path)
        icc = img.info.get('icc_profile', '')
    except:
        return False
    else:
        if icc:
            icc_conv, img_conv = change_img_profile(icc, img)
            if icc != icc_conv:
                img_conv.save(
                    file_path, format='PNG',
                    quality=50, icc_profile=icc_conv
                )
        return True
