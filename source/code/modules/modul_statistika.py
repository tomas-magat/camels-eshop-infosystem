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
        
        self.statistiky = DataFile('statistiky').data
        self.tovar = DataFile('tovar').data
        self.sklad = DataFile('sklad').data
        self.cennik = DataFile('cennik').data
        self.font = {'fontname': 'Arial'}
        self.edgecolor = '#CAD2C5'
        self.linewidth = 2
        self.graph_color = '#CAD2C5'
        self.funFactsColor = '#2C57D8'

        self.Values()
        self.NajviacGraf()
        self.NajmenejGraf()
        self.VyvojGraf()
        self.FunFacts()

    def switch_screen(self):
        """Redirect to this statistika screen."""
        self.commands.redirect(self.ui.statistika)


    def Values(self):
        self.pocet_produktov = 0
        najviac_produkt = 0
        self.posledna_objednavka = '2003-09-10 10-34-59;P;kosela;5ks;5.99/ks'

        for k, v in self.sklad.items():
            self.pocet_produktov += int(v[0])
            if int(v[0]) > najviac_produkt:
                najviac_produkt = int(v[0])
                self.najviac_produkt = k

        top_produkty = []

        print(self.statistiky)
        for k1, v1 in self.statistiky.items():
            if v1[0] == 'P':
                top_produkty += v1[2],
                print(top_produkty)
            p=v1[2]

        for k, v in self.tovar.items():
            if k == p:
                p = v[0]
            if k == self.najviac_produkt:
                self.najviac_produkt = v[0]+'-'+str(najviac_produkt)+'ks'

        for k, v in self.cennik.items():
            if k == v1[2]:
                if v1[0] == 'P':
                    if v[1] == v1[4]:
                        t=True
                    else:
                        t=False
                elif v1[0] == 'N':
                    if v[0] == v1[4]:
                        t=True
                    else:
                        t=False
                else:
                    t=False

        if t:
            k1 = k1.split()[0]+' '+k1.split()[1].replace('-', ':')
            self.posledna_objednavka = k1+';'+v1[0]+';'+p+';'+v1[3]+'ks'+';'+v1[4]+'/ks'
        else:
            self.posledna_objednavka = 'chyba v subore STATISTIKY alebo CENNIK v produkte '+k

        self.x = [i for i in range(10)]
        self.y = [i/2 for i in range(10)]
        self.y1 = [i**2 for i in range(10)]
        self.top_ten = sorted([15, 9, 80, 69, 25, 90, 63, 78, 54, 75], reverse=True)
        self.top_ten_worst = sorted([70, 5, 69, 20, 25, 90, 63, 78, 54, 75])
        self.profLoss = 0
        self.avPrice = '23.58€'
        self.najviac_den = 'Sobotu (87)'


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
        x = np.arange(0, 1, 0.01)
        y = np.sin(2 * 2 * np.pi * x)

        fig, ax = plt.subplots()
        ax.set_title('Blitted cursor')
        ax.plot(x, y, 'o')
        blitted_cursor = BlittedCursor(ax)
        fig.canvas.mpl_connect('motion_notify_event', blitted_cursor.on_mouse_move)
        self.commands.plot_graph(self.ui.trzbyNaklady, fig, size=68.5)
        plt.tight_layout()

        # def on_draw(event):
        #     create_new_background()

        # def set_cross_hair_visible(visible):
        #     need_redraw = horizontal_line.get_visible() != visible
        #     horizontal_line.set_visible(visible)
        #     horizontal_line1.set_visible(visible)
        #     vertical_line.set_visible(visible)
        #     text.set_visible(visible)
        #     return need_redraw

        # def create_new_background():
        #     global background
        #     if creating_background: 
        #         return
        #     creating_background = True
        #     set_cross_hair_visible(False)
        #     a3.figure.canvas.draw()
        #     background = a3.figure.canvas.copy_from_bbox(a3.bbox)
        #     set_cross_hair_visible(True)
        #     creating_background = False

        # def on_mouse_move(event):
        #     if background is None:
        #         create_new_background()
        #     if not event.inaxes:
        #         need_redraw = set_cross_hair_visible(False)
        #         if need_redraw:
        #             a3.figure.canvas.restore_region(background)
        #             a3.figure.canvas.blit(a3.bbox)
        #     else:
        #         index = min(np.searchsorted(x, event.xdata), len(x) - 1)
        #         set_cross_hair_visible(True)
        #         horizontal_line.set_ydata(y[index])
        #         horizontal_line1.set_ydata(z[index])
        #         vertical_line.set_xdata(x[index])
        #         text.set_text('x=%1.2f, y=%1.2f' % (event.xdata, event.ydata))

        #         a3.figure.canvas.restore_region(background)
        #         a3.draw_artist(horizontal_line)
        #         a3.draw_artist(horizontal_line1)
        #         a3.draw_artist(vertical_line)
        #         a3.draw_artist(text)
        #         a3.figure.canvas.blit(a3.bbox)



        # vyvoj_ceny, a3 = plt.subplots(
        #     figsize=[7.18, 3.21], linewidth=self.linewidth, edgecolor=self.edgecolor)
        # vyvoj_ceny.set_facecolor(self.graph_color)
        # a3.set_facecolor(self.graph_color)
        # a3.spines['top'].set_visible(False)
        # a3.spines['right'].set_visible(False)
        # a3.set_title('Vyvoj ceny', **self.font, fontsize=15,
        #              weight='bold')
        # line, = a3.plot(self.x, self.y, label='naklady')
        # line1, = a3.plot(self.x, self.y1, label='vynosy')
        # background = None
        # horizontal_line = a3.axhline(color='k', lw=0.8, ls='--')
        # horizontal_line1 = a3.axhline(color='k', lw=0.8, ls='--')
        # vertical_line = a3.axvline(color='k', lw=0.8, ls='--')
        # x, y = line.get_data()
        # x, z = line1.get_data()
        # creating_background = False
        # text = a3.text(0.72, 0.9, '', transform=a3.transAxes)
        # a3.figure.canvas.mpl_connect('draw_event', on_draw)
        # vyvoj_ceny.canvas.mpl_connect('motion_notify_event', on_mouse_move)
        # self.commands.plot_graph(self.ui.trzbyNaklady, vyvoj_ceny, size=68.5)
        # plt.tight_layout()


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
        self.ui.label_10.setText(str(self.pocet_produktov))
        self.ui.label_10.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_12.setText(self.najviac_den)
        self.ui.label_12.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_16.setText(self.najviac_produkt)
        self.ui.label_16.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_14.setText(self.posledna_objednavka)
        self.ui.label_14.setStyleSheet('color:'+self.funFactsColor)
        self.ui.camelLogo_2.setToolTip('')


class BlittedCursor:
    """
    A cross hair cursor using blitting for faster redraw.
    """
    def __init__(self, ax):
        self.ax = ax
        self.background = None
        self.horizontal_line = ax.axhline(color='k', lw=0.8, ls='--')
        self.vertical_line = ax.axvline(color='k', lw=0.8, ls='--')
        # text location in axes coordinates
        self.text = ax.text(0.72, 0.9, '', transform=ax.transAxes)
        self._creating_background = False
        ax.figure.canvas.mpl_connect('draw_event', self.on_draw)

    def on_draw(self, event):
        self.create_new_background()

    def set_cross_hair_visible(self, visible):
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)
        return need_redraw

    def create_new_background(self):
        if self._creating_background:
            # discard calls triggered from within this function
            return
        self._creating_background = True
        self.set_cross_hair_visible(False)
        self.ax.figure.canvas.draw()
        self.background = self.ax.figure.canvas.copy_from_bbox(self.ax.bbox)
        self.set_cross_hair_visible(True)
        self._creating_background = False

    def on_mouse_move(self, event):
        if self.background is None:
            self.create_new_background()
        if not event.inaxes:
            need_redraw = self.set_cross_hair_visible(False)
            if need_redraw:
                self.ax.figure.canvas.restore_region(self.background)
                self.ax.figure.canvas.blit(self.ax.bbox)
        else:
            self.set_cross_hair_visible(True)
            # update the line positions
            x, y = event.xdata, event.ydata
            self.horizontal_line.set_ydata(y)
            self.vertical_line.set_xdata(x)
            self.text.set_text('x=%1.2f, y=%1.2f' % (x, y))

            self.ax.figure.canvas.restore_region(self.background)
            self.ax.draw_artist(self.horizontal_line)
            self.ax.draw_artist(self.vertical_line)
            self.ax.draw_artist(self.text)
            self.ax.figure.canvas.blit(self.ax.bbox)