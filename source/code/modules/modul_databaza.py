from PyQt5 import QtWidgets, QtCore, QtGui

from utils.ui_commands import UI_Commands
from utils import tools

class Databaza:

    def __init__(self, ui):
        """
        This class handles everything done on the portal
        screen (button clicks, item listing...).
        """

        self.ui = ui
        self.commands = UI_Commands(self.ui)

        self.commands.button_click(
            self.ui.databazaButton, self.switch_screen)

        self.commands.button_click(
            self.ui.addItem, self.add)

    def switch_screen(self):
        """Redirect to this portal screen."""

        self.commands.change_screen(self.ui.databaza)

    def add(self):
        self.ui.listWidget.addItem('test2')




