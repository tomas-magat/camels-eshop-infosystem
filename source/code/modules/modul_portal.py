# Modul Portal -
# Lists catalog of available products, has an option
# to search by code/name and to filter products.
# After ordering the selected items in given amounts,
# creates file uctenka_[id_transakcie].txt.

from utils.ui_commands import UI_Commands


class Portal:

    def __init__(self, ui):
        """
        This class handles everything done on the portal
        screen (button clicks, item listing...).
        """

        self.ui = ui
        self.commands = UI_Commands(self.ui)

        self.commands.button_click(
            self.ui.portalButton, self.switch_screen)

        # Read file 'tovar.txt' - not in prototype
        # self.tovar = DataFile('tovar')
        # self.goods = self.tovar.read()
        # self.version = self.tovar.get_version()

        # Update 'goods' variable every 3 seconds
        # tools.run_periodically(self.update_goods, 3)

    def update_goods(self):
        """
        Update 'goods' variable if version of the tovar.txt
        datafile has changed.
        """

        current_version = self.tovar.get_version()

        if current_version != self.version:
            self.goods = self.tovar.read()
            self.version = current_version

    def switch_screen(self):
        """Redirect to this portal screen."""

        self.commands.change_screen(self.ui.portal)
