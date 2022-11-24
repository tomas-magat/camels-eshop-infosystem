from PyQt5 import QtWidgets, QtCore, QtGui
from utils.ui_commands import UI_Commands
from utils.tools import find_image


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
        for i in range(7):
            ItemPriceCard(self, self.ui.verticalLayout_25, "test" +
                          str(i), "Test "+str(i), "0000", (5.99, 6.59),
                          find_image("tricko.jpg"))


class ItemPriceCard(QtWidgets.QFrame):

    def __init__(self, page, layout, name: str,
                 display_name: str, code: str, price, image: str):

        super(ItemPriceCard, self).__init__(layout.parent())

        self.page = page
        self.ui = self.page.ui
        self.commands = self.page.commands

        self.parent_layout = layout

        self.name = name
        self.display_name = display_name
        self.code = code
        self.buy_price = str(price[0])
        self.sell_price = str(price[1])
        self.image = image

        self.draw_ui()

    def draw_ui(self):
        self.setMinimumSize(QtCore.QSize(0, 60))
        self.setMaximumSize(QtCore.QSize(16777215, 60))
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setObjectName(self.name)
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
        self.widget_5.setMinimumSize(QtCore.QSize(150, 0))
        self.widget_5.setMaximumSize(QtCore.QSize(150, 16777215))
        self.widget_5.setObjectName(self.name+"widget_5")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout_24.setContentsMargins(20, -1, -1, -1)
        self.verticalLayout_24.setObjectName(self.name+"verticalLayout_24")
        self.label_3 = QtWidgets.QLabel(self.display_name.upper())
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
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
        self.label_4 = QtWidgets.QLabel("PREDAJNA CENA")
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(0, 0))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 16777214))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(self.name+"label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.buy_price)
        self.lineEdit_4.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_4.setStyleSheet("background-color: #FFF")
        self.lineEdit_4.setFrame(False)
        self.lineEdit_4.setObjectName(self.name+"lineEdit_4")
        self.horizontalLayout_6.addWidget(self.lineEdit_4)
        self.label_5 = QtWidgets.QLabel("KUPNA CENA")
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(self.name+"label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.sell_price)
        self.lineEdit_5.setMaximumSize(QtCore.QSize(60, 16777215))
        self.lineEdit_5.setStyleSheet("background-color: #FFF")
        self.lineEdit_5.setFrame(False)
        self.lineEdit_5.setObjectName(self.name+"lineEdit_5")
        self.horizontalLayout_6.addWidget(self.lineEdit_5)
        self.horizontalLayout_2.addWidget(self.widget_6)
        self.parent_layout.addWidget(self)
