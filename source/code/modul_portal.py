import threading
import time

from utils import *


goods = read_file('tovar')

# Continuous updating of 'goods' variable
def update_goods():
    global goods

    last_version = get_version('tovar')
    
    while True:
        time.sleep(3)
        current_version = get_version('tovar')

        if current_version != last_version:
            goods = read_file('tovar')
            last_version = current_version
        

goods_thread = threading.Thread(target=update_goods)
goods_thread.start()


goods.append(['2121', 'hocico', 'hocico.jpg'])

if not is_locked('tovar'):
    lock_file('tovar')
    save_to_file('tovar', goods)
    unlock_file('tovar')




    
