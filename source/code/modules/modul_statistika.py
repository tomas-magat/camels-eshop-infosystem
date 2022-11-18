from utils.file import DataFile
from utils.ui_commands import UI_Commands
from utils import tools
import matplotlib.pyplot as plt


class Statistika:

    def __init__(self, ui):

        self.ui = ui
        self.commands = UI_Commands(self.ui)

        # Track button clicks
        self.commands.button_click(
            self.ui.statistikaButton, self.switch_screen)
        self.statistika_test()
        # Read file 'tovar.txt'
        # self.tovar = DataFile('tovar')
        # self.goods = self.tovar.read()
        # self.version = self.tovar.get_version()

        # Update 'goods' variable every 3 seconds
        # tools.run_periodically(self.update_goods, 3)

    def switch_screen(self):
        """Redirect to this statistika screen."""

        self.commands.redirect(self.ui.statistika)

    def statistika_test(self):
        # data
        x = [i for i in range(10)]
        y = [i/2 for i in range(10)]
        y1 = [i**2 for i in range(10)]
        m = [4, 5, 2]
        # fig, ax = plt.subplot_mosaic([['upleft', 'upright'], ['lowleft', 'lowright']])
        plt.style.use(['seaborn-v0_8-notebook'])
        fig, (a1, a2) = plt.subplots(1, 2)
        # a1 = fig.add_subplot(1,2,1)
        # a2 = fig.add_subplot(1,2,2)
        c = ['a', 'b', 'c']
        a1.bar(c, m)
        a1.margins(0.2, 0.2)
        # a1.plot(x,y)
        # a1.plot(x,y1)
        a2.plot(x, y)
        a2.plot(x, y1)

        self.commands.plot_graph(self.ui.statistikaTestGraf, fig)
