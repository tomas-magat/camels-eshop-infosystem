# Secondary version of statistika module for debugging purposes
# must be moved to modules/ and added to __init__.py to work
from datetime import datetime

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

        self.graphs = []

        self.canvases = [
            self.ui.trzbyNakladyVsetko,
            self.ui.trzbyNakladyTricka,
            self.ui.trzbyNakladyTopanky,
            self.ui.trzbyNakladyMikiny,
            self.ui.trzbyNakladyNohavice,
            self.ui.trzbyNakladyDoplnky
        ]

        # Track button clicks
        self.commands.button_click(
            self.ui.statistikaButton, self.switch_screen
        )
        self.commands.tab_selected(
            self.ui.tabWidget, self.update_category
        )
        self.commands.date_changed(
            [self.ui.dateFrom, self.ui.dateTo], self.reload
        )

        self.init_data()

    def init_data(self):
        self.statistics = self.data['statistiky']
        self.goods = self.data['tovar']
        self.storage = self.data['sklad']
        self.statistics.version_changed(self.reload, dict_data=False)
        self.goods.version_changed(self.reload, dict_data=False)
        self.storage.version_changed(self.reload, dict_data=False)
        self.ui.tabWidget.setCurrentIndex(0)
        self.update_category()

    def init_stats(self):
        if len(self.statistics.data_list) > 0:
            self.display_total_money()
            self.most_buying()
            self.least_buying()
            self.load_graphs()
            self.fun_facts()
        else:
            self.no_data()

    def no_data(self):
        scene = QGraphicsScene()
        scene.addText('ziadne data v STATISTIKY.txt')
        self.ui.najviacGraf.setScene(scene)
        self.ui.najmenejGraf.setScene(scene)

        for canvas in self.canvases:
            canvas.setScene(scene)

    def update_category(self):
        self.category = self.ui.tabWidget.currentIndex()
        self.reload(self.statistics.data_list)

    def reload(self, data_list):
        for graph in self.graphs:
            plt.close(graph)
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
                if purchase[3] == code and purchase[1] == 'P':
                    counts[code] += 1

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
        self.graphs.append(top_10_graph)

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
        self.graphs.append(worst_10_graph)

    def load_data(self, category):
        return statistics_range(
            self.ui.dateFrom.dateTime().toPyDateTime(),
            self.ui.dateTo.dateTime().toPyDateTime(),
            category
        )

    def load_graphs(self):
        for category, canvas in enumerate(self.canvases):
            data = self.load_data(category)
            profits = {}
            for i in data:
                date = i[0].split()[0]
                if profits.get(date) == None:
                    profits[date] = [0, 0]

                if i[1] == 'P':
                    profits[date][0] += int(i[4])*float(i[5])
                else:
                    profits[date][1] += int(i[4])*float(i[5])

            self.profits_graph(
                [k.split()[0]+':'+str(i)
                 for i, k in enumerate(profits.keys())],
                [i[0] for i in profits.values()],
                [i[1] for i in profits.values()], canvas)

    def profits_graph(self, x_date, profit, loss, qtgraf):

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
                    profits_axes.figure.canvas.draw()
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
                profits_axes.figure.canvas.draw()

        vyvoj_ceny, profits_axes = plt.subplots(
            figsize=[7.18, 3.21], linewidth=self.linewidth, edgecolor=self.edge_color)
        vyvoj_ceny.set_facecolor(self.graph_color)

        profits_axes.set_facecolor(self.graph_color)
        profits_axes.spines['top'].set_visible(False)
        profits_axes.spines['right'].set_visible(False)
        profits_axes.set_title('Vyvoj ceny', **self.font, fontsize=15,
                               weight='bold')
        profits_axes.xaxis.set_major_locator(plt.MaxNLocator(3))

        line, = profits_axes.plot(x_date, profit, label='vynosy')
        line1, = profits_axes.plot(x_date, loss, label='naklady')

        profits_axes.legend(loc='upper left', frameon=False)
        horizontal_line = profits_axes.axhline(color='k', lw=0.8, ls='--')
        horizontal_line1 = profits_axes.axhline(color='k', lw=0.8, ls='--')
        vertical_line = profits_axes.axvline(color='k', lw=0.8, ls='--')
        x, y = line.get_data()
        x, z = line1.get_data()
        x_axis = [i for i in range(len(x_date))]
        self.last_index = None
        text = profits_axes.text(
            0.8, 0.9, '', transform=profits_axes.transAxes)
        vyvoj_ceny.canvas.mpl_connect(
            'motion_notify_event', on_mouse_move)

        self.commands.plot_graph(qtgraf, vyvoj_ceny, size=68.5)
        self.graphs.append(vyvoj_ceny)

    def get_facts(self):
        prices = [int(i[4])*float(i[5]) for i in self.statistics.data_list]
        self.avPrice = "%.2f" % (sum(prices) / len(prices)) + " €"

        days = [
            datetime.strptime(i[0], "%Y-%m-%d %H-%M-%S").strftime("%A")
            for i in self.statistics.data_list
        ]
        self.top_day = max(set(days), key=days.count)

        self.total_products = 0
        self.most_in_stock = ['', 0]
        for k, v in self.storage.data.items():
            if int(v[0]) > self.most_in_stock[1]:
                self.most_in_stock = [k, int(v[0])]
            self.total_products += int(v[0])

        self.most_in_stock = self.goods.data[self.most_in_stock[0]][0]

    def fun_facts(self):
        self.get_facts()
        self.ui.label_20.setText(str(self.avPrice))
        self.ui.label_20.setStyleSheet('color:'+self.facts_color)
        self.ui.label_10.setText(str(self.total_products))
        self.ui.label_10.setStyleSheet('color:'+self.facts_color)
        self.ui.label_12.setText(str(self.top_day))
        self.ui.label_12.setStyleSheet('color:'+self.facts_color)
        self.ui.label_16.setText(str(self.most_in_stock))
        self.ui.label_16.setStyleSheet('color:'+self.facts_color)
        self.ui.label_14.setText(';'.join(self.statistics.data_list[0]))
        self.ui.label_14.setStyleSheet('color:'+self.facts_color)
        self.ui.label_3.setText(';'.join(self.statistics.data_list[0]))
        self.ui.label_3.setStyleSheet('color:'+self.facts_color)
        self.ui.camelLogo_2.setToolTip('')
