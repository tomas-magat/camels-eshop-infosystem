from PyQt5 import QtWidgets, QtCore, QtGui
from utils.tools import *


class Cenotvorba:

    def __init__(self, app):

        self.ui = app.ui
        self.commands = app.commands
        self.data = app.data

        self.layouts = [
            self.ui.verticalLayout_51,
            self.ui.verticalLayout_53,
            self.ui.verticalLayout_55,
            self.ui.verticalLayout_54,
            self.ui.verticalLayout_56,
            self.ui.verticalLayout_57,
            self.ui.verticalLayout_58,
        ]

        self.commands.button_click(
            self.ui.cenotvorbaButton, self.switch_screen
        )
        self.commands.buttons_click(
            [self.ui.saveButton, self.ui.homeArrow3], self.savefile
        )
        self.commands.form_submit(
            [self.ui.searchButton_2, self.ui.searchField_2],
            self.search
        )
        self.commands.tab_selected(
            self.ui.tabWidget_2, self.update_category
        )

        self.price_cards = []
        self.items = self.data['tovar']
        self.prices = self.data['cennik']
        # self.items.version_changed(self.loadfile)
        # self.prices.version_changed(
        #     lambda x: self.loadfile(self.items.data))
        self.ui.tabWidget_2.setCurrentIndex(0)
        self.update_category()

    def switch_screen(self):
        self.commands.redirect(self.ui.cenotvorba)

    def update_category(self):
        self.category = self.ui.tabWidget_2.currentIndex()
        self.loadfile(self.items.data)

    def loadfile(self, data):
        self.commands.clear_layout(self.layouts[self.category])
        data = filter_category(data, self.category)

        for code, value in data.items():
            self.load_item(code, value)

    def load_item(self, code, value):
        item_price = self.prices.data.get(code)

        if item_price != None:
            price = item_price
        else:
            price = ['----', '----']
            item_card = ItemPriceCard(self, self.layouts[6],
                                      value[0], code, price, value[1], )
            self.price_cards.append(item_card)

        if self.category != 6:
            item_card = ItemPriceCard(self, self.layouts[self.category],
                                      value[0], code, price, value[1])
            self.price_cards.append(item_card)

    def savefile(self):
        self.changed = False
        for item in self.price_cards:
            prices = item.getPrices()

            if self.prices.data.get(item.code) != prices:
                if '----' not in prices:
                    self.prices.data[item.code] = prices
                    self.changed = True

        if self.changed:
            self.prices.save_data()

    def search(self):
        self.query = self.ui.searchField_2.text()
        self.result = search_items(
            self.query, self.items.data, self.category
        ) if self.query != '' else self.items.data

        self.search_results()

    def search_results(self):
        if self.result == {}:
            self.no_results()
        else:
            self.loadfile(self.result)

    def no_results(self):
        self.commands.clear_layout(self.layouts[self.category])
        label = self.no_results_label()
        self.layouts[self.category].addWidget(label)

    @staticmethod
    def no_results_label():
        label = QtWidgets.QLabel('Produkt sa nena??iel...')
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(12)
        label.setFont(font)
        label.setStyleSheet('color: #b0180b;')
        return label


class ItemPriceCard(QtWidgets.QFrame):

    def __init__(self, page, layout, name: str, code: str,
                 price=['----', '----'], image: str = ''):

        super(ItemPriceCard, self).__init__(layout.parent())

        self.page = page
        self.ui = self.page.ui
        self.commands = self.page.commands

        self.parent_layout = layout

        self.name = camelify(name)
        self.display_name = name
        self.code = code
        self.buy_price = str(price[0])
        self.sell_price = str(price[1])
        self.image = find_image(image)
        self.valid = [True, True]

        self.draw_ui()

    def getPrices(self):
        if self.valid[0]:
            self.buy_price = convert_price(self.lineEdit_4)
        else:
            self.commands.error('Zadajte spr??vnu k??pnu cenu.')
        if self.valid[1]:
            self.sell_price = convert_price(self.lineEdit_5)
        else:
            self.commands.error('Zadajte spr??vnu predajn?? cenu.')

        return [self.buy_price, self.sell_price]

    def validate_field(self, line_edit, i):
        try:
            text = re.sub(',|;', '.', line_edit.text())
            float(text)
        except:
            if '----' not in line_edit.text():
                self.valid[i] = False
                line_edit.setStyleSheet("border: 1px solid red;")
            else:
                self.valid[i] = True
                line_edit.setStyleSheet("")
        else:
            self.valid[i] = True
            line_edit.setStyleSheet("")

    def draw_ui(self):
        self.setMinimumSize(QtCore.QSize(0, 60))
        self.setMaximumSize(QtCore.QSize(16777215, 60))
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setObjectName("Frame")
        if '----' in self.buy_price or '----' in self.sell_price:
            self.setStyleSheet("#Frame{border: 2px solid red}")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(self.name+"horizontalLayout_2")
        self.widget_4 = QtWidgets.QWidget(self)
        self.widget_4.setMinimumSize(QtCore.QSize(60, 0))
        self.widget_4.setMaximumSize(QtCore.QSize(60, 16777215))
        self.widget_4.setObjectName(self.name+"widget_4")
        self.label_2 = QtWidgets.QLabel(self.widget_4)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 61, 61))
        self.label_2.setPixmap(QtGui.QPixmap(self.image))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName(self.name+"label_2")
        self.horizontalLayout_2.addWidget(self.widget_4)
        self.widget_5 = QtWidgets.QWidget(self)
        self.widget_5.setMinimumSize(QtCore.QSize(190, 0))
        self.widget_5.setMaximumSize(QtCore.QSize(190, 16777215))
        self.widget_5.setObjectName(self.name+"widget_5")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout_24.setContentsMargins(20, -1, -1, -1)
        self.verticalLayout_24.setObjectName(self.name+"verticalLayout_24")
        self.label_3 = QtWidgets.QLabel(self.display_name + ' #' + self.code)
        self.label_3.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(self.name+"label_3")
        self.verticalLayout_24.addWidget(self.label_3)
        self.horizontalLayout_2.addWidget(self.widget_5)
        self.widget_6 = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setObjectName(self.name+"widget_6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_6.setContentsMargins(-1, -1, 50, -1)
        self.horizontalLayout_6.setObjectName(self.name+"horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel("K??pna cena: ")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(0, 0))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 16777214))
        self.label_4.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(self.name+"label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.buy_price)
        self.lineEdit_4.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_4.setStyleSheet("background-color: #FFF")
        self.lineEdit_4.setObjectName(self.name+"lineEdit_4")
        self.commands.text_changed(
            self.lineEdit_4,
            lambda: self.validate_field(self.lineEdit_4, 0)
        )
        self.horizontalLayout_6.addWidget(self.lineEdit_4)
        self.label_5 = QtWidgets.QLabel("Predajn?? cena: ")
        self.label_5.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(self.name+"label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.sell_price)
        self.lineEdit_5.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_5.setStyleSheet("background-color: #FFF")
        self.lineEdit_5.setObjectName(self.name+"lineEdit_5")
        self.commands.text_changed(
            self.lineEdit_5,
            lambda: self.validate_field(self.lineEdit_5, 1)
        )
        self.horizontalLayout_6.addWidget(self.lineEdit_5)
        self.horizontalLayout_2.addWidget(self.widget_6)
        self.parent_layout.addWidget(self)
