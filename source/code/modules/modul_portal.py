# Modul Portal -
# Lists catalog of available products, has an option
# to search by code/name and to filter products.
# After ordering the selected items in given amounts,
# creates file uctenka_[id_transakcie].txt.

from PyQt5 import QtWidgets, QtCore, QtGui

from utils.ui_commands import UI_Commands


class Portal:

    def __init__(self, ui):
        """
        This class handles everything done on the portal
        screen (button clicks, item listing...).
        """

        self.ui = ui
        self.commands = UI_Commands(self.ui)

        self.commands.button_click(
            self.ui.portalButton, self.switch_screen)
        self.commands.button_click(
            self.ui.add, self.add_item)

        # Read file 'tovar.txt' - not in prototype
        # self.tovar = DataFile('tovar')
        # self.goods = self.tovar.read()
        # self.version = self.tovar.get_version()

        # Update 'goods' variable every 3 seconds
        # tools.run_periodically(self.update_goods, 3)

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

        self.commands.change_screen(self.ui.portal)

    def add_item(self):
        """Add item card to catalog."""

        ItemCard(self.ui, self.ui.shirtsContents,
                 "testItem", "TEST ITEM", "4444")


class ItemCard(QtWidgets.QFrame):

    def __init__(self, ui, parent, name: str, display_name: str, code: str):
        super(ItemCard, self).__init__(parent)

        self.ui = ui
        self.name = name
        self.display_name = display_name
        self.code = code

        self.draw_ui()

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
        self.itemImage = QtWidgets.QLabel("image preview")
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
        self.itemButton.setMaximumSize(QtCore.QSize(80, 16777215))
        self.itemButton.setObjectName(self.name+"Button")
        self.buttonLayout = QtWidgets.QVBoxLayout(self.itemButton)
        self.buttonLayout.setObjectName(self.name+"ButtonLayout")
        self.addButton = QtWidgets.QPushButton("Add to cart")
        self.addButton.setObjectName(self.name+"AddButton")
        self.buttonLayout.addWidget(self.addButton)
        self.mainLayout.addWidget(self.itemButton)
        self.ui.verticalLayout_3.addWidget(self)


class CartItem(QtWidgets.QFrame):

    def __init__(self, ui, parent, name: str, display_name: str, price: float, amount: int):
        super(ItemCard, self).__init__(parent)

        self.ui = ui
        self.name = "cart"+name
        self.display_name = display_name
        self.price = price
        self.amount = amount

        self.draw_ui()

    def draw_ui(self):
        self.cartItem = QtWidgets.QFrame(self.cartContents)
        self.cartItem.setMaximumSize(QtCore.QSize(16777215, 40))
        self.cartItem.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cartItem.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cartItem.setObjectName("cartItem")
        self.widget1 = QtWidgets.QWidget(self.cartItem)
        self.widget1.setGeometry(QtCore.QRect(0, 0, 281, 43))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.itemInfo = QtWidgets.QWidget(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.itemInfo.sizePolicy().hasHeightForWidth())
        self.itemInfo.setSizePolicy(sizePolicy)
        self.itemInfo.setObjectName("itemInfo")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.itemInfo)
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.cartItemName = QtWidgets.QWidget(self.itemInfo)
        self.cartItemName.setObjectName("cartItemName")
        self.label = QtWidgets.QLabel(self.cartItemName)
        self.label.setGeometry(QtCore.QRect(6, 0, 131, 20))
        self.label.setStyleSheet("color: rgb(223, 223, 223);")
        self.label.setObjectName("label")
        self.verticalLayout_12.addWidget(self.cartItemName)
        self.cartItemPrice = QtWidgets.QWidget(self.itemInfo)
        self.cartItemPrice.setObjectName("cartItemPrice")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.cartItemPrice)
        self.horizontalLayout_4.setContentsMargins(6, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.cartItemPrice)
        self.label_2.setStyleSheet("color: rgb(223, 223, 223);")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.cartItemPrice)
        self.label_3.setStyleSheet("color: rgb(223, 223, 223);")
        self.label_3.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.verticalLayout_12.addWidget(self.cartItemPrice)
        self.horizontalLayout_3.addWidget(self.itemInfo)
        self.cancelSection = QtWidgets.QWidget(self.widget1)
        self.cancelSection.setMinimumSize(QtCore.QSize(40, 0))
        self.cancelSection.setObjectName("cancelSection")
        self.searchButton_2 = QtWidgets.QPushButton(self.cancelSection)
        self.searchButton_2.setGeometry(QtCore.QRect(15, 15, 10, 10))
        self.searchButton_2.setStyleSheet("border: none;\n"
                                          "color: rgb(125, 125, 125);")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(
            "../../assets/icons/x-button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.searchButton_2.setIcon(icon3)
        self.searchButton_2.setIconSize(QtCore.QSize(10, 10))
        self.searchButton_2.setObjectName("searchButton_2")
        self.horizontalLayout_3.addWidget(
            self.cancelSection, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_11.addWidget(self.cartItem)
