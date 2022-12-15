# This is the main file which imports all modules and
# after executing displays an App window

# TODO
# App - global file source

import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5 import uic

from utils.ui_commands import UI_Commands
from utils.file import DataFile
from utils.tools import update_data
from utils.ENV_VARS import PATH
from modules import *


class MainWindow:
    """
    Class containing the main window of the app.
    On initializing, set the landing page to index, 
    track home button clicks and initialize modules.
    Has a method .show() which displays this window.
    """

    def __init__(self):
        self.ui = uic.loadUi(
            os.path.join(PATH, 'source', 'code', 'main.ui'))

        self.commands = UI_Commands(self.ui)
        self.index()

        # Load data globally
        self.datafile_names = ['tovar', 'cennik', 'sklad', 'statistiky']
        self.data = {}
        for filename in self.datafile_names:
            self.data[filename] = DataFile(filename)

        # Initialize modules
        self.portal = modul_portal.Portal(self.ui, self.data)
        self.databaza = modul_databaza.Databaza(self.ui)
        self.statistika = modul_statistika.Statistika(self.ui)
        self.cenotvorba = modul_cenotvorba.Cenotvorba(self.ui)
        self.sklad = modul_sklad.Sklad(self.ui)

        # Track all home button clicks
        self.home_buttons = [
            self.ui.homeArrow,
            self.ui.homeArrow2,
            self.ui.homeArrow3,
            self.ui.homeArrow4,
            self.ui.homeArrow5,
        ]
        self.commands.buttons_click(self.home_buttons, self.index)

        update_data(list(self.data.values()), 5.0)

    def show(self):
        """Show the main App UI window."""
        self.ui.show()

    def index(self):
        self.commands.redirect(self.ui.index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
