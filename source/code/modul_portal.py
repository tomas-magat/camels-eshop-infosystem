from utils import *


goods = read_file('tovar')
version = get_version('tovar')


# Update 'goods' variable every 3 seconds
def update_goods():
    global goods, version
    
    current_version = get_version('tovar')

    if current_version != version:
        print('y')
        goods = read_file('tovar')
        version = current_version

run_periodically(update_goods, 3)
