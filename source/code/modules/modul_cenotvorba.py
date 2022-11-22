
from utils.ui_commands import UI_Commands


class Cenotvorba:

    def __init__(self, ui):

        self.ui = ui
        self.commands = UI_Commands(self.ui)
        self.commands.button_click(
            self.ui.cenotvorbaButton, self.switch_screen)
        self.loadfile()

    def switch_screen(self):

        self.commands.redirect(self.ui.cenotvorba)

    def loadfile(self):
        
