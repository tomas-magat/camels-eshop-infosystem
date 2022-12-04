# Modul Sklad -
# Show amount of products.
# Alerts you to products with low quantity.
# Can generate (automatic/half-automatic/manual) order,
# creating objednavka_[id_transakcie].txt

from PyQt5 import QtWidgets, QtCore, QtGui

from utils.ui_commands import UI_Commands
from utils.tools import *
from utils.file import DataFile


class Sklad:

    def __init__(self, ui):
        """
        This class handles everything done on the sklad
        screen (button clicks, item listing...).
        """

        self.ui = ui
        self.commands = UI_Commands(self.ui)

        # Init global variables
        self.total_price = 0
        self.sort_state = 1
        self.order_mode = 3
        self.catalog = []
        self.layouts=[(self.ui.verticalLayout_18,0),(self.ui.verticalLayout_37,1),(self.ui.verticalLayout_20,2),(self.ui.verticalLayout_28,3),
                    (self.ui.verticalLayout_31,4),(self.ui.verticalLayout_35,5)]
        # Track UI actions
        self.button_clicks()

         # Load data
        self.goods = DataFile('tovar')
        self.prices = DataFile('cennik')
        self.storage = DataFile('sklad')
        self.load_items(self.goods.data)

        # Update 'goods' variable every 3 seconds
        self.version = self.goods.version
        run_periodically(self.update_goods, 3)

    
    def load_items(self, data):
        """Load all items from database into catalog."""

        for key, vals in data.items():
            self.load_item(key, vals)

    def load_item(self, key, vals):
        price = self.prices.data.get(key)
        name = camelify(vals[0])
        count = self.storage.data.get(key)
        for layout in self.layouts:
            if name not in self.catalog:
                image = find_image(vals[1])
                ItemCard(self, layout[0],
                        vals[0], key, float(price[1]), image, int(count[0]))

                self.catalog.append(name)

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

    def switch_screen(self):
        """Redirect to this sklad screen."""

        self.commands.redirect(self.ui.sklad)

    def search_items(self):
        """
        Get the value of the search field and return
        list of matching item names or codes.
        """

        self.query = self.ui.searchField.text()
        self.result = search_items(self.query)
        print(self.result)

    def update_price(self, value):
        """Update total price of a cart."""

        self.total_price += value
        self.ui.totalPrice_2.setText(
            "Spolu: " + str_price(self.total_price, 1))

    def create_item_cards(self, n):
        """Creates n new item cards in the sklad screen catalog."""

        for i in range(n):
            ItemCard(self, self.ui.verticalLayout_20, "test" +
                     str(i), "Test "+str(i), "0000", "Na sklade: 5", find_image("question_mark.png"))
        for i in range(n):
            ItemCard(self, self.ui.verticalLayout_18, "test" +
                     str(i), "Test "+str(i), "0000", "Na sklade: 2", find_image("question_mark.png"))
        for i in range(n):
            ItemCard(self, self.ui.verticalLayout_37, "test" +
                     str(i), "Test "+str(i), "0000", "Na sklade: 5", find_image("question_mark.png"))
        for i in range(n):
            ItemCard(self, self.ui.verticalLayout_28, "test" +
                     str(i), "Test "+str(i), "0000", "Na sklade: 5", find_image("question_mark.png"))
        for i in range(n):
            ItemCard(self, self.ui.verticalLayout_31, "test" +
                     str(i), "Test "+str(i), "0000", "Na sklade: 5", find_image("question_mark.png"))
        for i in range(n):
            ItemCard(self, self.ui.verticalLayout_35, "test" +
                     str(i), "Test "+str(i), "0000", "Na sklade: 5", find_image("question_mark.png"))

    def sort_button_state(self):
        """Update sort button state and change its icon."""

        icon = QtGui.QIcon()

        if self.sort_state == 1:
            icon.addPixmap(QtGui.QPixmap(
                find_icon("up_arrow.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.sortButton_2.setText("Highest price")
            self.sort_state = 2

        elif self.sort_state == 2:
            icon.addPixmap(QtGui.QPixmap(
                find_icon("down_arrow.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.sortButton_2.setText("Lowest price")
            self.sort_state = 3

        else:
            icon.addPixmap(QtGui.QPixmap(
                find_icon("up_down_arrow.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.sortButton_2.setText("Sort by price")
            self.sort_state = 1

        self.ui.sortButton_2.setIcon(icon)

    def order(self):
        print(self.order_mode)

    def automatic(self):
        self.order_mode= 1
        self.order()

    def semiautomatic(self):
        self.order_mode= 2
        self.order()

    def manual(self):
        self.order_mode= 3
        self.order()

    def button_clicks(self):
        """All button click commands of sklad screen here."""

        self.commands.button_click(
            self.ui.skladButton, self.switch_screen)

        self.commands.form_submit(
            [self.ui.searchButton_3, self.ui.searchField],
            self.search_items)

        self.commands.button_click(
            self.ui.sortButton_2, self.sort_button_state)

        self.commands.button_click(
            self.ui.automatic, self.automatic)

        self.commands.button_click(
            self.ui.semiautomatic, self.semiautomatic)

        self.commands.button_click(
            self.ui.manual, self.manual)


class ItemCard(QtWidgets.QFrame):

    def __init__(self, page, layout, name: str,
                 code: str, price: float, image: str, count: float):

        super(ItemCard, self).__init__(layout.parent())

        self.page = page
        self.ui = self.page.ui
        self.commands = self.page.commands

        self.parent_layout = layout

        self.name = camelify(name)
        self.display_name = name
        self.code = code
        self.price = price
        self.image = image
        self.count = count

        self.bought = False

        self.draw_ui()

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
            self.update_button()
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

        self.cart_item = CartItem(self.page, self.ui.verticalLayout_34, self.name,
                                  self.display_name, self.price, self.amount)

        self.page.update_price(self.amount*self.price)

        self.update_button()

    def update_button(self):
        self.bought = not self.bought

        if not self.bought:
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
        self.mainLayout_2 = QtWidgets.QHBoxLayout(self)
        self.mainLayout_2.setContentsMargins(0, 0, 0, 0)
        self.mainLayout_2.setSpacing(0)
        self.mainLayout_2.setObjectName(self.name+"Layout")
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
        self.mainLayout_2.addWidget(self.itemPreview)
        self.itemName = QtWidgets.QWidget(self)
        self.itemName.setObjectName(self.name+"Name")
        self.nameLayout = QtWidgets.QVBoxLayout(self.itemName)
        self.nameLayout.setObjectName(self.name+"NameLayout")
        self.itemLabel = QtWidgets.QLabel(self.display_name+"  #"+self.code+"\nCena:"+str(self.price)+" €"+"    Na sklade: "+ str(self.count))
        self.itemLabel.setObjectName(self.name+"ItemLabel")
        self.nameLayout.addWidget(self.itemLabel)
        self.mainLayout_2.addWidget(self.itemName)
        self.itemCount = QtWidgets.QWidget(self)
        self.itemCount.setMaximumSize(QtCore.QSize(60, 16777215))
        self.itemCount.setObjectName(self.name+"Count")
        self.countLayout = QtWidgets.QVBoxLayout(self.itemCount)
        self.countLayout.setObjectName(self.name+"CountLayout")
        self.spinBox = QtWidgets.QSpinBox(self.itemCount)
        self.spinBox.setObjectName(self.name+"SpinBox")
        self.countLayout.addWidget(self.spinBox)
        self.mainLayout_2.addWidget(self.itemCount)
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
        self.mainLayout_2.addWidget(self.itemButton)
        self.parent_layout.addWidget(self)

    def draw_ui_1(self):
        self.setMinimumSize(QtCore.QSize(200, 60))
        self.setMaximumSize(QtCore.QSize(16777215, 60))
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        if self.parent_layout == self.ui.verticalLayout_18:
            self.setStyleSheet("background-color: rgb(255,64,64)")
        self.setObjectName(self.name)
        self.mainLayout_2 = QtWidgets.QHBoxLayout(self)
        self.mainLayout_2.setContentsMargins(0, 0, 0, 0)
        self.mainLayout_2.setSpacing(0)
        self.mainLayout_2.setObjectName(self.name+"Layout")
        self.itemPreview = QtWidgets.QWidget(self)
        self.itemPreview.setMaximumSize(QtCore.QSize(60, 16777215))
        self.itemPreview.setObjectName(self.name+"Preview")
        self.previewLayout = QtWidgets.QVBoxLayout(self.itemPreview)
        self.previewLayout.setObjectName(self.name+"PreviewLayout")
        self.itemImage = QtWidgets.QLabel()
        self.itemImage.setPixmap(QtGui.QPixmap(self.image))
        self.itemImage.setScaledContents(True)
        self.itemImage.setWordWrap(True)
        self.itemImage.setObjectName(self.name+"Image")
        self.previewLayout.addWidget(self.itemImage)
        self.mainLayout_2.addWidget(self.itemPreview)
        self.itemName = QtWidgets.QWidget(self)
        self.itemName.setObjectName(self.name+"Name")
        self.nameLayout = QtWidgets.QVBoxLayout(self.itemName)
        self.nameLayout.setObjectName(self.name+"NameLayout")
        self.itemLabel = QtWidgets.QLabel(self.display_name+"  #"+self.code+
                                          "  Cena: 5,99€   " + "self.count")
        self.itemLabel.setObjectName(self.name+"ItemLabel")
        self.nameLayout.addWidget(self.itemLabel)
        self.mainLayout_2.addWidget(self.itemName)
        self.itemCount = QtWidgets.QWidget(self)
        self.itemCount.setMaximumSize(QtCore.QSize(60, 16777215))
        self.itemCount.setObjectName(self.name+"Count")
        self.countLayout = QtWidgets.QVBoxLayout(self.itemCount)
        self.countLayout.setObjectName(self.name+"CountLayout")
        self.spinBox = QtWidgets.QSpinBox(self.itemCount)
        self.spinBox.setStyleSheet("QSpinBox"
                                   "{"
                                   "background-color : white;"
                                   "}")
        self.spinBox.setObjectName(self.name+"SpinBox")
        self.countLayout.addWidget(self.spinBox)
        self.mainLayout_2.addWidget(self.itemCount)
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
        self.commands.button_click(self.addButton, self.add_to_cart)
        self.buttonLayout.addWidget(self.addButton)
        self.mainLayout_2.addWidget(self.itemButton)
        self.parent_layout.addWidget(self)


class CartItem(QtWidgets.QFrame):

    def __init__(self, page, layout, name: str,
                 display_name: str, price: float, amount: int):

        super(CartItem, self).__init__(layout.parent())

        self.page = page
        self.ui = self.page.ui
        self.commands = self.page.commands

        self.parent_layout = layout

        self.name = "cart"+name
        self.display_name = display_name
        self.price = price
        self.amount = amount

        self.draw_ui()

    def delete_item(self):
        """Delete this item from cart."""

        self.deleteLater()
        self.page.update_price(-self.price*self.amount)

    def draw_ui(self):
        self.setMaximumSize(QtCore.QSize(16777215, 40))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setObjectName(self.name)
        self.mainLayout_2 = QtWidgets.QHBoxLayout(self)
        self.mainLayout_2.setContentsMargins(0, 0, 0, 0)
        self.mainLayout_2.setObjectName(self.name+"Layout")
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
            str_price(self.price, self.amount))
        self.sumPrice.setStyleSheet("color: rgb(223, 223, 223);")
        self.sumPrice.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.sumPrice.setObjectName(self.name+"SumPrice")
        self.priceLayout.addWidget(self.sumPrice)
        self.infoLayout.addWidget(self.itemPrice)
        self.mainLayout_2.addWidget(self.itemInfo)
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
        self.mainLayout_2.addWidget(
            self.cancelSection, 0, QtCore.Qt.AlignRight)
        self.parent_layout.addWidget(self)
