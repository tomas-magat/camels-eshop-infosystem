import os
import platform


rootpath = os.getcwd()

# Move to the root directory /camels-eshop-infosystem
if rootpath == 'code':
    os.chdir('..')
    os.chdir('..')


PATH = os.path.abspath(rootpath)
SYSTEM = platform.system()
