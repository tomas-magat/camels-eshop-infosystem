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
        
        self.x = [i for i in range(10)]
        self.y = [i/2 for i in range(10)]
        self.y1 = [i**2 for i in range(10)]
        self.top_ten = sorted([15, 9, 80, 69, 25, 90, 63, 78, 54, 75], reverse=True)
        self.top_ten_worst = sorted([70, 5, 69, 20, 25, 90, 63, 78, 54, 75])
        self.font = {'fontname': 'Arial'}
        self.edgecolor = '#CAD2C5'
        self.linewidth = 2
        self.graph_color = '#CAD2C5'
        self.profLoss = 0
        self.funFactsColor = '#2C57D8'
        self.avPrice = '23.58€'

        self.NajviacGraf()
        self.NajmenejGraf()
        self.VyvojGraf()
        self.FunFacts()

    def switch_screen(self):
        """Redirect to this statistika screen."""
        self.commands.redirect(self.ui.statistika)



    def NajviacGraf(self):
        najviac, a1 = plt.subplots(
            figsize=[4.9, 3.15], linewidth=self.linewidth, edgecolor=self.edgecolor)
        najviac.patch.set_facecolor(self.graph_color)
        a1.set_facecolor(self.graph_color)
        a1.spines['top'].set_visible(False)
        a1.spines['right'].set_visible(False)
        a1.axes.xaxis.set_ticklabels([])
        a1.tick_params(axis='x', which='both', length=0)
        a1.set_title('Najpredavanejsie produkty', **
                     self.font, fontsize=15, weight='bold')
        bar_X = [0,1,2,3,4,5,6,7,8,9]
        bars1 = a1.bar(bar_X, self.top_ten)
        bar_X = []
        for bar in bars1:
            bar_X.append(bar.get_x())
        
        annot1 = a1.annotate("", xy=(0, 0), xytext=(0, 10), textcoords='offset points', ha='center', color='white', size=15,
                             bbox=dict(boxstyle="round", fc='#2F3E46', alpha=1, ec="#101416", lw=2))
        annot1.set_visible(False)
        def update_annot1(event,bar_x_pos):
            x = event.xdata
            y = event.ydata+5
            annot1.xy = (x, y)
            for c, i in enumerate(bar_X):
                if i == bar_x_pos:
                    text = self.top_ten[c]
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
        self.commands.plot_graph(self.ui.najviacGraf, najviac)


    def NajmenejGraf(self):
        najmenej, a2 = plt.subplots(
            figsize=[4.9, 3.15], linewidth=self.linewidth, edgecolor=self.edgecolor)
        najmenej.patch.set_facecolor(self.graph_color)
        a2.set_facecolor(self.graph_color)
        a2.spines['top'].set_visible(False)
        a2.spines['right'].set_visible(False)
        a2.axes.xaxis.set_ticklabels([])
        a2.tick_params(axis='x', which='both', length=0)
        a2.set_title('Najmenej predavane produkty', **
                     self.font, fontsize=15, weight='bold')
        bar_X = [0,1,2,3,4,5,6,7,8,9]
        bars2 = a2.bar(bar_X, self.top_ten_worst)
        bar_X = []
        for bar in bars2:
            bar_X.append(bar.get_x())

        annot2 = a2.annotate("", xy=(0, 0), xytext=(0, 10), textcoords='offset points', ha='center', color='white', size=15,
                             bbox=dict(boxstyle="round", fc='#2F3E46', alpha=1, ec="#101416", lw=2))
        annot2.set_visible(False)
        def update_annot2(event,bar_x_pos):
            x = event.xdata
            y = event.ydata+5
            annot2.xy = (x, y)
            for c, i in enumerate(bar_X):
                if i == bar_x_pos:
                    text = self.top_ten_worst[c]
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
        self.commands.plot_graph(self.ui.najmenejGraf, najmenej)


    def VyvojGraf(self):      
        def on_draw(event):
            create_new_background()

        def set_cross_hair_visible(visible):
            need_redraw = horizontal_line.get_visible() != visible
            horizontal_line.set_visible(visible)
            horizontal_line1.set_visible(visible)
            vertical_line.set_visible(visible)
            text.set_visible(visible)
            return need_redraw

        def create_new_background():
            global creating_background, background
            if creating_background: 
                return
            creating_background = True
            set_cross_hair_visible(False)
            a3.figure.canvas.draw()
            background = a3.figure.canvas.copy_from_bbox(a3.bbox)
            set_cross_hair_visible(True)
            creating_background = False

        def on_mouse_move(event):
            if background is None:
                create_new_background()
            if not event.inaxes:
                need_redraw = set_cross_hair_visible(False)
                if need_redraw:
                    a3.figure.canvas.restore_region(background)
                    a3.figure.canvas.blit(a3.bbox)
            else:
                index = min(np.searchsorted(x, event.xdata), len(x) - 1)
                set_cross_hair_visible(True)
                horizontal_line.set_ydata(y[index])
                horizontal_line1.set_ydata(z[index])
                vertical_line.set_xdata(x[index])
                text.set_text('x=%1.2f, y=%1.2f' % (event.xdata, event.ydata))

                a3.figure.canvas.restore_region(background)
                a3.draw_artist(horizontal_line)
                a3.draw_artist(horizontal_line1)
                a3.draw_artist(vertical_line)
                a3.draw_artist(text)
                a3.figure.canvas.blit(a3.bbox)



        vyvoj_ceny, a3 = plt.subplots(
            figsize=[7.18, 3.21], linewidth=self.linewidth, edgecolor=self.edgecolor)
        vyvoj_ceny.set_facecolor(self.graph_color)
        a3.set_facecolor(self.graph_color)
        a3.spines['top'].set_visible(False)
        a3.spines['right'].set_visible(False)
        a3.set_title('Vyvoj ceny', **self.font, fontsize=15,
                     weight='bold')
        line, = a3.plot(self.x, self.y, label='naklady')
        line1, = a3.plot(self.x, self.y1, label='vynosy')
        background = None
        horizontal_line = a3.axhline(color='k', lw=0.8, ls='--')
        horizontal_line1 = a3.axhline(color='k', lw=0.8, ls='--')
        vertical_line = a3.axvline(color='k', lw=0.8, ls='--')
        x, y = line.get_data()
        x, z = line1.get_data()
        creating_background = False
        text = a3.text(0.72, 0.9, '', transform=a3.transAxes)
        a3.figure.canvas.mpl_connect('draw_event', on_draw)
        vyvoj_ceny.canvas.mpl_connect('motion_notify_event', on_mouse_move)
        self.commands.plot_graph(self.ui.trzbyNaklady, vyvoj_ceny, size=68.5)
        plt.tight_layout()


    def FunFacts(self):
        if self.profLoss < 0:
            profLossColor = '#FF0000'
        elif self.profLoss > 0:
            profLossColor = '#21BF3E'
        else:
            profLossColor = '#717171'


        self.ui.label_6.setText(str(self.profLoss)+'€')
        self.ui.label_6.setToolTip('''tato cena s pravidla vyjadruje zisk alebo stratu firmy za jeden den
napriklad od 2000.1.1 0:00:00 - 2000.1.1 23:59:59
pre detailnejsie zobrazenie vyvoju ceny firmy pozri graf nizsie -->''')
        self.ui.label_6.setStyleSheet('''QToolTip {
                                        font-size:9pt;
                                        color:white;
                                        background-color: #2F3E46;
                                        border: 1px solid #101416;}
                                        #label_6 {color: %s}''' % profLossColor)
        self.ui.label_20.setText(self.avPrice)
        self.ui.label_20.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_10.setText('2 678')
        self.ui.label_10.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_12.setText('Sobotu (87)')
        self.ui.label_12.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_16.setText('Topanok (865 parov)')
        self.ui.label_16.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_14.setText('2003-09-10 10-34-59;kosela;5ks;5.99/ks')
        self.ui.label_14.setStyleSheet('color:'+self.funFactsColor)
        self.ui.camelLogo_2.setToolTip('')
