from utils.file import DataFile
from utils.ui_commands import UI_Commands
from utils import tools
import matplotlib.pyplot as plt
import numpy as np


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
        c = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        m1 = [15, 9, 420, 69, 25, 90, 63, 78, 54, 75]
        m2 = [420, 5, 69, 20, 25, 90, 63, 78, 54, 75]
        # fig, ax = plt.subplot_mosaic([['upleft', 'upright'], ['lowleft', 'lowright']])
        # fig, (a1, a2, a3) = plt.subplots()
        # a1 = fig.add_subplot(1,2,1)
        # a2 = fig.add_subplot(1,2,2)
        plt.style.use(['seaborn-v0_8-notebook'])

        najviac, a1 = plt.subplots()
        najviac.patch.set_facecolor('#CED6C9')
        # a1.margins(0.2, 0.2)
        a1.set_facecolor('#CED6C9')
        a1.spines['top'].set_visible(False)
        a1.spines['right'].set_visible(False)
        a1.axes.xaxis.set_ticklabels([])
        a1.tick_params(axis='x', which='both', length=0)
        a1.bar(c, m1)
        # a1.spines['left'].set_visible(False)
        # a1.spines['bottom'].set_visible(False)

        najmenej, a2 = plt.subplots()#, linewidth=1, edgecolor='black')
        najmenej.patch.set_facecolor('#CED6C9')
        a2.bar(c, m2)
        a2.set_facecolor('#CED6C9')
        a2.spines['top'].set_visible(False)
        a2.spines['right'].set_visible(False)
        a2.axes.xaxis.set_ticklabels([])
        a2.tick_params(axis='x', which='both', length=0)

        vyvoj_ceny, a3 = plt.subplots()
        vyvoj_ceny.set_facecolor('#CED6C9')
        # a3.set_xlabel('x-label')  # , fontsize=fontsize)
        # a3.set_ylabel('y-label')  # , fontsize=fontsize)
        # a3.set_title('Title')  # , fontsize=fontsize)
        a3.set_facecolor('#CED6C9')
        a3.spines['top'].set_visible(False)
        a3.spines['right'].set_visible(False)
        a3.plot(x, y)
        a3.plot(x, y1)

        # fig.set_facecolor('grey')
        # a1 = plt.subplot(321)
        # a2 = plt.subplot(323)
        # a1.plot(x,y)
        # a1.plot(x,y1)
        # a3 = plt.subplot(325)
        # fig, ax = plt.subplot_mosaic([['upleft', 'upright'], ['lowleft', 'lowright']])
        # fig, (a1, a2, a3) = plt.subplots()
        # a1 = fig.add_subplot(1,2,1)
        # a2 = fig.add_subplot(1,2,2)
        # a4 = plt.subplot(122)
        # a4.bar(c, m)
        plt.tight_layout()#pad=5, w_pad=5, h_pad=5)
        # plt.rcParams["figure.autolayout"] = True


        self.commands.plot_graph(self.ui.najviacGraf, najviac)
        # self.commands.plot_graph(self.ui.najmenejGraf, najmenej)
        self.commands.plot_graph(self.ui.trzbyNaklady, vyvoj_ceny)