from utils.files import File
from utils.ui_commands import UI_Commands
from utils import tools


class Portal:
    def __init__(self, ui):
        # Initiate UI of the window and UI_Commands
        self.ui = ui
        self.commands = UI_Commands(self.ui)
        # Track button clicks
        self.commands.button_click(
            self.ui.portal_button, self.switch_screen)
        # Read file 'tovar.txt'
        self.tovar = File('tovar')
        self.goods = self.tovar.read()
        self.version = self.tovar.get_version()
        # Update 'goods' variable every 3 seconds
        tools.run_periodically(self.update_goods, 3)

    # Update 'goods' variable if version of tovar.txt changed
    def update_goods(self):
        current_version = self.tovar.get_version()

        if current_version != self.version:
            self.goods = self.tovar.read()
            self.version = current_version

    # Redirect to this selling portal screen
    def switch_screen(self):
        self.commands.change_screen(self.ui.portal)
