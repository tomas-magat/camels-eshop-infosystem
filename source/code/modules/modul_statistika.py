from utils.file import DataFile
from utils.ui_commands import UI_Commands
from utils import tools


class Statistika:

    def __init__(self, ui):

        self.ui = ui
        self.commands = UI_Commands(self.ui)

        # Track button clicks
        self.commands.button_click(
            self.ui.statistikaButton, self.switch_screen)
        # self.statistika_test()
        self.graph()
        # Read file 'tovar.txt'
        # self.tovar = DataFile('tovar')
        # self.goods = self.tovar.read()
        # self.version = self.tovar.get_version()

        # Update 'goods' variable every 3 seconds
        # tools.run_periodically(self.update_goods, 3)

    def switch_screen(self):
        """Redirect to this statistika screen."""

        self.commands.change_screen(self.ui.statistika)
    
    def statistika_test(self):
        x = [i for i in range(10)]
        y = [i/2 for i in range(10)]
        self.commands.plot_graph(self.ui.statistikaTestGraf, x,
                                 y, '-r', y, x, 'bo', title='Test')
    def graph(self):

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        self.commands.create_pyqtgraph(self.ui.statistikaTestGraf, hour, temperature)
        