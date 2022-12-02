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
        self.statistika()
        # Read file 'tovar.txt'
        # self.tovar = DataFile('tovar')
        # self.goods = self.tovar.read()
        # self.version = self.tovar.get_version()

        # Update 'goods' variable every 3 seconds
        # tools.run_periodically(self.update_goods, 3)

    def switch_screen(self):
        """Redirect to this statistika screen."""
        self.commands.redirect(self.ui.statistika)

    def statistika(self):
        x = [i for i in range(10)]
        y = [i/2 for i in range(10)]
        y1 = [i**2 for i in range(10)]
        top_ten = sorted([15, 9, 80, 69, 25, 90, 63, 78, 54, 75], reverse=True)
        top_ten_worst = sorted([70, 5, 69, 20, 25, 90, 63, 78, 54, 75])
        font = {'fontname': 'Arial'}
        edgecolor = '#757575'
        linewidth = 2
        graph_color = '#FFFFFF'

        najviac, a1 = plt.subplots(
            figsize=[4.9, 3.15], linewidth=linewidth, edgecolor=edgecolor)
        najviac.patch.set_facecolor(graph_color)
        # a1.margins(0.2, 0.2)
        a1.set_facecolor(graph_color)
        a1.spines['top'].set_visible(False)
        a1.spines['right'].set_visible(False)
        a1.axes.xaxis.set_ticklabels([])
        a1.tick_params(axis='x', which='both', length=0)
        a1.set_title('Najpredavanejsie produkty', **
                     font, fontsize=15, weight='bold')
        bar_X = [0,1,2,3,4,5,6,7,8,9]
        bars1 = a1.bar(bar_X, top_ten)
        bar_X = []
        for bar in bars1:
            bar_X.append(bar.get_x())
        

        annot1 = a1.annotate("", xy=(0, 0), xytext=(0, 10), textcoords='offset points', ha='center', color='white', size=15,
                             bbox=dict(boxstyle="round", fc='#2F3E46', alpha=1, ec="#101416", lw=2))
        annot1.set_visible(False)
        def update_annot1(event,bar_x_pos):
            xaxis_length = abs((plt.xlim()[0]*-1)+plt.xlim()[1])
            yaxis_length = abs((plt.ylim()[0]*-1)+plt.ylim()[1])
            x = xaxis_length/0.775*event.x/260-2.5
            y = yaxis_length/0.77*event.y/175.275-10
            annot1.xy = (x, y)
            for c,i in enumerate(bar_X):
                if i == bar_x_pos:
                    text = top_ten[c]
            annot1.set_text(text)
        def hover1(event):
            vis = annot1.get_visible()
            if event.inaxes == a1:
                for bar in bars1:
                    bar_x_pos = bar.get_x()
                    cont = bar.contains(event)
                    if cont[0]:
                        update_annot1(event,bar_x_pos)
                        annot1.set_visible(True)
                        najviac.canvas.draw_idle()
                        return
                    else:
                        if vis:
                            annot1.set_visible(False)
                            najviac.canvas.draw_idle()
        najviac.canvas.mpl_connect("motion_notify_event", hover1)
        # a1.spines['left'].set_visible(False)
        # a1.spines['bottom'].set_visible(False)

        najmenej, a2 = plt.subplots(
            figsize=[4.9, 3.15], linewidth=linewidth, edgecolor=edgecolor)
        najmenej.patch.set_facecolor(graph_color)
        a2.set_facecolor(graph_color)
        a2.spines['top'].set_visible(False)
        a2.spines['right'].set_visible(False)
        a2.axes.xaxis.set_ticklabels([])
        a2.tick_params(axis='x', which='both', length=0)
        a2.set_title('Najmenej predavane produkty', **
                     font, fontsize=15, weight='bold')
        bar_X = [0,1,2,3,4,5,6,7,8,9]
        bars2 = a2.bar(bar_X, top_ten_worst)
        bar_X = []
        for bar in bars2:
            bar_X.append(bar.get_x())

        annot2 = a2.annotate("", xy=(0, 0), xytext=(0, 10), textcoords='offset points', ha='center', color='white', size=15,
                             bbox=dict(boxstyle="round", fc='#2F3E46', alpha=1, ec="#101416", lw=2))
        annot2.set_visible(False)

        def update_annot2(event,bar_x_pos):
            xaxis_length = abs((plt.xlim()[0]*-1)+plt.xlim()[1])
            yaxis_length = abs((plt.ylim()[0]*-1)+plt.ylim()[1])
            x = xaxis_length/0.775*event.x/260-2.5
            y = yaxis_length/0.77*event.y/175.275-10
            annot2.xy = (x, y)
            for c,i in enumerate(bar_X):
                if i == bar_x_pos:
                    text = top_ten_worst[c]
            annot2.set_text(text)

        def hover2(event):
            vis = annot2.get_visible()
            if event.inaxes == a2:
                for bar in bars2:
                    bar_x_pos = bar.get_x()
                    cont = bar.contains(event)
                    if cont[0]:
                        update_annot2(event,bar_x_pos)
                        annot2.set_visible(True)
                        najmenej.canvas.draw_idle()
                        return
                    else:
                        if vis:
                            annot2.set_visible(False)
                            najmenej.canvas.draw_idle()
        najmenej.canvas.mpl_connect("motion_notify_event", hover2)

        vyvoj_ceny, a3 = plt.subplots(
            figsize=[7.18, 3.21], linewidth=linewidth, edgecolor=edgecolor)
        vyvoj_ceny.set_facecolor(graph_color)
        a3.set_facecolor(graph_color)
        a3.spines['top'].set_visible(False)
        a3.spines['right'].set_visible(False)
        a3.set_title('Vyvoj ceny', **font, fontsize=15,
                     weight='bold')  # backgroundcolor= 'silver'
        a3.plot(x, y, label='naklady')
        a3.plot(x, y1, label='vynosy')
        a3.legend(frameon=False, fontsize=15)

        plt.tight_layout()
        self.commands.plot_graph(self.ui.najviacGraf, najviac)
        self.commands.plot_graph(self.ui.najmenejGraf, najmenej)
        self.commands.plot_graph_trzby(self.ui.trzbyNaklady, vyvoj_ceny)
        

        profLoss = 0
        if profLoss < 0:
            profLossColor = '#FF0000'
        elif profLoss > 0:
            profLossColor = '#21BF3E'
        else:
            profLossColor = '#717171'

        funFactsColor = '#2C57D8'
        avPrice = '23.58€'

        self.ui.label_6.setText(str(profLoss)+'€')
        self.ui.label_6.setToolTip('''tato cena s pravidla vyjadruje zisk alebo stratu firmy za jeden den
napriklad od 2000.1.1 0:00:00 - 2000.1.1 23:59:59
pre detailnejsie zobrazenie vyvoju ceny firmy pozri grafy nizsie''')
        self.ui.label_6.setStyleSheet('''QToolTip {
                                        font-size:9pt;
                                        color:white; padding:2px;
                                        border-width:2px;
                                        border-style:solid;
                                        border-radius:20px;
                                        background-color: #2F3E46;
                                        border: 1px solid #101416;}
                                        #label_6 {color: %s}''' % profLossColor)
        self.ui.label_20.setText(avPrice)
        self.ui.label_10.setText('2 678')
        self.ui.label_10.setStyleSheet('color:'+funFactsColor)
        self.ui.label_12.setText('Sobotu (87)')
        self.ui.label_12.setStyleSheet('color:'+funFactsColor)
        self.ui.label_16.setText('Topanok (865 parov)')
        self.ui.label_16.setStyleSheet('color:'+funFactsColor)
        self.ui.label_14.setText('2003-09-10 10-34-59;kosela;5ks;5.99/ks')
        self.ui.label_14.setStyleSheet('color:'+funFactsColor)
