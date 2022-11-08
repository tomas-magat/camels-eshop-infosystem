import os
import platform


rootpath = os.getcwd()

# Move to the root directory /camels-eshop-infosystem
if rootpath == 'code':
    os.chdir('..')
    os.chdir('..')
    PATH = rootpath
else:
    PATH = os.path.abspath('camels-eshop-infosystem')


SYSTEM = platform.system()
