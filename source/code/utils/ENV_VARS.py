import platform
from pathlib import Path

PATH = Path(__file__).parent.parent.parent.parent
DATAPATH = PATH.joinpath('source', 'data')
SYSTEM = platform.system()
