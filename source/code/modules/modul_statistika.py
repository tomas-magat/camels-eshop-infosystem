from utils.ui_commands import UI_Commands
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QGraphicsScene
from utils.tools import find_image
import datetime


class Statistika:

    def __init__(self, ui, data):
        self.ui = ui
        self.commands = UI_Commands(self.ui)
        self.data = data

        # Track button clicks
        self.commands.button_click(
            self.ui.statistikaButton, self.switch_screen)

        self.statistiky = self.data['statistiky'].data_list
        self.tovar = self.data['tovar'].data_list
        self.sklad = self.data['sklad'].data_list
        self.cennik = self.data['cennik'].data_list
        self.font = {'fontname': 'Arial'}
        self.edgecolor = '#CAD2C5'
        self.linewidth = 2
        self.graph_color = '#CAD2C5'
        self.funFactsColor = '#2C57D8'

        self.data['statistiky'].version_changed(self.reload, dict_data=False)
        # find_image('tricko.jpg')
        self.reload(self.statistiky)

        self.commands.date_changed(
            [self.ui.dateFrom, self.ui.dateTo], lambda x: x
        )

    def reload(self, data_list):
        self.statistiky = data_list
        self.Values()
        self.NajviacGraf()
        self.NajmenejGraf()
        self.VyvojGrafVsetky()
        self.FunFacts()

    def switch_screen(self):
        """Redirect to this statistika screen."""
        self.commands.redirect(self.ui.statistika)

    def Values(self):
        if self.sklad:
            self.celkovy_pocet_produktov_na_sklade = 0
            self.najviac_mame_produkt = 0
        else:
            self.celkovy_pocet_produktov_na_sklade = 'ziadne data v SKLAD.txt'
            self.najviac_mame_produkt = 'ziadne data v SKLAD.txt'
        self.top_ten_graf = [0]
        self.top_ten = 0
        self.top_ten_worst_graf = [0]
        self.top_ten_worst = 0
        if self.statistiky:
            self.avPrice = 0
        else:
            self.avPrice = 'ziadne data v STATISTIKY.txt'
        self.posledna_objednavka_P = 'ziadna'
        self.posledna_objednavka_N = 'ziadna'
        self.profLoss = 0

        self.najviac_sa_nakupuje = 'Sobota (87)'

        najviac_produkt = 0
        for produkt_sklad in self.sklad:
            self.celkovy_pocet_produktov_na_sklade += int(produkt_sklad[1])
            if najviac_produkt == int(produkt_sklad[1]):
                self.najviac_mame_produkt += produkt_sklad,
            elif najviac_produkt < int(produkt_sklad[1]):
                self.najviac_mame_produkt = produkt_sklad,
                najviac_produkt = int(produkt_sklad[1])

        statistiky_tricka = [1]
        statistiky_topanky = [3]
        statistiky_mikiny = [4]
        statistiky_nohavice = [2]
        statistiky_doplnky = [5]
        top_produkty = [[0, 0]]
        ttt = 0
        if self.statistiky:
            for objednavka in self.statistiky:
                m = 0
                if objednavka[1] == 'P':
                    for i in range(len(top_produkty)):
                        if objednavka[3] == top_produkty[i][0]:
                            top_produkty[i][1] += 1
                            m = 1
                            break
                    if m == 0:
                        top_produkty.append([objednavka[3], 1])
                    self.avPrice += int(objednavka[4])*float(objednavka[5])
                    ttt += 1
                    self.posledna_objednavka_P = objednavka
                else:
                    self.posledna_objednavka_N = objednavka
                if objednavka[3][0] == str(statistiky_tricka[0]):
                    statistiky_tricka += objednavka,
                elif objednavka[3][0] == str(statistiky_topanky[0]):
                    statistiky_topanky += objednavka,
                elif objednavka[3][0] == str(statistiky_mikiny[0]):
                    statistiky_mikiny += objednavka,
                elif objednavka[3][0] == str(statistiky_nohavice[0]):
                    statistiky_nohavice += objednavka,
                elif objednavka[3][0] == str(statistiky_doplnky[0]):
                    statistiky_doplnky += objednavka,
                else:
                    print('chyba v kode produktu -', objednavka)

            if ttt != 0:
                self.avPrice /= ttt
                self.avPrice = str(round(self.avPrice, 2))+'€'

            statistiky_tricka.pop(0)
            statistiky_topanky.pop(0)
            statistiky_mikiny.pop(0)
            statistiky_nohavice.pop(0)
            statistiky_doplnky.pop(0)

            statistiky_prof_loss1 = self.statistiky[-1]
            statistiky_prof_loss = []
            for i in reversed(self.statistiky):
                if i[0].split()[0] == statistiky_prof_loss1[0].split()[0]:
                    statistiky_prof_loss += i,
                else:
                    break

            for i in statistiky_prof_loss:
                if i[1] == 'P':
                    self.profLoss += int(i[4])*float(i[5])
                else:
                    self.profLoss -= int(i[4])*float(i[5])
            self.profLoss = round(self.profLoss, 2)

        top_produkty.remove([0, 0])
        self.top_ten_graf = sorted(
            top_produkty, key=lambda x: x[1], reverse=True)
        self.top_ten_graf = self.top_ten_graf[:10]
        self.top_ten = [i[1] for i in self.top_ten_graf]

        self.top_ten_worst_graf = sorted(
            top_produkty, key=lambda x: x[1])
        self.top_ten_worst_graf = self.top_ten_worst_graf[:10]
        self.top_ten_worst = [i[1] for i in self.top_ten_worst_graf]

        if len(top_produkty) != len(self.sklad):
            product_worst = []
            product_non = []
            product_non_index = []
            for product_worst_i in top_produkty:
                product_worst += product_worst_i[0],
            for product_sklad in self.sklad:
                if product_sklad[0] not in product_worst:
                    product_non += [product_sklad[0], 0],
                    product_non_index += 0.5,
            self.top_ten_worst = (product_non_index + self.top_ten_worst)[:10]
            self.top_ten_worst_graf = (
                product_non + self.top_ten_worst_graf)[:10]

        for produkt_tovar in self.tovar:
            for i in range(len(self.top_ten_graf)):
                if produkt_tovar[0] == self.top_ten_graf[i][0]:
                    self.top_ten_graf[i][0] = produkt_tovar[1]

            for i in range(len(self.top_ten_worst_graf)):
                if produkt_tovar[0] == self.top_ten_worst_graf[i][0]:
                    self.top_ten_worst_graf[i][0] = produkt_tovar[1]

            if self.najviac_mame_produkt != 0:
                for i in range(len(self.najviac_mame_produkt)):
                    if self.najviac_mame_produkt[i][0] == produkt_tovar[0]:
                        self.najviac_mame_produkt[i][0] = produkt_tovar[1]

            if produkt_tovar[0] == self.posledna_objednavka_N[3]:
                self.posledna_objednavka_N[3] = produkt_tovar[1]

            if produkt_tovar[0] == self.posledna_objednavka_P[3]:
                self.posledna_objednavka_P[3] = produkt_tovar[1]

        if self.sklad and self.najviac_mame_produkt != 0:
            nove_produkty = str(self.najviac_mame_produkt[0][1])+' ks'
            for i in self.najviac_mame_produkt:
                nove_produkty += '\n'+i[0]
            self.najviac_mame_produkt = nove_produkty

        if self.posledna_objednavka_N != 'ziadna':
            # self.posledna_objednavka_N[0] = self.posledna_objednavka_N[0].split()[0].split('-')[2] +'-'+ \
            #     self.posledna_objednavka_N[0].split()[0].split('-')[1]+'-'+self.posledna_objednavka_N[0].split()[0].split('-')[0] + \
            #     ' '+self.posledna_objednavka_N[0].split()[1]

            self.posledna_objednavka_N = self.posledna_objednavka_N[0].split()[0].replace('-', '.')+' ' + \
                self.posledna_objednavka_N[0].split()[1].replace('-', ':')+'\n'+self.posledna_objednavka_N[3]+'\n' + \
                self.posledna_objednavka_N[4]+'ks'+';' + \
                self.posledna_objednavka_N[5]+'€/ks'

        if self.posledna_objednavka_P != 'ziadna':
            # self.posledna_objednavka_P[0] = self.posledna_objednavka_P[0].split()[0].split('-')[2] +'-'+ \
            #     self.posledna_objednavka_P[0].split()[0].split('-')[1]+'-'+self.posledna_objednavka_P[0].split()[0].split('-')[0] + \
            #     ' '+self.posledna_objednavka_P[0].split()[1]

            self.posledna_objednavka_P = self.posledna_objednavka_P[0].split()[0].replace('-', '.')+' ' + \
                self.posledna_objednavka_P[0].split()[1].replace('-', ':')+'\n'+self.posledna_objednavka_P[3]+'\n' + \
                self.posledna_objednavka_P[4]+'ks'+';' + \
                self.posledna_objednavka_P[5]+'€/ks'

        if self.statistiky:
            self.x_date_all = []
            self.price_graph_all = []
            self.commands.product_sorted_graph(
                self.statistiky, self.x_date_all, self.price_graph_all)

        # if statistiky_tricka:
        #     self.x_date_tricka = []
        #     self.price_graph_tricka= []
        #     self.commands.product_sorted_graph(
        #         statistiky_tricka, self.x_date_tricka, self.price_graph_tricka)

        # if statistiky_topanky:
        #     self.x_date_topanky = []
        #     self.price_graph_topanky = []
        #     self.commands.product_sorted_graph(
        #         statistiky_topanky, self.x_date_topanky, self.price_graph_topanky)

        # if statistiky_mikiny:
        #     self.x_date_mikiny = []
        #     self.price_graph_mikiny = []
        #     self.commands.product_sorted_graph(
        #         statistiky_mikiny, self.x_date_mikiny, self.price_graph_mikiny)

        # if statistiky_nohavice:
        #     self.x_date_nohavice = []
        #     self.price_graph_nohavice = []
        #     self.commands.product_sorted_graph(
        #         statistiky_nohavice, self.x_date_nohavice, self.price_graph_nohavice)

        # if statistiky_doplnky:
        #     self.x_date_doplnky = []
        #     self.price_graph_doplnky = []
        #     self.commands.product_sorted_graph(
        #         statistiky_doplnky, self.x_date_doplnky, self.price_graph_doplnky)

    def NajviacGraf(self):
        if self.statistiky:
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
                        text_lomeno_n = ''
                        text_bez_lomeno_n = self.top_ten_graf[c][0].split()
                        for i in text_bez_lomeno_n:
                            text_lomeno_n += i+'\n'
                        if self.top_ten_graf[c][1] == 1:
                            objednavka_text = ' objednavka'
                        elif 1 < self.top_ten_graf[c][1] < 5:
                            objednavka_text = ' objednavky'
                        else:
                            objednavka_text = ' objednavok'
                        text = text_lomeno_n+' ' + \
                            str(self.top_ten_graf[c][1])+objednavka_text
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
        else:
            scene = QGraphicsScene()
            text = scene.addText('najpredavanejsie produkty')
            text.setPos(0, -50)
            scene.addText('ziadne data v STATISTIKY.txt')
            self.ui.najviacGraf.setScene(scene)

    def NajmenejGraf(self):
        if self.statistiky:
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
                        text_lomeno_n = ''
                        text_bez_lomeno_n = self.top_ten_worst_graf[c][0].split(
                        )
                        for i in text_bez_lomeno_n:
                            text_lomeno_n += i+'\n'
                        if self.top_ten_worst_graf[c][1] == 0.5:
                            objednavka_text = 'objednavok'
                        elif self.top_ten_worst_graf[c][1] == 1:
                            objednavka_text = ' objednavka'
                        elif 1 < self.top_ten_worst_graf[c][1] < 5:
                            objednavka_text = ' objednavky'
                        else:
                            objednavka_text = ' objednavok'
                        text = text_lomeno_n+' ' + \
                            str(self.top_ten_worst_graf[c][1])+objednavka_text
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
        else:
            scene = QGraphicsScene()
            text = scene.addText('nejmenej predavane produkty')
            text.setPos(0, -50)
            scene.addText('ziadne data v STATISTIKY.txt')
            self.ui.najmenejGraf.setScene(scene)

    def VyvojGrafVsetky(self):
        if self.statistiky:
            self.VyvojGraf(self.x_date_all, self.price_graph_all,
                           self.ui.trzbyNakladyVsetko)
            # self.VyvojGraf(self.x_date_tricka, self.price_graph_tricka, self.ui.trzbyNakladyTricka)
        #     self.VyvojGraf(self.x_date_topanky, self.price_graph_topanky, self.ui.trzbyNakladyTopanky)
        #     self.VyvojGraf(self.x_date_mikiny, self.price_graph_mikiny, self.ui.trzbyNakladyMikiny)
        #     self.VyvojGraf(self.x_date_nohavice, self.price_graph_nohavice, self.ui.trzbyNakladyNohavice)
        #     self.VyvojGraf(self.x_date_doplnky, self.price_graph_doplnky, self.ui.trzbyNakladyDoplnky)
        # else:
        #     scene = QGraphicsScene()
        #     scene.addText('ziadne data v STATISTIKY.txt')
        #     self.ui.trzbyNakladyVsetko.setScene(scene)
        #     self.ui.trzbyNakladyTricka.setScene(scene)
        #     self.ui.trzbyNakladyTopanky.setScene(scene)
        #     self.ui.trzbyNakladyMikiny.setScene(scene)
        #     self.ui.trzbyNakladyNohavice.setScene(scene)
        #     self.ui.trzbyNakladyDoplnky.setScene(scene)

    def VyvojGraf(self, x_date, price_graph, qtgraf):

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
                              (x_date[index], round(y[index], 2)))
                a3.figure.canvas.draw()

        vyvoj_ceny, a3 = plt.subplots(
            figsize=[7.18, 3.21], linewidth=self.linewidth, edgecolor=self.edgecolor)
        vyvoj_ceny.set_facecolor(self.graph_color)
        a3.set_facecolor(self.graph_color)
        a3.spines['top'].set_visible(False)
        a3.spines['right'].set_visible(False)
        a3.set_title('Vyvoj ceny', **self.font, fontsize=15,
                     weight='bold')
        line, = a3.plot(x_date, price_graph, label='vynosy')
        line1, = a3.plot(x_date, price_graph, label='naklady')
        a3.xaxis.set_major_locator(plt.MaxNLocator(5))
        # a3.legend(loc='upper left', frameon=False)
        horizontal_line = a3.axhline(color='k', lw=0.8, ls='--')
        horizontal_line1 = a3.axhline(color='k', lw=0.8, ls='--')
        vertical_line = a3.axvline(color='k', lw=0.8, ls='--')
        x, y = line.get_data()
        x, z = line1.get_data()
        x_axis = [i for i in range(len(x_date))]
        self.last_index = None
        text = a3.text(0.8, 0.9, '', transform=a3.transAxes)
        vyvoj_ceny.canvas.mpl_connect(
            'motion_notify_event', on_mouse_move)
        self.commands.plot_graph(qtgraf,
                                 vyvoj_ceny, size=68.5)

    def FunFacts(self):

        profLossColor = '#717171'
        if self.statistiky:
            if self.profLoss < 0:
                profLossColor = '#FF0000'
            elif self.profLoss > 0:
                profLossColor = '#21BF3E'

        self.ui.label_6.setText(str(self.profLoss)+'€')
        self.ui.label_6.setToolTip('''tato cena vyjadruje zisk alebo stratu firmy za jeden den
napriklad od 2000.1.1 0:00:00 - 2000.1.1 23:59:59
pre detailnejsie zobrazenie vyvoju ceny firmy pozri graf nizsie -->''')
        self.ui.label_6.setStyleSheet('''QToolTip {
                                        font-size:9pt;
                                        color:white;
                                        background-color: #2F3E46;
                                        border: 1px solid #101416;}
                                        #label_6 {color: %s}''' % profLossColor)
        self.ui.label_20.setText(str(self.avPrice))
        self.ui.label_20.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_10.setText(str(self.celkovy_pocet_produktov_na_sklade))
        self.ui.label_10.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_12.setText(str(self.najviac_sa_nakupuje))
        self.ui.label_12.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_16.setText(str(self.najviac_mame_produkt))
        self.ui.label_16.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_14.setText(str(self.posledna_objednavka_P))
        self.ui.label_14.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_3.setText(str(self.posledna_objednavka_N))
        self.ui.label_3.setStyleSheet('color:'+self.funFactsColor)
        self.ui.camelLogo_2.setToolTip('')
