from utils import *


goods = read_file('tovar')
goods.append(['2121', 'hocico', 'hocico.jpg'])

if not is_locked('tovar'):
    lock_file('tovar')
    save_to_file('tovar', goods)
    unlock_file('tovar')
