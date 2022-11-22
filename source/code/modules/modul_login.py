from PyQt5 import QtWidgets, QtCore

from utils.ui_commands import UI_Commands


class Login:

    def __init__(self, ui):
        """
        This class handles everything done on the login
        screen (button clicks, item listing...).
        """

        self.ui = ui
        self.commands = UI_Commands(self.ui)

        self.button_clicks()

    def switch_to_portal(self):
        self.commands.redirect(self.ui.portal)

    def button_clicks(self):
        """All button click commands of login screen here."""
        
        self.commands.button_click(
            self.ui.pushButton_2, self.switch_to_portal)
        
        self.commands.button_click(
            self.ui.homeArrow6, self.switch_to_portal)
