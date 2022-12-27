import datetime

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QGraphicsScene

from utils.ui_commands import UI_Commands
from utils.tools import statistics_range


class Statistika:

    def __init__(self, ui, data):
        self.ui = ui
        self.commands = UI_Commands(self.ui)
        self.data = data

        self.font = {'fontname': 'Arial'}
        self.edge_color = '#CAD2C5'
        self.linewidth = 2
        self.graph_color = '#CAD2C5'
        self.facts_color = '#2C57D8'

        self.init_data()

        self.canvases = [
            self.ui.trzbyNakladyVsetko,
            self.ui.trzbyNakladyTricka,
            self.ui.trzbyNakladyTopanky,
            self.ui.trzbyNakladyMikiny,
            self.ui.trzbyNakladyNohavice,
            self.ui.trzbyNakladyDoplnky
        ]

        self.init_stats()

        # Track button clicks
        self.commands.button_click(
            self.ui.statistikaButton, self.switch_screen)

    def init_data(self):
        self.statistics = self.data['statistiky']
        self.goods = self.data['tovar']
        self.storage = self.data['sklad']
        self.statistics.version_changed(self.reload, dict_data=False)
        self.ui.tabWidget.setCurrentIndex(0)
        self.update_category()

    def init_stats(self):
        if len(self.statistics.data_list) > 0:
            self.display_total_money()
            self.most_buying()
            self.least_buying()
            # self.load_graphs()
            self.fun_facts()

    def update_category(self):
        self.category = self.ui.tabWidget.currentIndex()
        self.reload(self.statistics.data_list)

    def reload(self, data_list):
        self.init_stats()

    def switch_screen(self):
        """Redirect to this statistika screen."""
        self.commands.redirect(self.ui.statistika)

    def get_total_money(self):
        self.total_money = 0
        for purchase in self.statistics.data_list:
            purchase_price = int(purchase[4])*float(purchase[5])
            if purchase[1] == 'N':
                self.total_money -= purchase_price
            else:
                self.total_money += purchase_price

    def display_total_money(self):
        self.get_total_money()

        label_color = '#FF0000' if self.total_money < 0 else '#21BF3E'
        self.ui.label_6.setText(str(self.total_money)+' €')
        self.ui.label_6.setToolTip("Celkovy zisk alebo strata firmy")
        self.ui.label_6.setStyleSheet(
            """QToolTip {
                font-size:9pt;
                color:white;
                background-color: #2F3E46;
                border: 1px solid #101416;}
                #label_6 {color: %s}""" % label_color)

    def get_counts(self, most=True):
        counts = {}
        for code in self.goods.data.keys():
            counts[code] = 0
            for purchase in self.statistics.data_list:
                if purchase[3] == code:
                    counts[code] += int(purchase[4])

        result = []
        for code, count in counts.items():
            result.append([self.goods.data[code][0], count])

        return sorted(result, key=lambda x: x[1], reverse=most)[:10]

    def most_buying(self):
        top_10_graph, top_10_axes = plt.subplots(
            figsize=[4.9, 3.15], linewidth=2, edgecolor=self.edge_color)

        top_10_graph.patch.set_facecolor(self.graph_color)

        top_10_axes.set_facecolor(self.graph_color)
        top_10_axes.spines['top'].set_visible(False)
        top_10_axes.spines['right'].set_visible(False)
        top_10_axes.axes.xaxis.set_ticklabels([])
        top_10_axes.tick_params(axis='x', which='both', length=0)
        top_10_axes.set_title('Najpredavanejsie produkty', **
                              self.font, fontsize=15, weight='bold')

        x_vals = list(range(10))
        y_vals = self.get_counts()
        bar_graph = top_10_axes.bar(x_vals, [val[1] for val in y_vals])

        x_bars = []
        for bar in bar_graph:
            x_bars.append(bar.get_x())

        top_10_annot = top_10_axes.annotate(
            "", xy=(0, 0), xytext=(0, 10), textcoords='offset points',
            ha='center', color='white', size=15,
            bbox=dict(
                boxstyle="round", fc='#2F3E46', alpha=1,
                ec="#101416", lw=2)
        )
        top_10_annot.set_visible(False)

        def update_annotation(event, bar_x_pos):
            x = event.xdata
            y = event.ydata
            top_10_annot.xy = (x, y)
            for c, i in enumerate(x_bars):
                if i == bar_x_pos:
                    text = '\n'.join(y_vals[c][0].split())
                    text += '\n'+str(y_vals[c][1])
                    if y_vals[c][1] == 1:
                        text += ' kupeny'
                    elif 1 < y_vals[c][1] < 5:
                        text += ' kupene'
                    else:
                        text += ' kupenych'

            top_10_annot.set_text(text)

        def on_hover(event):
            vis = top_10_annot.get_visible()
            if event.inaxes == top_10_axes:
                for bar in bar_graph:
                    bar_x_pos = bar.get_x()
                    cont = bar.contains(event)
                    if cont[0]:
                        update_annotation(event, bar_x_pos)
                        top_10_annot.set_visible(True)
                        top_10_graph.canvas.draw_idle()
                        return
                    else:
                        if vis:
                            top_10_annot.set_visible(False)
                            top_10_graph.canvas.draw_idle()

        top_10_graph.canvas.mpl_connect("motion_notify_event", on_hover)
        self.commands.plot_graph(self.ui.najviacGraf, top_10_graph)

    def least_buying(self):
        worst_10_graph, worst_10_axes = plt.subplots(
            figsize=[4.9, 3.15], linewidth=2, edgecolor=self.edge_color)

        worst_10_graph.patch.set_facecolor(self.graph_color)

        worst_10_axes.set_facecolor(self.graph_color)
        worst_10_axes.spines['top'].set_visible(False)
        worst_10_axes.spines['right'].set_visible(False)
        worst_10_axes.axes.xaxis.set_ticklabels([])
        worst_10_axes.tick_params(axis='x', which='both', length=0)
        worst_10_axes.set_title('Najmenej predavane produkty', **
                                self.font, fontsize=15, weight='bold')

        x_vals = list(range(10))
        y_vals = self.get_counts(most=False)
        bar_graph = worst_10_axes.bar(x_vals, [val[1] for val in y_vals])

        x_bars = []
        for bar in bar_graph:
            x_bars.append(bar.get_x())

        top_10_annot = worst_10_axes.annotate(
            "", xy=(0, 0), xytext=(0, 10), textcoords='offset points',
            ha='center', color='white', size=15,
            bbox=dict(
                boxstyle="round", fc='#2F3E46', alpha=1,
                ec="#101416", lw=2)
        )
        top_10_annot.set_visible(False)

        def update_annotation(event, bar_x_pos):
            x = event.xdata
            y = event.ydata
            top_10_annot.xy = (x, y)
            for c, i in enumerate(x_bars):
                if i == bar_x_pos:
                    text = '\n'.join(y_vals[c][0].split())
                    text += '\n'+str(y_vals[c][1])
                    if y_vals[c][1] == 1:
                        text += ' kupeny'
                    elif 1 < y_vals[c][1] < 5:
                        text += ' kupene'
                    else:
                        text += ' kupenych'

            top_10_annot.set_text(text)

        def on_hover(event):
            vis = top_10_annot.get_visible()
            if event.inaxes == worst_10_axes:
                for bar in bar_graph:
                    bar_x_pos = bar.get_x()
                    cont = bar.contains(event)
                    if cont[0]:
                        update_annotation(event, bar_x_pos)
                        top_10_annot.set_visible(True)
                        worst_10_graph.canvas.draw_idle()
                        return
                    else:
                        if vis:
                            top_10_annot.set_visible(False)
                            worst_10_graph.canvas.draw_idle()

        worst_10_graph.canvas.mpl_connect("motion_notify_event", on_hover)
        self.commands.plot_graph(self.ui.najmenejGraf, worst_10_graph)


#     def load_graphs(self):
#         if self.statistics.data_list:
#             self.VyvojGraf(self.x_date, self.profit_all,
#                            self.loss_all, self.ui.trzbyNakladyVsetko)
#             self.VyvojGraf(self.x_date_tricka, self.profit_tricka,
#                            self.loss_tricka, self.ui.trzbyNakladyTricka)
#             self.VyvojGraf(self.x_date_topanky, self.profit_topanky,
#                            self.loss_topanky, self.ui.trzbyNakladyTopanky)
#             self.VyvojGraf(self.x_date_mikiny, self.profit_mikiny,
#                            self.loss_mikiny, self.ui.trzbyNakladyMikiny)
#             self.VyvojGraf(self.x_date_nohavice, self.profit_nohavice,
#                            self.loss_nohavice, self.ui.trzbyNakladyNohavice)
#             self.VyvojGraf(self.x_date_doplnky, self.profit_doplnky,
#                            self.loss_doplnky, self.ui.trzbyNakladyDoplnky)
#         else:
#             scene = QGraphicsScene()
#             scene.addText('ziadne data v STATISTIKY.txt')
#             self.ui.trzbyNakladyVsetko.setScene(scene)
#             self.ui.trzbyNakladyTricka.setScene(scene)
#             self.ui.trzbyNakladyTopanky.setScene(scene)
#             self.ui.trzbyNakladyMikiny.setScene(scene)
#             self.ui.trzbyNakladyNohavice.setScene(scene)
#             self.ui.trzbyNakladyDoplnky.setScene(scene)

#     def VyvojGraf(self, x_date, profit, loss, qtgraf):

#         def set_cross_hair_visible(visible):
#             need_redraw = horizontal_line.get_visible() != visible
#             horizontal_line.set_visible(visible)
#             horizontal_line1.set_visible(visible)
#             vertical_line.set_visible(visible)
#             text.set_visible(visible)
#             return need_redraw

#         def on_mouse_move(event):
#             if not event.inaxes:
#                 self.last_index = None
#                 need_redraw = set_cross_hair_visible(False)
#                 if need_redraw:
#                     a3.figure.canvas.draw()
#             else:
#                 set_cross_hair_visible(True)
#                 x1 = event.xdata
#                 index = min(np.searchsorted(x_axis, x1), len(x) - 1)
#                 if index == self.last_index:
#                     return
#                 self.last_index = index

#                 vertical_line.set_xdata(x[index])
#                 horizontal_line.set_ydata(y[index])
#                 horizontal_line1.set_ydata(z[index])
#                 text.set_text('Dátum = %s\namount = %s' %
#                               (x_date[index], round(y[index], 2)))
#                 a3.figure.canvas.draw()

#         vyvoj_ceny, a3 = plt.subplots(
#             figsize=[7.18, 3.21], linewidth=self.linewidth, edge_color=self.edge_color)
#         vyvoj_ceny.set_facecolor(self.graph_color)
#         a3.set_facecolor(self.graph_color)
#         a3.spines['top'].set_visible(False)
#         a3.spines['right'].set_visible(False)
#         a3.set_title('Vyvoj ceny', **self.font, fontsize=15,
#                      weight='bold')
#         line, = a3.plot(x_date, profit, label='vynosy')
#         line1, = a3.plot(x_date, loss, label='naklady')
#         a3.legend(loc='upper left', frameon=False)
#         horizontal_line = a3.axhline(color='k', lw=0.8, ls='--')
#         horizontal_line1 = a3.axhline(color='k', lw=0.8, ls='--')
#         vertical_line = a3.axvline(color='k', lw=0.8, ls='--')
#         x, y = line.get_data()
#         x, z = line1.get_data()
#         x_axis = [i for i in range(len(x_date))]
#         self.last_index = None
#         text = a3.text(0.8, 0.9, '', transform=a3.transAxes)
#         vyvoj_ceny.canvas.mpl_connect(
#             'motion_notify_event', on_mouse_move)
#         self.commands.plot_graph(qtgraf,
#                                  vyvoj_ceny, size=68.5)
#         plt.tight_layout()

#     def fun_facts(self):

#         profLossColor = '#717171'
#         if self.statistics.data_list:
#             if self.profLoss < 0:
#                 profLossColor = '#FF0000'
#             elif self.profLoss > 0:
#                 profLossColor = '#21BF3E'

#         self.ui.label_6.setText(str(self.profLoss)+'€')
#         self.ui.label_6.setToolTip('''tato cena vyjadruje zisk alebo stratu firmy za jeden den
# napriklad od 2000.1.1 0:00:00 - 2000.1.1 23:59:59
# pre detailnejsie zobrazenie vyvoju ceny firmy pozri graf nizsie -->''')
#         self.ui.label_6.setStyleSheet('''QToolTip {
#                                         font-size:9pt;
#                                         color:white;
#                                         background-color: #2F3E46;
#                                         border: 1px solid #101416;}
#                                         #label_6 {color: %s}''' % profLossColor)
#         self.ui.label_20.setText(str(self.avPrice))
#         self.ui.label_20.setStyleSheet('color:'+self.facts_color)
#         self.ui.label_10.setText(str(self.celkovy_pocet_produktov_na_sklade))
#         self.ui.label_10.setStyleSheet('color:'+self.facts_color)
#         self.ui.label_12.setText(str(self.top_10_graph_sa_nakupuje))
#         self.ui.label_12.setStyleSheet('color:'+self.facts_color)
#         self.ui.label_16.setText(str(self.top_10_graph_mame_produkt))
#         self.ui.label_16.setStyleSheet('color:'+self.facts_color)
#         self.ui.label_14.setText(str(self.posledna_objednavka_P))
#         self.ui.label_14.setStyleSheet('color:'+self.facts_color)
#         self.ui.label_3.setText(str(self.posledna_objednavka_N))
#         self.ui.label_3.setStyleSheet('color:'+self.facts_color)
#         self.ui.camelLogo_2.setToolTip('')

    def fun_facts(self):
        pass
        # if self.sklad:
        #     self.celkovy_pocet_produktov_na_sklade = 0
        #     self.top_10_graph_mame_produkt = 0
        # else:
        #     self.celkovy_pocet_produktov_na_sklade = 'ziadne data v SKLAD.txt'
        #     self.top_10_graph_mame_produkt = 'ziadne data v SKLAD.txt'
        # self.top_ten_graf = [0]
        # self.top_ten = 0
        # self.top_ten_worst_graf = [0]
        # self.top_ten_worst = 0
        # if self.statistics.data_list:
        #     self.avPrice = 0
        # else:
        #     self.avPrice = 'ziadne data v STATISTIKY.txt'
        # self.posledna_objednavka_P = 'ziadna'
        # self.posledna_objednavka_N = 'ziadna'
        # self.profLoss = 0

        # self.top_10_graph_sa_nakupuje = 'Sobota (87)'

        # top_10_graph_produkt = 0
        # for produkt_sklad in self.sklad:
        #     self.celkovy_pocet_produktov_na_sklade += int(produkt_sklad[1])
        #     if top_10_graph_produkt == int(produkt_sklad[1]):
        #         self.top_10_graph_mame_produkt += produkt_sklad,
        #     elif top_10_graph_produkt < int(produkt_sklad[1]):
        #         self.top_10_graph_mame_produkt = produkt_sklad,
        #         top_10_graph_produkt = int(produkt_sklad[1])

        # top_produkty = [[0, 0]]
        # ttt = 0
        # self.statistics.data_list_list = []
        # if self.statistics.data_list:
        #     for objednavka in self.statistics.data_list:
        #         m = 0
        #         if objednavka[1] == 'P':
        #             for i in range(len(top_produkty)):
        #                 if objednavka[3] == top_produkty[i][0]:
        #                     top_produkty[i][1] += 1
        #                     m = 1
        #                     break
        #             if m == 0:
        #                 top_produkty.append([objednavka[3], 1])
        #             self.avPrice += int(objednavka[4])*float(objednavka[5])
        #             ttt += 1
        #             self.posledna_objednavka_P = objednavka
        #         else:
        #             self.posledna_objednavka_N = objednavka
        #         self.statistics.data_list_list += objednavka,
        #     self.avPrice /= ttt
        #     self.avPrice = str(round(self.avPrice, 2))+'€'

        #     self.statistics.data_list_prof_loss1 = self.statistics.data_list_list[-1]
        #     self.statistics.data_list_prof_loss = []
        #     for i in reversed(self.statistics.data_list_list):
        #         if i[0].split()[0] == self.statistics.data_list_prof_loss1[0].split()[0]:
        #             self.statistics.data_list_prof_loss += i,
        #         else:
        #             break

        #     for i in self.statistics.data_list_prof_loss:
        #         if i[1] == 'P':
        #             self.profLoss += int(i[4])*float(i[5])
        #         else:
        #             self.profLoss -= int(i[4])*float(i[5])
        #     self.profLoss = round(self.profLoss, 2)

        # self.statistics.data_list_tricka = [1]
        # self.statistics.data_list_topanky = [3]
        # self.statistics.data_list_mikiny = [4]
        # self.statistics.data_list_nohavice = [2]
        # self.statistics.data_list_doplnky = [5]
        # for i in sorted(self.statistics.data_list_list, key=lambda x: x[3]):
        #     if i[3][0] == str(self.statistics.data_list_tricka[0]):
        #         self.statistics.data_lisself.self.xt_tricka += i,
        #     elif i[3][0] == str(self.statistics.data_list_nohavice[0]):
        #         self.statistics.data_list_nohavice += i,
        #     elif i[3][0] == str(self.statistics.data_list_topanky[0]):
        #         self.statistics.data_list_topanky += i,
        #     elif i[3][0] == str(self.statistics.data_list_mikiny[0]):
        #         self.self.xstatistics.data_list_mikiny += i,
        #     elif i[3][0] == str(self.self.xstatistics.data_list_doplnky[0]):
        #         self.self.xstatistics.data_list_doplnky += i,
        #     else:
        #         print('chyba v kode produktu'+str(i))
        # self.self.xstatistics.data_list_tricka.pop(0)
        # self.self.xstatistics.data_list_topanky.pop(0)
        # self.self.xstatistics.data_list_mikiny.pop(0)
        # self.self.xstatistics.data_list_nohavice.pop(0)
        # self.self.xstatistics.data_list_doplnky.pop(0)

        # top_produkty.remove([0, 0])
        # self.top_ten_graf = sorted(
        #     top_produkty, key=lambda x: x[1], reverse=True)
        # self.top_ten_graf = self.top_ten_graf[:10]
        # self.top_ten = [i[1] for i in self.top_ten_graf]

        # self.top_ten_worst_graf = sorted(top_produkty, key=lambda x: x[1])
        # self.top_ten_worst_graf = self.top_ten_worst_graf[:10]
        # self.top_ten_worst = [i[1] for i in self.top_ten_worst_graf]

        # for produkt_tovar in self.tovar:
        #     for i in range(len(self.top_ten_graf)):
        #         if produkt_tovar[0] == self.top_ten_graf[i][0]:
        #             self.top_ten_graf[i][0] = produkt_tovar[1]

        #     for i in range(len(self.top_ten_worst_graf)):
        #         if produkt_tovar[0] == self.top_ten_worst_graf[i][0]:
        #             self.top_ten_worst_graf[i][0] = produkt_tovar[1]

        #     if self.top_10_graph_mame_produkt != 0:
        #         for i in range(len(self.top_10_graph_mame_produkt)):
        #             if self.top_10_graph_mame_produkt[i][0] == produkt_tovar[0]:
        #                 self.top_10_graph_mame_produkt[i][0] = produkt_tovar[1]

        #     if produkt_tovar[0] == self.posledna_objednavka_N[3]:
        #         self.posledna_objednavka_N[3] = produkt_tovar[1]

        #     if produkt_tovar[0] == self.posledna_objednavka_P[3]:
        #         self.posledna_objednavka_P[3] = produkt_tovar[1]

        # if self.sklad and self.top_10_graph_mame_produkt != 0:
        #     nove_produkty = str(self.top_10_graph_mame_produkt[0][1])+' ks'
        #     for i in self.top_10_graph_mame_produkt:
        #         nove_produkty += '\n'+i[0]
        #     self.top_10_graph_mame_produkt = nove_produkty

        # if self.statistics.data_list:
        #     self.posledna_objednavka_N = self.posledna_objednavka_N[0].split()[0].replace('-', '.')+' ' + \
        #         self.posledna_objednavka_N[0].split()[1].replace('-', ':')+';'+self.posledna_objednavka_N[3]+';' + \
        #         self.posledna_objednavka_N[4]+'ks'+';' + \
        #         self.posledna_objednavka_N[5]+'€/ks'

        #     self.posledna_objednavka_P = self.posledna_objednavka_P[0].split()[0].replace('-', '.')+' ' + \
        #         self.posledna_objednavka_P[0].split()[1].replace('-', ':')+';'+self.posledna_objednavka_P[3]+';' + \
        #         self.posledna_objednavka_P[4]+'ks'+';' + \
        #         self.posledna_objednavka_P[5]+'€/ks'

        # self.x_date = []
        # self.profit_all = [0]
        # self.loss_all = [0]
        # self.commands.product_sorted_graph(
        #     self.xstatistics.data_list_list, self.x_date, self.profit_all, self.loss_all)

        # self.x_date_tricka = []
        # self.profit_tricka = [0]
        # self.loss_tricka = [0]
        # self.commands.product_sorted_graph(
        #     self.xstatistics.data_list_tricka, self.x_date_tricka, self.profit_tricka, self.loss_tricka)

        # self.x_date_topanky = []
        # self.profit_topanky = [0]
        # self.loss_topanky = [0]
        # self.commands.product_sorted_graph(
        #     self.xstatistics.data_list_topanky, self.x_date_topanky, self.profit_topanky, self.loss_topanky)

        # self.x_date_mikiny = []
        # self.profit_mikiny = [0]
        # self.loss_mikiny = [0]
        # self.commands.product_sorted_graph(
        #     self.statistics.data_list_mikiny, self.x_date_mikiny, self.profit_mikiny, self.loss_mikiny)

        # self.x_date_nohavice = []
        # self.profit_nohavice = [0]
        # self.loss_nohavice = [0]
        # self.commands.product_sorted_graph(
        #     self.statistics.data_list_nohavice, self.x_date_nohavice, self.profit_nohavice, self.loss_nohavice)

        # self.x_date_doplnky = []
        # self.profit_doplnky = [0]
        # self.loss_doplnky = [0]
        # self.commands.product_sorted_graph(
        #     self.statistics.data_list_doplnky, self.x_date_doplnky, self.profit_doplnky, self.loss_doplnky)
