# Modul Sklad -
# Show amount of products.
# Alerts you to products with low quantity.
# Can generate (automatic/half-automatic/manual) order,
# creating objednavka_[id_transakcie].txt

from PyQt5 import QtWidgets, QtCore, QtGui

from utils.ui_commands import UI_Commands
from utils.tools import *
from utils.file import DataFile
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap
from utils.ENV_VARS import PATH


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

        self.cart_price = 0
        self.cart = {}
        self.catalog = []
        self.category= 0

        # Track UI actions
        self.button_clicks()

        # Init category layouts
        self.layouts=[self.ui.verticalLayout_18,self.ui.verticalLayout_37,self.ui.verticalLayout_20,self.ui.verticalLayout_28,
                        self.ui.verticalLayout_31,self.ui.verticalLayout_35]

         # Load data
        self.goods = DataFile('tovar')
        self.prices = DataFile('cennik')
        self.storage = DataFile('sklad')
        self.load_items(self.goods.data)

        # Track UI actions
        self.redirect_action()
        self.search_action()
        self.sort_action()
        self.buy_action()
        self.catalog_action()

        # Update 'goods' variable every 3 seconds
        self.version = self.goods.version
        run_periodically(self.update_goods, 3)
    # ==================== ACTIONS =======================
    def redirect_action(self):
        self.commands.buttons_click(
            [self.ui.skladButton, self.ui.homeArrow4],
            self.switch_screen
        )

    def search_action(self):
        self.commands.form_submit(
            [self.ui.searchButton, self.ui.searchField_3],
            self.search
        )

    def sort_action(self):
        self.commands.button_click(
            self.ui.sortButton, self.sort
        )
    
    def buy_action(self):
        self.commands.button_click(
            self.ui.buyButton_7, self.buy
        )

    def catalog_action(self):
        self.commands.tab_selected(
            self.ui.itemCategories, self.set_category
        )

    # ==================== MAIN FUNCTIONALITY =======================
    def switch_screen(self):
        """Redirect to this sklad screen."""

        self.commands.redirect(self.ui.sklad)

    def search(self):
        """
        Get the value of the search field and load
        items with matching names or codes.
        """

        self.query = self.ui.searchField_3.text()
        self.result = search_items(self.query, category=self.category)
        self.reload_items()

    def sort(self):
        """Update sort button and change sort state."""

        if self.sort_state == 1:
            self.create_icon("up_arrow.png", "Highest price", 2)
        elif self.sort_state == 2:
            self.create_icon("down_arrow.png", "Lowest price", 3)
        else:
            self.create_icon("up_down_arrow.png", "Sort by price", 1)

        self.result = sort_items(self.sort_state)
        print(self.result)
    
    def buy(self):
        """Buy everything in the cart, generate objednavka_[id].txt"""

        self.create_receipt()
        for item in self.cart.values():
            item.delete()

    def set_category(self):
        """Set currently selected category."""

        self.category = self.ui.itemCategories.currentIndex()
    # ==================== HELPER FUNCTIONS =======================
    def create_icon(self, icon_name, text, new_state):
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(find_icon(icon_name)),
            QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.ui.sortButton.setText(text)
        self.sort_state = new_state

        self.ui.sortButton.setIcon(icon)

    def reload_items(self):
        self.catalog = []
        self.commands.clear_layout(self.layouts[self.category])
        self.load_items(self.result, all_layouts=False)

    def load_items(self, data, all_layouts= True):
        """Load all items from database into catalog."""

        for key, vals in data.items():
            self.load_item(key, vals,all_layouts)

    def load_item(self, key, vals, all_layouts):
        price = self.prices.data.get(key)
        name = camelify(vals[0])
        count = self.storage.data.get(key)
        if name not in self.catalog:
            image = find_image(vals[1])
            ItemCard(self, self.layouts[int(key[0])],
                    vals[0], key, float(price[0]), image, int(count[0]))
        if name not in self.catalog and int(count[0])<10:
            ItemCard(self, self.ui.verticalLayout_18,
                    vals[0], key, float(price[0]), image, int(count[0]))

        self.catalog.append(name)
    
    def create_receipt(self):
        receipt_id = random_id('N')
        filename = 'objednavka_'+receipt_id+'.txt'
        filepath = os.path.join(PATH, 'source', 'data', filename)

        with open(filepath, 'w', encoding='utf-8') as receipt:
            self.receipt_template(receipt, receipt_id)

        receipt_icon = QtGui.QIcon()
        msg = QMessageBox()
        
        receipt_icon.addPixmap(QtGui.QPixmap(find_icon('receipt.svg')),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msg.setWindowTitle(f"Sale {receipt_id[1:]} - confirmed")
        msg.setText('<b><p style="padding: 0px;  margin: 0px;">Pokladničný doklad bol úspešne vygenerovaný.</p>' + f'<br><a href="file:///{PATH}/source/data/{filename}">Otvor objednávku č. {receipt_id}</a>')
        msg.setIconPixmap(QPixmap(find_icon('receipt.svg')))
        msg.exec_()

    def receipt_template(self, receipt, id):
        receipt.write('Camels E-shop s.r.o.\n')
        receipt.write('\nCislo objednavky: '+id)
        receipt.write('\nVytvorene: '+now())
        receipt.write('\n\n=================================\n\n')
        items = [
            item.display_name+'\n\t'+str(item.amount)+'ks x ' +
            str_price(item.price)+'\t\t\t\t' +
            str_price(item.price, item.amount)+' €\n'
            for item in list(self.cart.values())
        ]
        receipt.writelines(items)
        receipt.write('\n=================================\n\n')
        receipt.write('Spolu cena: '+str_price(self.cart_price)+' €')
        receipt.write('\nDPH(20%): '+str_price(self.cart_price*0.2)+' €')

    # ==================== SKLAD UPDATING =======================
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
        self.ui.totalPrice_2.setText(
            "Spolu: "+str_price(self.cart_price, 1)+" €")

    #===================SORT BUTTON STATE==================================

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
            [self.ui.searchButton_3, self.ui.searchField_3],
            self.search)

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

        self.in_cart = False

        self.draw_ui()

    def button_press(self):
        self.amount = self.spinBox.value()

        if self.in_cart:
            self.update_cart()
        else:
            self.add_to_cart()

    def update_cart(self):
        if self.amount != self.cart_item.amount:
            if self.amount == 0:
                self.cart_item.delete()
            else:
                self.cart_item.update(self.amount)

    def add_to_cart(self):
        if self.amount > 0:
            self.cart_item = CartItem(
                self, self.display_name, self.price, self.amount
            )
            self.update_status()

    def update_status(self):
        self.in_cart = not self.in_cart
        self.update_button()

    def update_button(self):
        if self.in_cart:
            self.itemButton.setMaximumWidth(130)
            self.addButton.setText("Update amount")
        else:
            self.spinBox.setValue(0)
            self.itemButton.setMaximumWidth(110)
            self.addButton.setText("Add to cart")

    def draw_ui(self):
        self.setMinimumSize(QtCore.QSize(200, 60))
        self.setMaximumSize(QtCore.QSize(16777215, 60))
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        if self.parent_layout == self.ui.verticalLayout_18:
            self.setStyleSheet("background-color: rgb(255, 240, 245)")
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
        self.commands.button_click(self.addButton, self.button_press)
        self.buttonLayout.addWidget(self.addButton)
        self.mainLayout_2.addWidget(self.itemButton)
        self.parent_layout.addWidget(self)

class CartItem(QtWidgets.QFrame):

    def __init__(self, item, name: str, price: float, amount: int):
        self.item = item
        self.page = item.page
        self.ui = self.page.ui
        self.commands = self.page.commands
        self.parent_layout = self.ui.verticalLayout_21

        super(CartItem, self).__init__(self.parent_layout.parent())

        self.name = "cart"+camelify(name)
        self.display_name = name

        self.price = price
        self.amount = amount
        self.total = price*amount
        self.update_page_cart()
        self.page.update_price(self.total)

        self.draw_ui()

    def delete(self):
        """Delete this item from cart."""
        self.item.update_status()
        self.price_change(0)
        self.deleteLater()

    def update(self, amount):
        self.price_change(amount)
        self.priceLabel.setText(
            str(self.amount)+" ks x "+str(self.price))
        self.sumPrice.setText(
            str_price(self.price, self.amount)+" €")

    def price_change(self, amount):
        new_price = amount*self.price - self.amount*self.price
        self.amount = amount
        self.update_page_cart()
        self.page.update_price(new_price)

    def update_page_cart(self):
        self.page.cart[self.name] = self

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
            str_price(self.price, self.amount)+" €")
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
        self.commands.button_click(self.cancelButton, self.delete)
        self.mainLayout_2.addWidget(
            self.cancelSection, 0, QtCore.Qt.AlignRight)
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