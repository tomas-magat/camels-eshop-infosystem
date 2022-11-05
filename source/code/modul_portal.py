from utils import *

from PyQt5.QtWidgets import QApplication, QWidget


goods = read_file('tovar')
version = get_version('tovar')

def update_goods():
    global goods, version
    
    current_version = get_version('tovar')

    if current_version != version:
        goods = read_file('tovar')
        version = current_version


# Update 'goods' variable every 3 seconds
run_periodically(update_goods, 3)
