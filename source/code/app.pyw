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
        self.databaza = modul_databaza.Databaza(self.ui, self.data)
        self.statistika = modul_statistika.Statistika(self.ui, self.data)
        self.cenotvorba = modul_cenotvorba.Cenotvorba(self.ui, self.data)
        self.sklad = modul_sklad.Sklad(self.ui, self.data)

        # Track all home button clicks
        self.home_buttons = [
            self.ui.homeArrow,
            self.ui.homeArrow2,
            self.ui.homeArrow3,
            self.ui.homeArrow4,
            self.ui.homeArrow5,
        ]
        self.commands.buttons_click(self.home_buttons, self.index)

        self.auto_updating()
        self.thread.start()

    def show(self):
        """Show the main App UI window."""
        self.ui.show()

    def index(self):
        self.commands.redirect(self.ui.index)

    def auto_updating(self):
        self.thread = QThread()
        self.timer = Timer(self.data)
        self.timer.moveToThread(self.thread)
        self.thread.started.connect(self.timer.run)
        self.thread.finished.connect(self.thread.deleteLater)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
