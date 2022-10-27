import os
import platform

rootpath = os.getcwd()
if rootpath == 'code':
    os.chdir('..')
    os.chdir('..')


PATH = os.path.abspath(rootpath)
SYSTEM = platform.system()
