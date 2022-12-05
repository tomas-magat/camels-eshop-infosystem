# Modul Portal -
# Lists catalog of available products, has an option
# to search by code/name and to filter products.
# After buying the selected items in given amounts,
# creates file uctenka_[id_transakcie].txt.

from PyQt5 import QtWidgets, QtCore, QtGui

from utils.ui_commands import UI_Commands
from utils.file import DataFile
from utils.tools import *


class Portal:

    def __init__(self, ui):
        """
        This class handles everything done on the portal
        screen (button clicks, item listing...).
        """

        self.ui = ui
        self.commands = UI_Commands(self.ui)

        # Init cart global variables
        self.cart_price = 0
        self.cart = {}
        self.cashier_name = ""

        # Init catalog global variables
        self.sort_state = 1
        self.catalog = []

        # Track UI actions
        self.redirect_action()
        self.search_action()
        self.sort_action()
        self.login_actions()
        self.buy_action()

        # Load data
        self.goods = DataFile('tovar')
        self.prices = DataFile('cennik')
        self.storage = DataFile('sklad')
        self.load_items(self.goods.data)

        # Update 'goods' variable every 3 seconds
        self.version = self.goods.version
        # run_periodically(self.update_goods, 3)

    # ==================== ACTIONS =======================
    def redirect_action(self):
        self.commands.buttons_click(
            [self.ui.portalButton, self.ui.homeArrow6],
            self.switch_screen
        )

    def search_action(self):
        self.commands.form_submit(
            [self.ui.searchButton, self.ui.searchField],
            self.search
        )

    def sort_action(self):
        self.commands.button_click(
            self.ui.sortButton, self.sort
        )

    def login_actions(self):
        self.commands.buttons_click(
            [self.ui.userIconButton, self.ui.userNameButton],
            self.login
        )
        self.commands.form_submit(
            [self.ui.nameEntry, self.ui.loginButton],
            lambda: self.switch_screen(update_user=True)
        )

    def buy_action(self):
        self.commands.button_click(
            self.ui.buyButton, self.buy
        )

    def switch_screen(self, update_user: bool = False):
        """Redirect to portal screen, set cashier name if given."""

        if update_user:
            self.cashier_name = self.ui.nameEntry.text()
            self.ui.userNameButton.setText(self.cashier_name)

        self.commands.redirect(self.ui.portal)

    def search(self):
        """
        Get the value of the search field and load
        items with matching names or codes.
        """

        self.query = self.ui.searchField.text()
        self.result = search_items(self.query)
        self.reload_items(self.result)

    def sort(self):
        """Update sort button and change sort state."""

        if self.sort_state == 1:
            self.create_icon("up_arrow.png", "Highest price", 2)
        elif self.sort_state == 2:
            self.create_icon("down_arrow.png", "Lowest price", 3)
        else:
            self.create_icon("up_down_arrow.png", "Sort by price", 1)

    def login(self):
        """Redirect to login screen."""

        self.commands.redirect(self.ui.login)

    def buy(self):
        """Buy everything in the cart, generate uctenka_[id].txt"""

        self.create_receipt()
        self.update_price(-self.cart_price)
        self.commands.clear_layout(self.ui.cartLayout)

    def create_icon(self, icon_name, text, new_state):
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(find_icon(icon_name)),
            QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.ui.sortButton.setText(text)
        self.sort_state = new_state

        self.ui.sortButton.setIcon(icon)

    def reload_items(self, data):
        self.catalog = []
        self.commands.clear_layout(self.ui.allLayout)
        self.load_items(self.result)

    def load_items(self, data):
        for key, vals in data.items():
            self.load_item(key, vals)

    def load_item(self, key, vals):
        price = self.prices.data.get(key)

        if price != None and key not in self.catalog:
            ItemCard(
                self, int(key[0]), vals[0],
                key, float(price[1]), find_image(vals[1])
            )
            self.catalog.append(key)

    def create_receipt(self):
        receipt_id = random_id('P')
        filename = 'uctenka_'+receipt_id+'.txt'
        filepath = os.path.join(PATH, 'source', 'data', filename)

        with open(filepath, 'w') as receipt:
            self.receipt_template(receipt, receipt_id)

    def receipt_template(self, receipt, id):
        receipt.write('Cislo uctenky: '+id)
        receipt.write('\nVytvorene: '+now())
        receipt.write('\nPokladnik: '+self.cashier_name)
        receipt.write('\nSpolu cena: '+str(self.cart_price)+' €\n')
        receipt.write('\n=================================\n')
        items = [' - '.join(x)+'\n' for x in list(self.cart.values())]
        receipt.writelines(items)

    def update_goods(self):
        """
        Update 'goods' variable if version of the tovar.txt
        datafile has changed.
        """

        current_version = self.goods.version

        if current_version != self.version:
            self.goods.read()
            self.version = current_version
            self.load_items()

    def update_price(self, value):
        """Update total price of a cart."""

        self.cart_price += value
        self.ui.totalPrice.setText(
            "Spolu: "+str_price(self.cart_price, 1)+" €")


class ItemCard(QtWidgets.QFrame):

    def __init__(self, page, category: int = 0, name: str = '',
                 code: str = '', price: float = 1.99, image: str = ''):

        self.page = page
        self.ui = self.page.ui
        self.commands = self.page.commands

        self.parent_layout = self.get_layout(category)
        super(ItemCard, self).__init__(self.parent_layout)

        self.name = camelify(name)
        self.display_name = name
        self.code = code
        self.price = price
        self.image = image

        self.bought = False

        self.draw_ui()

    def get_layout(self, category):
        if category == 1:
            return self.ui.verticalLayout_3
        elif category == 2:
            return self.ui.verticalLayout_42
        elif category == 3:
            return self.ui.verticalLayout_44
        elif category == 4:
            return self.ui.verticalLayout_40
        elif category == 5:
            return self.ui.verticalLayout_46
        else:
            return self.ui.allLayout

    def add_item(self):
        """Add item to the cart section after add button pressed."""

        self.amount = self.spinBox.value()

        if self.amount > 0:
            if self.bought:
                self.update_cart()
            else:
                self.add_to_cart()
        elif self.amount == 0 and self.bought:
            self.update_cart()
            self.cart_item.delete_item()

    def update_cart(self):
        """Updates items in cart."""

        new_price = self.amount*self.price - \
            float(self.cart_item.sumPrice.text().rstrip(' €'))
        self.page.update_price(new_price)

        self.update_cart_item()

    def update_cart_item(self):
        """Update the UI of cart item"""

        self.cart_item.priceLabel.setText(
            str(self.amount)+" ks x "+str(self.price))
        self.cart_item.sumPrice.setText(
            str_price(self.price, self.amount)+" €")

    def add_to_cart(self):
        """Adds new item to the cart."""

        self.cart_item = CartItem(self, self.ui.cartLayout,
                                  self.display_name, self.price, self.amount)

        self.page.update_price(self.amount*self.price)
        self.update_button()

    def update_button(self):
        self.bought = not self.bought

        if not self.bought:
            self.spinBox.setValue(0)
            self.itemButton.setMaximumWidth(110)
            self.addButton.setText("Add to cart")
        else:
            self.itemButton.setMaximumWidth(130)
            self.addButton.setText("Update amount")

    def draw_ui(self):
        self.setMinimumSize(QtCore.QSize(200, 60))
        self.setMaximumSize(QtCore.QSize(16777215, 60))
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setObjectName(self.name)
        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName(self.name+"Layout")
        self.itemPreview = QtWidgets.QWidget(self)
        self.itemPreview.setMaximumSize(QtCore.QSize(60, 16777215))
        self.itemPreview.setObjectName(self.name+"Preview")
        self.previewLayout = QtWidgets.QVBoxLayout(self.itemPreview)
        self.previewLayout.setObjectName(self.name+"PreviewLayout")
        self.previewLayout.setContentsMargins(0, 0, 0, 0)
        self.previewLayout.setSpacing(0)
        self.itemImage = QtWidgets.QLabel()
        self.itemImage.setPixmap(QtGui.QPixmap(self.image))
        self.itemImage.setScaledContents(True)
        self.itemImage.setWordWrap(True)
        self.itemImage.setObjectName(self.name+"Image")
        self.previewLayout.addWidget(self.itemImage)
        self.mainLayout.addWidget(self.itemPreview)
        self.itemName = QtWidgets.QWidget(self)
        self.itemName.setObjectName(self.name+"Name")
        self.nameLayout = QtWidgets.QVBoxLayout(self.itemName)
        self.nameLayout.setObjectName(self.name+"NameLayout")
        self.itemLabel = QtWidgets.QLabel(self.display_name+" #"+self.code)
        self.itemLabel.setObjectName(self.name+"ItemLabel")
        self.nameLayout.addWidget(self.itemLabel)
        self.mainLayout.addWidget(self.itemName)
        self.itemCount = QtWidgets.QWidget(self)
        self.itemCount.setMaximumSize(QtCore.QSize(60, 16777215))
        self.itemCount.setObjectName(self.name+"Count")
        self.countLayout = QtWidgets.QVBoxLayout(self.itemCount)
        self.countLayout.setObjectName(self.name+"CountLayout")
        self.spinBox = QtWidgets.QSpinBox(self.itemCount)
        self.spinBox.setObjectName(self.name+"SpinBox")
        self.countLayout.addWidget(self.spinBox)
        self.mainLayout.addWidget(self.itemCount)
        self.itemButton = QtWidgets.QWidget(self)
        self.itemButton.setMaximumSize(QtCore.QSize(110, 16777215))
        self.itemButton.setObjectName(self.name+"Button")
        self.buttonLayout = QtWidgets.QVBoxLayout(self.itemButton)
        self.buttonLayout.setObjectName(self.name+"ButtonLayout")
        self.addButton = QtWidgets.QPushButton("Add to cart")
        self.addButton.setMinimumHeight(24)
        self.addButton.setObjectName(self.name+"AddButton")
        self.addButton.setStyleSheet(
            "QPushButton {font-weight: bold; border: 4px solid #2f3e46; border-radius: 12px;background-color: #2f3e46;color: #cad2c5;} QPushButton:hover {border-color: #354f52; background-color: #354f52;} QPushButton:pressed {border-color: #354f52;background-color: #354f52;}")
        self.commands.button_click(self.addButton, self.add_item)
        self.buttonLayout.addWidget(self.addButton)
        self.mainLayout.addWidget(self.itemButton)
        self.parent_layout.addWidget(self)


class CartItem(QtWidgets.QFrame):

    def __init__(self, item, layout, name: str,
                 price: float, amount: int):

        super(CartItem, self).__init__(layout.parent())

        self.page = item.page
        self.item = item
        self.ui = self.page.ui
        self.commands = self.page.commands

        self.parent_layout = layout

        self.name = "cart"+camelify(name)
        self.display_name = name
        self.price = price
        self.amount = amount

        self.draw_ui()

    def delete_item(self):
        """Delete this item from cart."""

        self.item.update_button()
        self.deleteLater()

    def draw_ui(self):
        self.setMaximumSize(QtCore.QSize(16777215, 40))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setObjectName(self.name)
        self.mainLayout = QtWidgets.QHBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setObjectName(self.name+"Layout")
        self.itemInfo = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.itemInfo.sizePolicy().hasHeightForWidth())
        self.itemInfo.setSizePolicy(sizePolicy)
        self.itemInfo.setObjectName(self.name+"Info")
        self.infoLayout = QtWidgets.QVBoxLayout(self.itemInfo)
        self.infoLayout.setContentsMargins(0, 0, 0, 0)
        self.infoLayout.setSpacing(0)
        self.infoLayout.setObjectName(self.name+"InfoLayout")
        self.itemName = QtWidgets.QWidget(self.itemInfo)
        self.itemName.setObjectName(self.name+"ItemName")
        self.label = QtWidgets.QLabel(self.display_name, self.itemName)
        self.label.setGeometry(QtCore.QRect(6, 0, 131, 20))
        self.label.setStyleSheet("color: rgb(223, 223, 223);")
        self.label.setObjectName(self.name+"Label")
        self.infoLayout.addWidget(self.itemName)
        self.itemPrice = QtWidgets.QWidget(self.itemInfo)
        self.itemPrice.setObjectName(self.name+"itemPrice")
        self.priceLayout = QtWidgets.QHBoxLayout(self.itemPrice)
        self.priceLayout.setContentsMargins(6, 0, 0, 0)
        self.priceLayout.setSpacing(20)
        self.priceLayout.setObjectName(self.name+"PriceLayout")
        self.priceLabel = QtWidgets.QLabel(
            str(self.amount)+" ks x "+str(self.price))
        self.priceLabel.setStyleSheet("color: rgb(223, 223, 223);")
        self.priceLabel.setObjectName(self.name+"PriceLabel")
        self.priceLayout.addWidget(self.priceLabel)
        self.sumPrice = QtWidgets.QLabel(
            str_price(self.price, self.amount)+" €")
        self.sumPrice.setStyleSheet("color: rgb(223, 223, 223);")
        self.sumPrice.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.sumPrice.setObjectName(self.name+"SumPrice")
        self.priceLayout.addWidget(self.sumPrice)
        self.infoLayout.addWidget(self.itemPrice)
        self.mainLayout.addWidget(self.itemInfo)
        self.cancelSection = QtWidgets.QWidget(self)
        self.cancelSection.setMinimumSize(QtCore.QSize(40, 40))
        self.cancelSection.setObjectName(self.name+"CancelSection")
        self.cancelButton = QtWidgets.QPushButton(self.cancelSection)
        self.cancelButton.setGeometry(QtCore.QRect(10, 10, 20, 20))
        self.cancelButton.setStyleSheet(
            "border: none; color: rgb(125, 125, 125);")
        crossIcon = QtGui.QIcon()
        crossIcon.addPixmap(QtGui.QPixmap(
            "../../assets/icons/x-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancelButton.setIcon(crossIcon)
        self.cancelButton.setIconSize(QtCore.QSize(10, 10))
        self.cancelButton.setObjectName(self.name+"CancelButton")
        self.commands.button_click(self.cancelButton, self.delete_item)
        self.mainLayout.addWidget(
            self.cancelSection, 0, QtCore.Qt.AlignRight)
        self.parent_layout.addWidget(self)
