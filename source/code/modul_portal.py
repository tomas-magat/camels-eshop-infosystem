import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

import utils
from main_ui import Ui_MainWindow


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.ui.stackedWidget.setCurrentWidget(self.ui.index)

        self.ui.pushButton.clicked.connect(self.price)
        self.ui.pushButton_2.clicked.connect(self.stats)
        self.ui.pushButton_3.clicked.connect(self.storage)
        self.ui.pushButton_4.clicked.connect(self.portal)
        self.ui.pushButton_5.clicked.connect(self.database)

        self.ui.home.clicked.connect(self.index)
        self.ui.home_2.clicked.connect(self.index)
        self.ui.home_3.clicked.connect(self.index)
        self.ui.home_4.clicked.connect(self.index)
        self.ui.home_5.clicked.connect(self.index)

        # self.goods = utils.read_file('tovar')
        # self.version = utils.get_version('tovar')

        # # Update 'goods' variable every 3 seconds
        # utils.run_periodically(self.update_goods, 3)

    def update_goods(self):
        current_version = utils.get_version('tovar')

        if current_version != self.version:
            self.goods = utils.read_file('tovar')
            self.version = current_version

    def show(self):
        self.main_win.show()

    def price(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.cenotvorba)

    def stats(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.statistika)

    def storage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.sklad)

    def portal(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.portal)

    def database(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.databaza)

    def index(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
