import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QGraphicsScene
import datetime
from PyQt5.QtCore import QTimer

class Statistika:

    def __init__(self, app):

        self.ui = app.ui
        self.commands = app.commands
        self.data = app.data

        self.init_data()
        self.init_variables()
        self.init_changed()

    def init_data(self):

        # Create variables from files
        self.statistiky = self.data['statistiky'].data_list
        self.tovar = self.data['tovar'].data_list
        self.sklad = self.data['sklad'].data_list
        self.cennik = self.data['cennik'].data_list

    def init_changed(self):

        # Track button clicks
        self.commands.button_click(
            self.ui.statistikaButton, self.switch_screen)

        # Track date button clicks
        self.commands.button_click(
            self.ui.pushButton_2, self.reload_graph_date)
        if self.statistiky:
            self.ui.dateFrom.setDate(self.first_day)
            self.ui.dateTo.setDate(datetime.date.today())

        # Track version changed
        self.data['statistiky'].version_changed(
            self.reload_statistiky, dict_data=False)
        self.data['tovar'].version_changed(
            self.reload_tovar)
        self.reload_statistiky(self.statistiky)

        # Track info button clicks
        self.commands.button_click(
            self.ui.pushButton_3, self.show_hide_info)

    def init_variables(self):

        # Create variables needed later
        self.font = {'fontname': 'Arial'}
        self.edgecolor = '#CAD2C5'
        self.linewidth = 2
        self.graph_color = '#CAD2C5'
        self.funFactsColor = '#2C57D8'
        self.list_kategorie = [
            self.ui.trzbyNakladyVsetko,        
            self.ui.trzbyNakladyTricka,
            self.ui.trzbyNakladyTopanky,
            self.ui.trzbyNakladyMikiny,
            self.ui.trzbyNakladyNohavice,
            self.ui.trzbyNakladyDoplnky,
        ]
        if self.statistiky:
            self.first_day = datetime.datetime.strptime(
                self.statistiky[0][0].split()[0], '%Y-%m-%d').date()
            self.last_day = datetime.datetime.strptime(
                self.statistiky[-1][0].split()[0], '%Y-%m-%d').date()

    def reload_statistiky(self, data_list):
        
        # Reload necessary definitions
        self.statistiky = data_list
        self.sklad = self.data['sklad'].data_list
        self.commands.close_all_graphs()
        self.Values()
        self.sklad_loop()
        self.statistiky_loop()
        self.prof_loss_current_day()
        self.top_products()
        self.best_selling_day()
        self.tovar_loop()
        self.NajviacGraf()
        self.NajmenejGraf()
        self.reload_graph_date()
        self.zisk_firmy_color()
        self.FunFacts()

    def reload_tovar(self, data_dict):

        # Reload necessary definitions
        self.tovar = self.data['tovar'].data_list
        self.commands.close_najviac_najmenej_graphs()
        self.top_products()
        self.tovar_loop()
        self.NajviacGraf()
        self.NajmenejGraf()
        self.FunFacts()

    def switch_screen(self):

        # Redirect to this statistika screen
        self.commands.redirect(self.ui.statistika)
    
    def show_hide_info(self):

        # First press shows the info
        # second press hides the info
        if self.ui.label_18.isHidden():
            self.ui.label_18.setHidden(False)
        else:
            self.ui.label_18.setHidden(True)


    def reload_graph_date(self):

        # Create new statistika variable
        # based on new date changed
        self.ui.pushButton_2.setEnabled(False)
        QTimer.singleShot(
            500, lambda: self.ui.pushButton_2.setDisabled(False))
        self.date_from = self.ui.dateFrom.date().toPyDate()
        self.date_to = self.ui.dateTo.date().toPyDate()
        if self.date_from <= self.date_to:
            new_statistiky_data = []
            if self.statistiky:
                for i in self.statistiky:
                    date_time = datetime.datetime.strptime(
                        i[0].split()[0], '%Y-%m-%d').date()
                    if date_time >= self.date_from and date_time <= self.date_to:
                        new_statistiky_data += i,
            if new_statistiky_data:
                self.change_graph_date(new_statistiky_data)
            else:
                scene = QGraphicsScene()
                scene.addText(
                    'Žiadne dáta v STATISTIKY.txt v tomto rozmedzí dátumov')
                for i in self.list_kategorie:
                    i.setScene(scene)
                self.ui.label_17.setText('--')
                self.ui.label_17.setStyleSheet('color: #717171')

        else:
            scene = QGraphicsScene()
            scene.addText('Dátum ''DO'' musí byť väčší než dátum ''OD''')
            for i in self.list_kategorie:
                    i.setScene(scene)
            self.ui.label_17.setText('--')
            self.ui.label_17.setStyleSheet('color: #717171')

    def change_graph_date(self, new_statistiky_data):

        # Reload graph zisk
        # firmy based on new
        # statistiky data
        statistiky_tricka = [1]
        statistiky_topanky = [3]
        statistiky_mikiny = [4]
        statistiky_nohavice = [2]
        statistiky_doplnky = [5]
        self.zisk_firmy_za_obdobie = 0
        for objednavka in new_statistiky_data:
            if objednavka[1] == 'P':
                self.zisk_firmy_za_obdobie += int(objednavka[4])*float(
                                                                objednavka[5])
            else:
                self.zisk_firmy_za_obdobie -= int(objednavka[4])*float(
                                                                objednavka[5])
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

        statistiky_tricka.pop(0)
        statistiky_topanky.pop(0)
        statistiky_mikiny.pop(0)
        statistiky_nohavice.pop(0)
        statistiky_doplnky.pop(0)

        self.x_date_all = []
        self.price_graph_all = []
        self.date_info_all = [[]]
        if new_statistiky_data:
            self.product_sorted_graph(
                new_statistiky_data, self.x_date_all,
                self.price_graph_all, self.date_info_all)

        self.x_date_tricka = []
        self.price_graph_tricka = []
        self.date_info_tricka = [[]]
        if statistiky_tricka:
            self.product_sorted_graph(
                statistiky_tricka, self.x_date_tricka,
                self.price_graph_tricka, self.date_info_tricka)

        self.x_date_topanky = []
        self.price_graph_topanky = []
        self.date_info_topanky = [[]]
        if statistiky_topanky:
            self.product_sorted_graph(
                statistiky_topanky, self.x_date_topanky,
                self.price_graph_topanky, self.date_info_topanky)

        self.x_date_mikiny = []
        self.price_graph_mikiny = []
        self.date_info_mikiny = [[]]
        if statistiky_mikiny:
            self.product_sorted_graph(
                statistiky_mikiny, self.x_date_mikiny,
                self.price_graph_mikiny, self.date_info_mikiny)

        self.x_date_nohavice = []
        self.price_graph_nohavice = []
        self.date_info_nohavice = [[]]
        if statistiky_nohavice:
            self.product_sorted_graph(
                statistiky_nohavice, self.x_date_nohavice,
                self.price_graph_nohavice, self.date_info_nohavice)

        self.x_date_doplnky = []
        self.price_graph_doplnky = []
        self.date_info_doplnky = [[]]
        if statistiky_doplnky:
            self.product_sorted_graph(
                statistiky_doplnky, self.x_date_doplnky,
                self.price_graph_doplnky, self.date_info_doplnky)

        self.commands.close_graph_vyvoj_ceny()
        self.VyvojGrafVsetky()
        self.zisk_firmy_color()
    
    def product_sorted_graph(self, main_list, x_date, price_graph, date_info):

        # Create 2 lists from statistiky.txt 
        # needed to plot the graph vyvoj_ceny
        deta = main_list[0][0].split()[0]
        x_date_unedited = [deta.split('-')]
        price_graph_unedited = [0]
        for i in main_list:
            split_date = i[0].split()
            if x_date_unedited[-1] != split_date[0].split('-'):
                x_date_unedited += split_date[0].split('-'),
                date_info += [i],
            else:
                date_info[-1] += [i]
            if split_date[0] == deta:
                if i[1] == 'N':
                    price_graph_unedited[-1] -= int(i[4])*float(i[5])
                else:
                    price_graph_unedited[-1] += int(i[4])*float(i[5])
            else:
                deta = split_date[0]
                if i[1] == 'N':
                    price_graph_unedited += price_graph_unedited[-1] -\
                        int(i[4])*float(i[5]),
                else:
                    price_graph_unedited += price_graph_unedited[-1] +\
                        int(i[4])*float(i[5]),
        for i in price_graph_unedited:
            price_graph += round(i, 2),
        for i in x_date_unedited:
            x_date += i[2]+'.'+i[1]+'.'+i[0][2:],
        b = 0
        for i in range(len(x_date_unedited)-1):
            d1 = datetime.date(
                int(x_date_unedited[i][0]),
                int(x_date_unedited[i][1]),
                int(x_date_unedited[i][2]))
            d2 = datetime.date(
                int(x_date_unedited[i+1][0]),
                int(x_date_unedited[i+1][1]),
                int(x_date_unedited[i+1][2]))
            x = x_date_unedited[i]
            y = x_date_unedited[i+1]
            price_connection = round(price_graph_unedited[i], 2)
            if x[0] == y[0] and x[1] == y[1]:
                date_connection = '.'+x[1]+'.'+x[0][2:]
                for date_number in range(int(x[2])+1, int(y[2])):
                    b += 1
                    if len(str(date_number)) == 1:
                        date_number_changed = '0'+str(date_number)
                    else:
                        date_number_changed = str(date_number)
                    x_date.insert(i+b, date_number_changed+date_connection)
                    price_graph.insert(i+b, price_connection)
                    date_info.insert(i+b, [['Žiadne objednávky\nv tento deň']])
            else:
                days_number = (d2-d1).days-1
                days_number_before = days_number-(int(y[2])-1)
                if days_number_before != 0:
                    date_connection = '.'+x[1]+'.'+x[0][2:]
                    for date_number in range(
                        int(x[2]), int(x[2])+days_number_before):
                        b += 1
                        if len(str(date_number+1)) == 1:
                            date_number_changed = '0'+str(date_number+1)
                        else:
                            date_number_changed = str(date_number+1)
                        x_date.insert(i+b, date_number_changed+date_connection)
                        price_graph.insert(i+b, price_connection)
                        date_info.insert(
                            i+b, [['Žiadne objednávky\nv tento deň']])
                date_connection = '.'+y[1]+'.'+y[0][2:]
                for date_number in range(1, int(y[2])):
                    b += 1
                    if len(str(date_number)) == 1:
                        date_number_changed = '0'+str(date_number)
                    else:
                        date_number_changed = str(date_number)
                    x_date.insert(i+b, date_number_changed+date_connection)
                    price_graph.insert(i+b, price_connection)
                    date_info.insert(i+b, [['Žiadne objednávky\nv tento deň']])


    def Values(self):
        
        # Set the needed variables
        if self.sklad:
            self.celkovy_pocet_produktov_na_sklade = 0
            self.najviac_mame_produkt = []
        else:
            self.celkovy_pocet_produktov_na_sklade = 'Žiadne dáta v SKLAD.txt'
            self.najviac_mame_produkt_ui = 'Žiadne dáta v SKLAD.txt'
            self.najviac_mame_produkt = ''
        if self.statistiky:
            self.avPrice = 0
        else:
            self.avPrice = 'Žiadne dáta v STATISTIKY.txt'
        self.top_ten_graf =\
        self.top_ten_worst_graf =\
            ''
        self.posledna_objednavka_P_ui =\
        self.posledna_objednavka_P =\
        self.posledna_objednavka_N_ui =\
        self.posledna_objednavka_N =\
            'Žiadna'
        self.profLoss = 0
        self.top_day = 'Žiadne dáta v STATISTIKY.txt'


    def sklad_loop(self):

        # Make the loop necessary
        # for given variables
        if self.sklad:
            najviac_produkt = int(self.sklad[0][1])
            for produkt_sklad in self.sklad:
                self.celkovy_pocet_produktov_na_sklade += int(produkt_sklad[1])
                if najviac_produkt == int(produkt_sklad[1]):
                    self.najviac_mame_produkt += produkt_sklad,
                elif najviac_produkt < int(produkt_sklad[1]):
                    self.najviac_mame_produkt = produkt_sklad,
                    najviac_produkt = int(produkt_sklad[1])


    def statistiky_loop(self):

        # Make the loop necessary
        # for given variables
        if self.statistiky:
            ttt = 0
            for objednavka in self.statistiky:
                if objednavka[1] == 'P':
                    self.avPrice += int(objednavka[4])*float(objednavka[5])
                    ttt += 1
                    self.posledna_objednavka_P = objednavka.copy()
                else:
                    self.posledna_objednavka_N = objednavka.copy()

            if ttt != 0:
                self.avPrice /= ttt
                self.avPrice = str(round(self.avPrice, 2))+'€'

            
    def prof_loss_current_day(self):

        # Show profit or loss
        # for the current day
        if self.statistiky:
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


    def top_products(self):

        # Creates a top produkty list
        # with the last 30 days of data
        if self.statistiky:
            top_produkty = [[0, 0]]
            first_day_top_ten = self.last_day - datetime.timedelta(30)
            if self.first_day >= first_day_top_ten:
                index = 0
            else:
                for i, obj in enumerate(self.statistiky):
                    if first_day_top_ten <= datetime.datetime.strptime(
                                    obj[0].split()[0], '%Y-%m-%d').date():
                        index = i
                        break
            for objednavka in self.statistiky[index:]:
                m = 0
                if objednavka[1] == 'P':
                    for i in range(len(top_produkty)):
                        if objednavka[3] == top_produkty[i][0]:
                            top_produkty[i][1] += 1
                            m = 1
                            break
                    if m == 0:
                        top_produkty.append([objednavka[3], 1])
            top_produkty.remove([0, 0])
            self.top_products_graph(top_produkty)

    def top_products_graph(self, top_produkty):

        # Creates lists needed to plot
        # the graph najpredavanejsie and
        # najmenej predavane produkty
        self.top_ten_graf = sorted(
            top_produkty, key=lambda x: x[1], reverse=True)
        self.top_ten_graf = self.top_ten_graf[:10]
        self.top_ten = [i[1] for i in self.top_ten_graf]

        self.top_ten_worst_graf = sorted(
            top_produkty, key=lambda x: x[1])
        self.top_ten_worst_graf = self.top_ten_worst_graf[:10]
        self.top_ten_worst = [i[1] for i in self.top_ten_worst_graf]
        self.unsold_products(top_produkty)

    def unsold_products(self, top_produkty):

        # Checks for unsold products
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


    def best_selling_day(self):
        
        # Return day with the
        # highest number of sales
        if self.statistiky:
            days = [datetime.datetime.strptime(i[0],
                    "%Y-%m-%d %H-%M-%S").strftime("%A")
                    for i in self.statistiky]
            self.top_day = max(set(days), key=days.count)

                    
    def tovar_loop(self):

        # Make the loop necessary
        # for given variables
        for produkt_tovar in self.tovar:
            for i in range(len(self.top_ten_graf)):
                if produkt_tovar[0] == self.top_ten_graf[i][0]:
                    self.top_ten_graf[i][0] = produkt_tovar[1]
                    break

            for i in range(len(self.top_ten_worst_graf)):
                if produkt_tovar[0] == self.top_ten_worst_graf[i][0]:
                    self.top_ten_worst_graf[i][0] = produkt_tovar[1]
                    break

            if self.najviac_mame_produkt:
                for i in range(len(self.najviac_mame_produkt)):
                    if self.najviac_mame_produkt[i][0] == produkt_tovar[0]:
                        self.najviac_mame_produkt[i][0] = produkt_tovar[1]
                        break

            if produkt_tovar[0] == self.posledna_objednavka_N[3]:
                self.posledna_objednavka_N[3] = produkt_tovar[1]

            if produkt_tovar[0] == self.posledna_objednavka_P[3]:
                self.posledna_objednavka_P[3] = produkt_tovar[1]
        self.most_product()
        self.last_order()

    def most_product(self):

        # Replace the code with the
        # name in the most we have product
        if self.sklad and self.najviac_mame_produkt:
            nove_produkty = str(self.najviac_mame_produkt[0][1])+' ks'
            for i in self.najviac_mame_produkt:
                nove_produkty += '\n'+i[0]
            self.najviac_mame_produkt_ui = nove_produkty

    def last_order(self):

        # Adjust last order
        # variables as needed
        if self.posledna_objednavka_N != 'Žiadna':
            posledna_objednavka_date_N = \
                self.posledna_objednavka_N[0].split()[0].split('-')[2] + '-' + \
                self.posledna_objednavka_N[0].split()[0].split('-')[1] +\
                '-'+self.posledna_objednavka_N[0].split()[0].split('-')[0] + \
                ' '+self.posledna_objednavka_N[0].split()[1]

            self.posledna_objednavka_N_ui = self.posledna_objednavka_N[3]+'\n' + \
                posledna_objednavka_date_N.split()[0].replace('-', '.')+' ' + \
                posledna_objednavka_date_N.split()[1].replace('-', ':')+';' + \
                self.posledna_objednavka_N[4]+'ks'+';' + \
                self.posledna_objednavka_N[5]+'€/ks'

        if self.posledna_objednavka_P != 'Žiadna':
            posledna_objednavka_date_P = \
                self.posledna_objednavka_P[0].split()[0].split('-')[2] + '-' + \
                self.posledna_objednavka_P[0].split()[0].split('-')[1] +\
                '-'+self.posledna_objednavka_P[0].split()[0].split('-')[0] + \
                ' '+self.posledna_objednavka_P[0].split()[1]

            self.posledna_objednavka_P_ui = self.posledna_objednavka_P[3]+'\n' + \
                posledna_objednavka_date_P.split()[0].replace('-', '.')+' ' + \
                posledna_objednavka_date_P.split()[1].replace('-', ':')+';' + \
                self.posledna_objednavka_P[4]+'ks'+';' + \
                self.posledna_objednavka_P[5]+'€/ks'



    def NajviacGraf(self):

        if self.statistiky:
            def update_annot1(event, bar_x_pos):
                x = event.xdata
                y = event.ydata
                annot1.xy = (x, y)
                for c, i in enumerate(bar_X_new):
                    if i == bar_x_pos:
                        text_lomeno_n = ''
                        text_bez_lomeno_n = self.top_ten_graf[c][0].split()
                        for i in text_bez_lomeno_n:
                            text_lomeno_n += i+'\n'
                        if self.top_ten_graf[c][1] == 1:
                            objednavka_text = ' objednávka'
                        elif 1 < self.top_ten_graf[c][1] < 5:
                            objednavka_text = ' objednávky'
                        else:
                            objednavka_text = ' objednávok'
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

            najviac, a1 = plt.subplots(
                figsize=[4.9, 3.15], linewidth=self.linewidth,
                edgecolor=self.edgecolor)
            najviac.patch.set_facecolor(self.graph_color)
            self.commands.track_graph(najviac)
            a1.set_facecolor(self.graph_color)
            bar_X = [i for i in range(len(self.top_ten_graf))]
            a1.tick_params(axis='x', which='both', length=0)
            a1.spines.top.set_visible(False)
            a1.spines.right.set_visible(False)
            a1.axes.xaxis.set_ticklabels([])
            a1.set_title('Najpredávanejšie produkty', **
                        self.font, fontsize=15, weight='bold')
            bars1 = a1.bar(bar_X, self.top_ten)
            bar_X_new = []
            for bar in bars1:
                bar_X_new.append(bar.get_x())

            annot1 = a1.annotate('', xy=(0, 0), xytext=(0, 10), textcoords='offset points',
                                ha='center', color='white', size=15,
                                bbox=dict(boxstyle="round", fc='#2F3E46',
                                alpha=1, ec="#101416", lw=2))
            annot1.set_visible(False)

            najviac.canvas.mpl_connect("motion_notify_event", hover1)
            self.commands.plot_graph(self.ui.najviacGraf, najviac)
        else:
            scene = QGraphicsScene()
            text = scene.addText('Najpredávanejšie produkty')
            text.setPos(0, -50)
            scene.addText('Žiadne dáta v STATISTIKY.txt')
            self.ui.najviacGraf.setScene(scene)


    def NajmenejGraf(self):

        if self.statistiky:
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
                            objednavka_text = 'objednávok'
                        elif self.top_ten_worst_graf[c][1] == 1:
                            objednavka_text = ' objednávka'
                        elif 1 < self.top_ten_worst_graf[c][1] < 5:
                            objednavka_text = ' objednávky'
                        else:
                            objednavka_text = ' objednávok'
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

            najmenej, a2 = plt.subplots(
                figsize=[4.9, 3.15], linewidth=self.linewidth,
                edgecolor=self.edgecolor)
            najmenej.patch.set_facecolor(self.graph_color)
            self.commands.track_graph(najmenej)
            a2.set_facecolor(self.graph_color)
            a2.spines['top'].set_visible(False)
            a2.spines['right'].set_visible(False)
            a2.axes.xaxis.set_ticklabels([])
            a2.tick_params(axis='x', which='both', length=0)
            a2.set_title('Najmenej predávané produkty', **
                         self.font, fontsize=15, weight='bold')
            bar_X = [i for i in range(len(self.top_ten_worst_graf))]
            bars2 = a2.bar(bar_X, self.top_ten_worst, color='#d88c00')
            bar_X = []
            for bar in bars2:
                bar_X.append(bar.get_x())

            annot2 = a2.annotate("", xy=(0, 0), xytext=(0, 10), textcoords='offset points',
                                ha='center', color='white', size=15,
                                bbox=dict(boxstyle="round", fc='#2F3E46',
                                alpha=1, ec="#101416", lw=2))
            annot2.set_visible(False)

            najmenej.canvas.mpl_connect("motion_notify_event", hover2)
            self.commands.plot_graph(self.ui.najmenejGraf, najmenej)
        else:
            scene = QGraphicsScene()
            text = scene.addText('Najmenej predávané produkty')
            text.setPos(0, -50)
            scene.addText('Žiadne dáta v STATISTIKY.txt')
            self.ui.najmenejGraf.setScene(scene)


    def VyvojGrafVsetky(self):

        # Plot all graphs
        # based on categories
        tab_index = self.ui.tabWidget.currentIndex()
        if tab_index == 0:
            self.VyvojGraf(self.x_date_all, self.price_graph_all,
                            self.ui.trzbyNakladyVsetko, self.date_info_all)
            self.VyvojGraf(self.x_date_tricka, self.price_graph_tricka,
                            self.ui.trzbyNakladyTricka, self.date_info_tricka)
            self.VyvojGraf(self.x_date_topanky, self.price_graph_topanky,
                            self.ui.trzbyNakladyTopanky, self.date_info_topanky)
            self.VyvojGraf(self.x_date_mikiny, self.price_graph_mikiny,
                            self.ui.trzbyNakladyMikiny, self.date_info_mikiny)
            self.VyvojGraf(self.x_date_nohavice, self.price_graph_nohavice,
                            self.ui.trzbyNakladyNohavice, self.date_info_nohavice)
            self.VyvojGraf(self.x_date_doplnky, self.price_graph_doplnky,
                            self.ui.trzbyNakladyDoplnky, self.date_info_doplnky)
        elif tab_index == 1:
            self.VyvojGraf(self.x_date_tricka, self.price_graph_tricka,
                            self.ui.trzbyNakladyTricka, self.date_info_tricka)
            self.VyvojGraf(self.x_date_all, self.price_graph_all,
                            self.ui.trzbyNakladyVsetko, self.date_info_all)
            self.VyvojGraf(self.x_date_topanky, self.price_graph_topanky,
                            self.ui.trzbyNakladyTopanky, self.date_info_topanky)
            self.VyvojGraf(self.x_date_mikiny, self.price_graph_mikiny,
                            self.ui.trzbyNakladyMikiny, self.date_info_mikiny)
            self.VyvojGraf(self.x_date_nohavice, self.price_graph_nohavice,
                            self.ui.trzbyNakladyNohavice, self.date_info_nohavice)
            self.VyvojGraf(self.x_date_doplnky, self.price_graph_doplnky,
                            self.ui.trzbyNakladyDoplnky, self.date_info_doplnky)
        elif tab_index == 2:
            self.VyvojGraf(self.x_date_topanky, self.price_graph_topanky,
                            self.ui.trzbyNakladyTopanky, self.date_info_topanky)
            self.VyvojGraf(self.x_date_tricka, self.price_graph_tricka,
                            self.ui.trzbyNakladyTricka, self.date_info_tricka)
            self.VyvojGraf(self.x_date_all, self.price_graph_all,
                            self.ui.trzbyNakladyVsetko, self.date_info_all)
            self.VyvojGraf(self.x_date_mikiny, self.price_graph_mikiny,
                            self.ui.trzbyNakladyMikiny, self.date_info_mikiny)
            self.VyvojGraf(self.x_date_nohavice, self.price_graph_nohavice,
                            self.ui.trzbyNakladyNohavice, self.date_info_nohavice)
            self.VyvojGraf(self.x_date_doplnky, self.price_graph_doplnky,
                            self.ui.trzbyNakladyDoplnky, self.date_info_doplnky)
        elif tab_index == 3:
            self.VyvojGraf(self.x_date_mikiny, self.price_graph_mikiny,
                            self.ui.trzbyNakladyMikiny, self.date_info_mikiny)
            self.VyvojGraf(self.x_date_tricka, self.price_graph_tricka,
                            self.ui.trzbyNakladyTricka, self.date_info_tricka)
            self.VyvojGraf(self.x_date_all, self.price_graph_all,
                            self.ui.trzbyNakladyVsetko, self.date_info_all)
            self.VyvojGraf(self.x_date_topanky, self.price_graph_topanky,
                            self.ui.trzbyNakladyTopanky, self.date_info_topanky)
            self.VyvojGraf(self.x_date_nohavice, self.price_graph_nohavice,
                            self.ui.trzbyNakladyNohavice, self.date_info_nohavice)
            self.VyvojGraf(self.x_date_doplnky, self.price_graph_doplnky,
                            self.ui.trzbyNakladyDoplnky, self.date_info_doplnky)
        elif tab_index == 4:
            self.VyvojGraf(self.x_date_nohavice, self.price_graph_nohavice,
                            self.ui.trzbyNakladyNohavice, self.date_info_nohavice)
            self.VyvojGraf(self.x_date_tricka, self.price_graph_tricka,
                            self.ui.trzbyNakladyTricka, self.date_info_tricka)
            self.VyvojGraf(self.x_date_all, self.price_graph_all,
                            self.ui.trzbyNakladyVsetko, self.date_info_all)
            self.VyvojGraf(self.x_date_topanky, self.price_graph_topanky,
                            self.ui.trzbyNakladyTopanky, self.date_info_topanky)
            self.VyvojGraf(self.x_date_mikiny, self.price_graph_mikiny,
                            self.ui.trzbyNakladyMikiny, self.date_info_mikiny)
            self.VyvojGraf(self.x_date_doplnky, self.price_graph_doplnky,
                            self.ui.trzbyNakladyDoplnky, self.date_info_doplnky)
        elif tab_index == 5:
            self.VyvojGraf(self.x_date_doplnky, self.price_graph_doplnky,
                            self.ui.trzbyNakladyDoplnky, self.date_info_doplnky)
            self.VyvojGraf(self.x_date_tricka, self.price_graph_tricka,
                            self.ui.trzbyNakladyTricka, self.date_info_tricka)
            self.VyvojGraf(self.x_date_all, self.price_graph_all,
                            self.ui.trzbyNakladyVsetko, self.date_info_all)
            self.VyvojGraf(self.x_date_topanky, self.price_graph_topanky,
                            self.ui.trzbyNakladyTopanky, self.date_info_topanky)
            self.VyvojGraf(self.x_date_mikiny, self.price_graph_mikiny,
                            self.ui.trzbyNakladyMikiny, self.date_info_mikiny)
            self.VyvojGraf(self.x_date_nohavice, self.price_graph_nohavice,
                            self.ui.trzbyNakladyNohavice, self.date_info_nohavice)
        
    def VyvojGraf(self, x_date, price_graph, qtgraf, date_info_graph):

        def set_cross_hair_visible(visible):
            need_redraw = horizontal_line.get_visible() != visible
            horizontal_line.set_visible(visible)
            vertical_line.set_visible(visible)
            annot3.set_visible(visible)
            return need_redraw

        def on_mouse_move(event):
            if not event.inaxes:
                self.last_index = None
                need_redraw = set_cross_hair_visible(False)
                if need_redraw:
                    a3.figure.canvas.draw()
            else:
                x1 = event.xdata
                if x1 < mid_x:
                    annot3.xy = (mid_x+1/6*(x_axis_lim[1]-mid_x),
                                 mid_y+3/4*(y_axis_lim[1]-mid_y))
                else:
                    annot3.xy = (mid_x-15/16*(x_axis_lim[1]-mid_x),
                                 mid_y+3/4*(y_axis_lim[1]-mid_y))
                set_cross_hair_visible(True)

                if x1 < 0:
                    searchsorted = 0
                else:
                    searchsorted = str(round(x1, 0))[:-2]
                index = min(int(searchsorted), len(x) - 1)

                date_info_graph_index = date_info_graph[index]
                if date_info_graph_index != [['Žiadne objednávky\nv tento deň']]:
                    date_info_p = 0
                    date_info_n = 0
                    p_value = 0
                    n_value = 0
                    value_day = 0
                    for i in date_info_graph_index:
                        if i[1] == 'P':
                            date_info_p += 1
                            p_value += int(i[4])*float(i[5])
                            value_day += int(i[4])*float(i[5])
                        else:
                            date_info_n += 1
                            n_value += int(i[4])*float(i[5])
                            value_day -= int(i[4])*float(i[5])
                    annot3.set_text('''Dátum: %s
Počet objednávok: %s
Počet predajov: %s
Hodnota predajov: %s
Počet nákupov: %s
Hodnota nákupov: %s
Hrubý zisk za deň: %s€''' %
                        (x_date[index], len(date_info_graph[index]),
                            date_info_p, round(
                                p_value, 2), date_info_n,
                            round(n_value, 2), round(value_day, 2)))
                else:
                    annot3.set_text('Dátum: %s\n%s' %
                                    (x_date[index], date_info_graph[index][0][0]))

                if index == self.last_index:
                    return
                self.last_index = index

                vertical_line.set_xdata(x[index])
                horizontal_line.set_ydata(y[index])
                a3.figure.canvas.draw()

        vyvoj_ceny, a3 = plt.subplots(
            figsize=[7.18, 3.21], linewidth=self.linewidth, edgecolor=self.edgecolor)
        vyvoj_ceny.set_facecolor(self.graph_color)
        self.commands.track_graph(vyvoj_ceny)
        a3.set_facecolor(self.graph_color)
        a3.spines['top'].set_visible(False)
        a3.spines['right'].set_visible(False)
        a3.set_title('Zisk firmy', **self.font, fontsize=15,
                     weight='bold')
        line, = a3.plot(x_date, price_graph)
        a3.xaxis.set_major_locator(plt.MaxNLocator(5))
        horizontal_line = a3.axhline(color='k', lw=0.8, ls='--')
        vertical_line = a3.axvline(color='k', lw=0.8, ls='--')
        horizontal_line.set_visible(False)
        vertical_line.set_visible(False)
        x, y = line.get_data()
        self.last_index = None

        annot3 = a3.annotate("", xy=(0, 0), xytext=(0, 0), textcoords='offset points',
                            ha='left', va='top', color='white', size=15,
                            bbox=dict(boxstyle="round", fc='#2F3E46',
                            alpha=1, ec="#101416", lw=2))
        annot3.set_visible(False)

        x_axis_lim = a3.set_xlim()
        y_axis_lim = a3.set_ylim()
        mid_x = (x_axis_lim[0]+x_axis_lim[1])/2
        mid_y = (y_axis_lim[0]+y_axis_lim[1])/2

        if x_date:
            vyvoj_ceny.canvas.mpl_connect(
                'motion_notify_event', on_mouse_move)
            self.commands.plot_graph(qtgraf,vyvoj_ceny, size=68.5)
        else:
            scene = QGraphicsScene()
            scene.addText('Žiadne dáta v STATISTIKY.txt')
            qtgraf.setScene(scene)



    def zisk_firmy_color(self):

        # Sets zisk firmy color
        ziskFirmyColor = '#717171' 
        if self.statistiky:
            if self.zisk_firmy_za_obdobie < 0:
                    ziskFirmyColor = '#FF0000'
            elif self.zisk_firmy_za_obdobie > 0:
                ziskFirmyColor = '#21BF3E'
            self.ui.label_17.setText(str(round(self.zisk_firmy_za_obdobie,2))+'€')
            self.ui.label_17.setStyleSheet('color:'+ziskFirmyColor)
        else:
            self.ui.label_17.setText('--')
            self.ui.label_17.setStyleSheet('color:'+ziskFirmyColor)



    def FunFacts(self):
        
        # Display fun facts
        # about camels eshop
        profLossColor = '#717171'
        if self.statistiky:
            if str(datetime.date.today()) == self.statistiky[-1][0].split()[0]:
                if self.statistiky:
                    if self.profLoss < 0:
                        profLossColor = '#FF0000'
                    elif self.profLoss > 0:
                        profLossColor = '#21BF3E'
            else:
                profLossColor = '#717171'
                self.profLoss = 0

            self.ui.label_6.setText(str(self.profLoss)+'€')
            self.ui.label_6.setToolTip('''Táto cena vyjadruje zisk alebo stratu za aktuálny deň
od 0:00:00 až do 23:59:59.
Pre detailnejšie zobrazenie vývoju zisku firmy pozri graf nižšie -->''')
            self.ui.label_6.setStyleSheet('''QToolTip {
                                            font-size:9pt;
                                            color:white;
                                            background-color: #2F3E46;
                                            border: 1px solid #101416;}
                                            #label_6 {color: %s}''' % profLossColor)
        else:
            self.ui.label_6.setText('--')
            self.ui.label_6.setToolTip('Žiadne dáta v STATISTIKY.txt')
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
        self.ui.label_12.setText(str(self.top_day))
        self.ui.label_12.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_16.setText(str(self.najviac_mame_produkt_ui))
        self.ui.label_16.setStyleSheet('color:'+self.funFactsColor)
        self.ui.label_14.setText(str(self.posledna_objednavka_P_ui))
        self.ui.label_14.setStyleSheet('color:%s' % self.funFactsColor)
        self.ui.label_14.setToolTip('P - predaj firmy')
        self.ui.label_13.setToolTip('P - predaj firmy')
        self.ui.label_3.setText(str(self.posledna_objednavka_N_ui))
        self.ui.label_3.setStyleSheet('color:%s' % self.funFactsColor)
        self.ui.camelLogo_2.setToolTip('')
        self.ui.label_18.setHidden(True)
        self.ui.label_18.setStyleSheet('''QLabel {
                                        font-size:9pt;
                                        color:white;
                                        background-color: #2F3E46;
                                        border: 1px solid #101416;}''')
        self.ui.label_18.setText('''
-Grafy najpredávanejsie a najmenej predávané produkty,
 ukazujú produkty predané za posledných 30 dní

-Posledná objednávka N - nákup, ktorý urobila firma
-Posledná objednávka P - nákup, ktorý urobil zákazník

-Cena naľavo od ''INFO'' ukazuje zisk alebo stratu firmy
 za aktuálny deň

-''Zisk firmy za dané časové obdobie'' udáva zisk alebo stratu firmy
 za vami zvolené obdobie

-Graf ''Zisk firmy'' ukazuje krivku vývoja akcii spoločnosti CAMELS s.r.o,
 za vami zvolené časové obdobie
 Pomocou tlačidla ''OK'' naľavo od dátumov, sa graf updatne
''')