import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from main_ui import Ui_MainWindow
from utils.ui_commands import UI_Commands
from modules import *


class MainWindow:
    def __init__(self):
        # Setup the window
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.commands = UI_Commands(self.ui)
        # Set default screen to index
        self.commands.change_screen(self.ui.index)

        # Initialize modul portal
        self.portal = modul_portal.Portal(self.ui)
        # Track button clicks for index screen (module buttons)
        self.commands.button_click(self.ui.cenotvorba_button, self.price)
        self.commands.button_click(self.ui.statistika_button, self.stats)
        self.commands.button_click(self.ui.sklad_button, self.storage)
        self.commands.button_click(self.ui.databaza_button, self.database)

        # Track all home button clicks
        self.home_buttons = [
            self.ui.home,
            self.ui.home_2,
            self.ui.home_3,
            self.ui.home_4,
            self.ui.home_5,
        ]
        self.commands.multiple_button_click(self.home_buttons, self.index)

    # Show the main window
    def show(self):
        self.main_win.show()

    def price(self):
        self.commands.change_screen(self.ui.cenotvorba)

    def stats(self):
        self.commands.change_screen(self.ui.statistika)

    def storage(self):
        self.commands.change_screen(self.ui.sklad)

    def database(self):
        self.commands.change_screen(self.ui.databaza)

    def index(self):
        self.commands.change_screen(self.ui.index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
