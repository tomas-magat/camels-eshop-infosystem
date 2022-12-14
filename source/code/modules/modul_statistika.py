from utils.file import DataFile
from utils.ui_commands import UI_Commands
from utils import tools
import matplotlib.pyplot as plt
import numpy as np
from decimal import *


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

        if len(list(self.statistiky)) > 2:
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
        self.profLoss = 0
        self.avPrice = 0
        najviac_produkt = 0
        self.posledna_objednavka_Z = 'ziadna'
        self.posledna_objednavka_F = 'ziadna'

        for k, v in self.sklad.items():
            self.pocet_produktov += int(v[0])
            if int(v[0]) > najviac_produkt:
                najviac_produkt = int(v[0])
                self.najviac_produkt = k

        top_produkty = []
        self.statistika_list = []
        p, p1, k2, v2, k4, v4 = '', '', '', '', '', ''
        # TODO: daj si niaku podmienku ze to nacita tie data iba ked
        # len(self.sklad.items()) > 0 lebo ked je prazdny subor
        # statistiky.txt tak vypise chybu ze k1, v1 neexistuje
        for k1, v1 in self.statistiky.items():
            m = 0
            if v1[0] == 'P':
                if top_produkty == []:
                    top_produkty.append([v1[2], 1])
                else:
                    for i in range(len(top_produkty)):
                        if v1[2] == top_produkty[i][0]:
                            top_produkty[i][1] += 1
                            m = 1
                            break
                    if m == 0:
                        top_produkty.append([v1[2], 1])
                k2, v2 = k1, v1
                p = v1[2]
            else:
                k4, v4 = k1, v1
                p1 = v1[2]
            self.statistika_list += (k1.split()
                                     [0], k1.split()[1], v1[0], v1[2], v1[3], v1[4]),
        prem = k1.split()[0]
        novy_cas = []
        for i in range(len(self.statistika_list)-1, -1, -1):
            if self.statistika_list[i][0] == prem:
                novy_cas += self.statistika_list[i],
        for i in novy_cas:
            if i[2] == 'P':
                self.profLoss += int(i[4])*float(i[5])
            else:
                self.profLoss -= int(i[4])*float(i[5])
        self.profLoss = round(self.profLoss, 2)

        ttt = 0
        for i in self.statistika_list:
            if i[2] == 'P':
                self.avPrice += int(i[4])*float(i[5])
                ttt += 1
        self.avPrice /= ttt
        self.avPrice = round(self.avPrice, 2)

        self.x_date = []
        for i in self.statistika_list:
            aa = i[0].split('-')[0][2:]
            bb = i[0].split('-')[1]
            cc = i[0].split('-')[2]
            if not self.x_date:
                self.x_date += cc+'.'+bb+'.'+aa,
            elif cc+'.'+bb+'.'+aa != self.x_date[-1]:
                self.x_date += cc+'.'+bb+'.'+aa,

        self.profit_all = [0]
        self.loss_all = [0]
        date_var1 = self.statistika_list[0][0]
        date_var2 = self.statistika_list[0][0]
        for am, i in enumerate(self.statistika_list):
            io = False
            oi = False
            if i[2] == 'P':
                if date_var1 == self.statistika_list[am][0]:
                    self.profit_all[-1] += int(i[4])*float(i[5])
                else:
                    self.profit_all += int(i[4])*float(i[5]),
                    date_var1 = self.statistika_list[am][0]
                    io = True
            else:
                if date_var2 == self.statistika_list[am][0]:
                    self.loss_all[-1] += int(i[4])*float(i[5])
                else:
                    self.loss_all += int(i[4])*float(i[5]),
                    date_var2 = self.statistika_list[am][0]
                    oi = True
            if io:
                if self.loss_all != []:
                    self.loss_all += self.loss_all[-1],
                else:
                    self.loss_all += 0,
            elif oi:
                if self.profit_all != []:
                    self.profit_all += self.profit_all[-1],
                else:
                    self.profit_all += 0,

        h = True
        for k, v in self.tovar.items():
            if k == p:
                p = v[0]
            if k == p1:
                p1 = v[0]
            if k == self.najviac_produkt:
                self.najviac_produkt = v[0]+'-'+str(najviac_produkt)+'ks'
                h = False
        if h:
            self.najviac_produkt = 'produkt '+self.najviac_produkt+' nepridany v TOVARE'

        for k, v in self.cennik.items():
            if k == v1[2]:
                if v1[0] == 'P':
                    if v[1] == v1[4]:
                        t = True
                    else:
                        t = False
                elif v1[0] == 'N':
                    if v[0] == v1[4]:
                        t = True
                    else:
                        t = False
                else:
                    t = False
        if t:
            if k2 != '':
                k2 = k2.split()[0].replace('-', '.')+' ' + \
                    k2.split()[1].replace('-', ':')
                self.posledna_objednavka_Z = k2+';' + \
                    p+';'+v2[3]+'ks'+';'+v2[4]+'/ks'
            if k4 != '':
                k4 = k4.split()[0].replace('-', '.')+' ' + \
                    k4.split()[1].replace('-', ':')
                self.posledna_objednavka_F = k4+';' + \
                    p1+';'+v4[3]+'ks'+';'+v4[4]+'/ks'
        else:
            self.posledna_objednavka_Z = 'chyba v subore STATISTIKY alebo CENNIK v produkte '+k
            self.posledna_objednavka_F = 'chyba v subore STATISTIKY alebo CENNIK v produkte '+k

        self.top_ten_graf = sorted(
            top_produkty, key=lambda x: x[1], reverse=True)
        self.top_ten_worst_graf = sorted(top_produkty, key=lambda x: x[1])
        self.top_ten_graf = self.top_ten_graf[:10]
        self.top_ten_worst_graf = self.top_ten_worst_graf[:10]
        a = 0
        while a < len(self.top_ten_graf):
            for k, v in self.tovar.items():
                if k == self.top_ten_graf[a][0]:
                    self.top_ten_graf[a][0] = v[0]
                    break
            a += 1

        self.top_ten = [i[1] for i in self.top_ten_graf]
        self.top_ten_worst = [i[1] for i in self.top_ten_worst_graf]

        self.najviac_sa_nakupuje = 'Sobota (87)'

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
        bar_X = [i for i in range(len(self.top_ten_graf))]
        bars1 = a1.bar(bar_X, self.top_ten)
        bar_X = []
        for bar in bars1:
            bar_X.append(bar.get_x())

        annot1 = a1.annotate("", xy=(0, 0), xytext=(0, 10), textcoords='offset points', ha='center', color='white', size=15,
                             bbox=dict(boxstyle="round", fc='#2F3E46', alpha=1, ec="#101416", lw=2))
        annot1.set_visible(False)

        def update_annot1(event, bar_x_pos):
            x = event.xdata
            y = event.ydata
            annot1.xy = (x, y)
            for c, i in enumerate(bar_X):
                if i == bar_x_pos:
                    text = self.top_ten_graf[c][0]+' ' + \
                        str(self.top_ten_graf[c][1])+'ks'
            annot1.set_text(text)

        def hover1(event):
            vis = annot1.get_visible()
            if event.inaxes == a1:
                for bar in bars1:
                    bar_x_pos = bar.get_x()
                    cont = bar.contains(event)
                    if cont[0]:
                        update_annot1(event, bar_x_pos)
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
        bar_X = [i for i in range(len(self.top_ten_worst_graf))]
        bars2 = a2.bar(bar_X, self.top_ten_worst)
        bar_X = []
        for bar in bars2:
            bar_X.append(bar.get_x())

        annot2 = a2.annotate("", xy=(0, 0), xytext=(0, 10), textcoords='offset points', ha='center', color='white', size=15,
                             bbox=dict(boxstyle="round", fc='#2F3E46', alpha=1, ec="#101416", lw=2))
        annot2.set_visible(False)

        def update_annot2(event, bar_x_pos):
            x = event.xdata
            y = event.ydata
            annot2.xy = (x, y)
            for c, i in enumerate(bar_X):
                if i == bar_x_pos:
                    text = self.top_ten_worst_graf[c][0]
            annot2.set_text(text)

        def hover2(event):
            vis = annot2.get_visible()
            if event.inaxes == a2:
                for bar in bars2:
                    bar_x_pos = bar.get_x()
                    cont = bar.contains(event)
                    if cont[0]:
                        update_annot2(event, bar_x_pos)
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

        def set_cross_hair_visible(visible):
            need_redraw = horizontal_line.get_visible() != visible
            horizontal_line.set_visible(visible)
            horizontal_line1.set_visible(visible)
            vertical_line.set_visible(visible)
            text.set_visible(visible)
            return need_redraw

        def on_mouse_move(event):
            if not event.inaxes:
                self.last_index = None
                need_redraw = set_cross_hair_visible(False)
                if need_redraw:
                    a3.figure.canvas.draw()
            else:
                set_cross_hair_visible(True)
                x1 = event.xdata
                index = min(np.searchsorted(x_axis, x1), len(x) - 1)
                if index == self.last_index:
                    return
                self.last_index = index

                vertical_line.set_xdata(x[index])
                horizontal_line.set_ydata(y[index])
                horizontal_line1.set_ydata(z[index])
                text.set_text('Dátum = %s\namount = %s' %
                              (self.x_date[index], y[index]))
                a3.figure.canvas.draw()

        vyvoj_ceny, a3 = plt.subplots(
            figsize=[7.18, 3.21], linewidth=self.linewidth, edgecolor=self.edgecolor)
        vyvoj_ceny.set_facecolor(self.graph_color)
        a3.set_facecolor(self.graph_color)
        a3.spines['top'].set_visible(False)
        a3.spines['right'].set_visible(False)
        a3.set_title('Vyvoj ceny', **self.font, fontsize=15,
                     weight='bold')
        line, = a3.plot(self.x_date, self.profit_all, label='vynosy')
        line1, = a3.plot(self.x_date, self.loss_all, label='naklady')
        a3.legend(loc='upper left', frameon=False)
        horizontal_line = a3.axhline(color='k', lw=0.8, ls='--')
        horizontal_line1 = a3.axhline(color='k', lw=0.8, ls='--')
        vertical_line = a3.axvline(color='k', lw=0.8, ls='--')
        x, y = line.get_data()
        x, z = line1.get_data()
        x_axis = [i for i in range(len(self.x_date))]
        self.last_index = None
        text = a3.text(0.8, 0.9, '', transform=a3.transAxes)
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
        self.ui.label_20.setText(str(self.avPrice)+'€')
        self.ui.label_20.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_10.setText(str(self.pocet_produktov))
        self.ui.label_10.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_12.setText(str(self.najviac_sa_nakupuje))
        self.ui.label_12.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_16.setText(str(self.najviac_produkt))
        self.ui.label_16.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_14.setText(str(self.posledna_objednavka_Z))
        self.ui.label_14.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_3.setText(str(self.posledna_objednavka_F))
        self.ui.label_3.setStyleSheet('color:'+self.funFactsColor)
        self.ui.camelLogo_2.setToolTip('')
