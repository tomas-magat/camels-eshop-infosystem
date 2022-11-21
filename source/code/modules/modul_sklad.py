# Modul Sklad -
# Show amount of products.
# Alerts you to products with low quantity.
# Can generate (automatic/half-automatic/manual) order,
# creating objednavka_[id_transakcie].txt

from PyQt5 import QtWidgets, QtCore, QtGui

from utils.ui_commands import UI_Commands
from utils import tools

class Sklad:

    def __init__(self, ui):
        """
        This class handles everything done on the sklad
        screen (button clicks, item listing...).
        """

        self.ui = ui
        self.commands = UI_Commands(self.ui)
        self.total_price = 0

        self.create_item_cards(6)
        self.button_clicks()

    def update_goods(self):
        """
        Update 'goods' variable if version of the tovar.txt
        datafile has changed.
        """

        current_version = self.tovar.get_version()

        if current_version != self.version:
            self.goods = self.tovar.read()
            self.version = current_version

    def switch_screen(self):
        """Redirect to this portal screen."""

        self.commands.redirect(self.ui.portal)

    def update_price(self, value):
        """Update total price of a cart."""

        self.total_price += value
        self.ui.totalPrice_2.setText(
            "Spolu: "+tools.str_price(self.total_price, 1))

    def create_item_cards(self, n):
        """Creates n new item cards in the portal screen catalog."""

        for i in range(n):
            ItemCard(self, self.ui.shirtsCatalog_2, "test" +
                     str(i), "Test "+str(i), "0000")

    def button_clicks(self):
        """All button click commands of portal screen here."""

        self.commands.button_click(
            self.ui.skladButton, self.switch_screen)


class ItemCard(QtWidgets.QFrame):

    def __init__(self, page, parent, name: str,
                 display_name: str, code: str):

        super(ItemCard, self).__init__(parent)

        self.page = page
        self.ui = self.page.ui
        self.commands = self.page.commands

        self.name = name
        self.display_name = display_name
        self.code = code

        self.draw_ui()

    def add_to_cart(self):
        """Add item to the cart section after add button pressed."""

        self.amount = self.spinBox.value()

        if self.amount > 0:
            price = 15.99
            CartItem(self.page, self.ui.contentsSection_2, self.name,
                     self.display_name, price, self.amount)

            self.page.update_price(price*self.amount)

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
        self.itemImage = QtWidgets.QLabel("image preview")
        self.itemImage.setWordWrap(True)
        self.itemImage.setObjectName(self.name+"Image")
        self.previewLayout.addWidget(self.itemImage)
        self.mainLayout_2.addWidget(self.itemPreview)
        self.itemName = QtWidgets.QWidget(self)
        self.itemName.setObjectName(self.name+"Name")
        self.nameLayout = QtWidgets.QVBoxLayout(self.itemName)
        self.nameLayout.setObjectName(self.name+"NameLayout")
        self.itemLabel = QtWidgets.QLabel(self.display_name+" #"+self.code)
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
        self.itemButton.setMaximumSize(QtCore.QSize(80, 16777215))
        self.itemButton.setObjectName(self.name+"Button")
        self.buttonLayout = QtWidgets.QVBoxLayout(self.itemButton)
        self.buttonLayout.setObjectName(self.name+"ButtonLayout")
        self.addButton = QtWidgets.QPushButton("Add to cart")
        self.addButton.setObjectName(self.name+"AddButton")
        self.commands.button_click(self.addButton, self.add_to_cart)
        self.buttonLayout.addWidget(self.addButton)
        self.mainLayout_2.addWidget(self.itemButton)
        self.ui.verticalLayout_5.addWidget(self)

class CartItem(QtWidgets.QFrame):

    def __init__(self, page, parent, name: str,
                 display_name: str, price: float, amount: int):

        super(CartItem, self).__init__(parent)

        self.page = page
        self.ui = self.page.ui
        self.commands = self.page.commands

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
            tools.str_price(self.price, self.amount))
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
        self.ui.verticalLayout_12.addWidget(self)