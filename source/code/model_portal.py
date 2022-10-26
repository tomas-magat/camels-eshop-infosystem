from utils import *


goods = read_file('tovar')
id = random_id('N')

unlock_file('TOVAR.txt')
if is_locked('TOVAR'):
    print(goods, id)