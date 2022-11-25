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
        c = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        m1 = sorted([15, 9, 420, 69, 25, 90, 63, 78, 54, 75], reverse=True)
        m2 = sorted([420, 5, 69, 20, 25, 90, 63, 78, 54, 75])
        # plt.style.use(['seaborn-v0_8-notebook'])
        font = {'fontname':'Arial'}
        edgecolor = '#757575'
        linewidth = 2
        graph_color = '#FFFFFF'

        najviac, a1 = plt.subplots(figsize=[4.9,3.15],linewidth=linewidth, edgecolor=edgecolor)
        najviac.patch.set_facecolor(graph_color)
        # a1.margins(0.2, 0.2)
        a1.set_facecolor(graph_color)
        a1.spines['top'].set_visible(False)
        a1.spines['right'].set_visible(False)
        a1.axes.xaxis.set_ticklabels([])
        a1.tick_params(axis='x', which='both', length=0)
        a1.set_title('Najpredavanejsie produkty',**font,fontsize=15,weight='bold')
        a1.bar(c, m1)
        # a1.spines['left'].set_visible(False)
        # a1.spines['bottom'].set_visible(False)

        najmenej, a2 = plt.subplots(figsize=[4.9,3.15],linewidth=linewidth, edgecolor=edgecolor)
        najmenej.patch.set_facecolor(graph_color)
        a2.set_facecolor(graph_color)
        a2.spines['top'].set_visible(False)
        a2.spines['right'].set_visible(False)
        a2.axes.xaxis.set_ticklabels([])
        a2.tick_params(axis='x', which='both', length=0)
        a2.set_title('Najmenej predavane produkty',**font,fontsize=15,weight='bold')
        a2.bar(c, m2)

        vyvoj_ceny, a3 = plt.subplots(figsize=[7.18,3.5],linewidth=linewidth, edgecolor=edgecolor)
        vyvoj_ceny.set_facecolor(graph_color)
        a3.set_facecolor(graph_color)
        a3.spines['top'].set_visible(False)
        a3.spines['right'].set_visible(False)
        a3.set_title('Vyvoj ceny',**font,fontsize=15,weight='bold')#backgroundcolor= 'silver'
        # a3.set_xlabel('x-label')  # , fontsize=fontsize)
        # a3.set_ylabel('y-label')  # , fontsize=fontsize)
        # a3.set_title('Title')  # , fontsize=fontsize)
        a3.plot(x, y, label='naklady')
        a3.plot(x, y1,label='vynosy')
        a3.legend(frameon=False,fontsize=15)


        
        plt.tight_layout()

        c = '-0,05%'
        b = '#FF0000'
        f = '23,58€'
        self.commands.plot_graph(self.ui.najviacGraf, najviac)
        self.commands.plot_graph(self.ui.najmenejGraf, najmenej)
        self.commands.plot_graph_trzby(self.ui.trzbyNaklady, vyvoj_ceny)

        self.ui.label_6.setText(c)
        self.ui.label_6.setStyleSheet('color:'+b)
        self.ui.label_20.setText(f)
        self.ui.label_10.setText('2 678')
        self.ui.label_10.setStyleSheet('color:#2596be')
        self.ui.label_12.setText('Sobotu (87)')
        self.ui.label_12.setStyleSheet('color:#2596be')
        self.ui.label_16.setText('Topanok (865 parov)')
        self.ui.label_16.setStyleSheet('color:#2596be')
        self.ui.label_14.setText('2003-09-10 10-34-59;kosela;5ks;5.99/ks')
        self.ui.label_14.setStyleSheet('color:#2596be')