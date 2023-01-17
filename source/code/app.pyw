# This is the main file which imports all modules and
# after executing displays an App window

# TODO
# refactor ui_commands.date_range

import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5 import uic
from PyQt5.QtCore import QThread

from utils.ui_commands import UI_Commands, Timer
from utils.file import DataFile
from utils.ENV_VARS import PATH
from modules import *


class MainWindow:
    """
    Class initializing the main window of the app.
    On load, set the landing page to home, load datafiles,
    track home button clicks and initialize modules.
    Updates data periodically to keep it up-to-date.
    Has a method .show() which displays this window.
    """

    def __init__(self):
        self.ui = uic.loadUi(
            os.path.join(PATH, 'source', 'code', 'main.ui')
        )
        self.commands = UI_Commands(self.ui)
        self.home()
        self.load_data()

        # Initialize modules
        self.portal = modul_portal.Portal(self)
        self.databaza = modul_databaza.Databaza(self)
        self.statistika = modul_statistika.Statistika(self)
        self.cenotvorba = modul_cenotvorba.Cenotvorba(self)
        self.sklad = modul_sklad.Sklad(self)

        # Track all home button clicks
        self.home_buttons = [
            self.ui.homeArrow,
            self.ui.homeArrow2,
            self.ui.homeArrow3,
            self.ui.homeArrow4,
            self.ui.homeArrow5,
        ]
        self.commands.buttons_click(self.home_buttons, self.home)

        self.auto_update()

    def show(self):
        """Show the main App UI window."""
        self.ui.show()

    def home(self):
        self.commands.redirect(self.ui.index)

    def load_data(self):
        self.datafile_names = ['tovar', 'cennik', 'sklad', 'statistiky']
        self.data = {}
        for filename in self.datafile_names:
            self.data[filename] = DataFile(filename)

    def auto_update(self):
        self.timer = Timer(self.data)
        self.timer.run()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
