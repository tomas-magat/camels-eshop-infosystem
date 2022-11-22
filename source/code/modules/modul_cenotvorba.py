from PyQt5 import QtWidgets, QtCore
from utils.ui_commands import UI_Commands


class Cenotvorba:

    def __init__(self, ui):

        self.ui = ui
        self.commands = UI_Commands(self.ui)
        self.commands.button_click(
            self.ui.cenotvorbaButton, self.switch_screen)
        self.loadfile()

    def switch_screen(self):

        self.commands.redirect(self.ui.cenotvorba)

    def loadfile(self):
        for i in range(5):
            ItemPriceCard(self, self.ui.verticalLayout_25, "test" +
                     str(i), "Test "+str(i), "0000", (5.99, 6.59))


class ItemPriceCard(QtWidgets.QFrame):

    def __init__(self, page, layout, name: str,
                 display_name: str, code: str, price):

        super(ItemPriceCard, self).__init__(layout.parent())

        self.page = page
        self.ui = self.page.ui
        self.commands = self.page.commands

        self.parent_layout = layout

        self.name = name
        self.display_name = display_name
        self.code = code
        self.buy_price = price[0]
        self.self_price = price[1]

        self.draw_ui()
        

    def draw_ui(self):
        self.setGeometry(QtCore.QRect(10, 140, 701, 60))
        self.setMaximumSize(QtCore.QSize(16777215, 60))
        self.setShape(QtWidgets.Q.Box)
        self.setObjectName(self.name)
        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(self.name+"MainLayout")
        self.widget_4 = QtWidgets.QWidget(self)
        self.widget_4.setMinimumSize(QtCore.QSize(60, 0))
        self.widget_4.setMaximumSize(QtCore.QSize(60, 16777215))
        self.widget_4.setObjectName(self.name+"widget_4")
        self.label_2 = QtWidgets.QLabel(self.widget_4)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 43, 13))
        self.label_2.setObjectName(self.name+"label_2")
        self.mainLayout.addWidget(self.widget_4)
        self.widget_5 = QtWidgets.QWidget(self)
        self.widget_5.setMinimumSize(QtCore.QSize(200, 0))
        self.widget_5.setMaximumSize(QtCore.QSize(150, 16777215))
        self.widget_5.setObjectName(self.name+"widget_5")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout_24.setObjectName(self.name+"verticalLayout_24")
        self.label_3 = QtWidgets.QLabel(self.widget_5)
        self.label_3.setObjectName(self.name+"label_3")
        self.verticalLayout_24.addWidget(self.label_3)
        self.mainLayout.addWidget(self.widget_5)
        self.widget_6 = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setObjectName(self.name+"widget_6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_6.setObjectName(self.name+"horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.widget_6)
        self.label_4.setObjectName(self.name+"label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget_6)
        self.lineEdit_4.setObjectName(self.name+"lineEdit_4")
        self.lineEdit_4.setText(str(self.buy_price))
        self.horizontalLayout_6.addWidget(self.lineEdit_4)
        self.label_5 = QtWidgets.QLabel(self.widget_6)
        self.label_5.setObjectName(self.name+"label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.widget_6)
        self.lineEdit_5.setObjectName(self.name+"lineEdit_5")
        self.lineEdit_4.setText(str(self.sell_price))
        self.horizontalLayout_6.addWidget(self.lineEdit_5)
        self.mainLayout.addWidget(self.widget_6)
        self.parent_layout.addWidget(self)
