# Modul Portal -
# Lists catalog of available products, has an option
# to search by code/name and to filter products.
# After buying the selected items in given amounts,
# creates file uctenka_[id_transakcie].txt.

from PyQt5 import QtWidgets, QtCore, QtGui

from utils.tools import *


class Portal:
    """
    This class handles everything done on the portal
    screen (button clicks, item listing...).
    """

    def __init__(self, app):
        self.ui = app.ui
        self.commands = app.commands
        self.data = app.data

        # Init category layouts
        self.layouts = [
            self.ui.allLayout,
            self.ui.verticalLayout_3,
            self.ui.verticalLayout_40,
            self.ui.verticalLayout_42,
            self.ui.verticalLayout_44,
            self.ui.verticalLayout_46
        ]

        self.init_actions()
        self.init_data()

        # Init global variables
        self.cart = Cart(self)
        self.cashier_name = ""
        self.sort_state = 1

    def init_actions(self):
        self.redirect_actions()
        self.search_action()
        self.sort_action()
        self.login_actions()
        self.catalog_action()

    def init_data(self):
        self.goods = self.data['tovar']
        self.prices = self.data['cennik']
        self.storage = self.data['sklad']
        self.goods.version_changed(self.reload_items)
        self.ui.itemCategories.setCurrentIndex(0)
        self.update_category()

    # ==================== ACTIONS =======================
    def redirect_actions(self):
        self.commands.button_click(
            self.ui.portalButton,
            self.switch_screen
        )
        self.commands.button_click(
            self.ui.homeArrow6,
            self.exit_login
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
            lambda: self.commands.redirect(self.ui.login)
        )
        self.commands.form_submit(
            [self.ui.nameEntry, self.ui.loginButton],
            self.log_in
        )

    def catalog_action(self):
        self.commands.tab_selected(
            self.ui.itemCategories, self.update_category
        )

    # ==================== REDIRECTING =======================
    def switch_screen(self):
        """
        Redirect to login screen if this is first 
        login, otherwise redirect to portal.
        """
        if self.cashier_name == '':
            self.commands.redirect(self.ui.login)
        else:
            self.commands.redirect(self.ui.portal)

    def exit_login(self):
        """
        Redirect back to landing page if user has not been logged in
        yet or redirect to portal screen if cashier name was updated.
        """
        if self.cashier_name == '':
            self.commands.redirect(self.ui.index)
        else:
            self.commands.redirect(self.ui.portal)

    def log_in(self):
        """
        Log user in with the name entered into field on login screen.
        """
        entry = self.ui.nameEntry.text()
        if entry != '':
            self.cashier_name = entry
            self.ui.userNameButton.setText(entry)
            self.commands.redirect(self.ui.portal)

    # ==================== SEARCHING =======================
    def search(self):
        """
        Get the value of search field and find matching items.
        """
        self.query = self.ui.searchField.text()
        self.result = search_items(
            self.query, self.goods.data, self.category
        ) if self.query != '' else self.goods.data
        self.search_results()

    def search_results(self):
        """Load search results, or display 'no results' message."""
        if self.result == {}:
            self.no_results()
        else:
            self.reload_items(self.result)

    def no_results(self):
        """Display 'item not found' in search results."""
        self.commands.clear_layout(self.layouts[self.category])
        label = self.no_results_label()
        self.layouts[self.category].addWidget(label)

    @staticmethod
    def no_results_label():
        label = QtWidgets.QLabel('Produkt sa nenašiel...')
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(12)
        label.setFont(font)
        label.setStyleSheet('color: #b0180b;')
        return label

    # ==================== SORTING =======================
    def sort(self):
        self.update_sort_state()
        self.load_sorted_items()

    def update_sort_state(self):
        """Update sort button and change sort state."""
        if self.sort_state == 1:
            self.update_sort_button("up_arrow.png", "Highest price")
            self.sort_state = 2
        elif self.sort_state == 2:
            self.update_sort_button("down_arrow.png", "Lowest price")
            self.sort_state = 3
        else:
            self.update_sort_button("up_down_arrow.png", "Sort by price")
            self.sort_state = 1

    def load_sorted_items(self):
        """Sort item codes and load sorted items into catalog."""
        sorted_codes = sort_items(
            self.sort_state, category=self.category
        )
        self.result = {}

        for code in sorted_codes:
            if code in self.goods.data.keys():
                self.result[code] = self.goods.data[code]

        self.reload_items(self.result)

    def update_sort_button(self, icon_name, text):
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(find_icon(icon_name)),
            QtGui.QIcon.Normal, QtGui.QIcon.Off
        )
        self.ui.sortButton.setText(text)
        self.ui.sortButton.setIcon(icon)

    # ===================== LOADING =======================
    def reload_items(self, data):
        """
        Clear items in currently selected category and load new.
        """
        self.commands.clear_layout(self.layouts[self.category])
        self.load_items(data)

    def load_items(self, data):
        """Display item cards in the catalog."""
        data = filter_category(data, self.category)
        for code, vals in data.items():
            self.load_item(code, vals)

    def load_item(self, code, vals):
        """Load item data and display item card in the catalog."""
        price = self.prices.data.get(code)
        amount = self.storage.data.get(code)

        if self.check_available(price, amount):
            ItemCard(
                self, self.layouts[self.category], vals[0],
                code, float(price[1]), vals[1]
            )

    def check_available(self, price, amount):
        """
        Check if item is available (is in the storage and has price).
        """
        try:
            available = int(amount[0]) >= 0
        except:
            return False
        else:
            return price != None and amount != None and available

    # ==================== PORTAL UPDATING =======================
    def update_category(self):
        """
        Set selected category and load items of that category.
        """
        self.category = self.ui.itemCategories.currentIndex()
        self.reload_items(self.goods.data)


class Cart:
    """This class represents a cart with its contents and price."""

    def __init__(self, page):
        self.page = page
        self.ui = page.ui
        self.commands = page.commands

        # Init data
        self.statistics = self.page.data['statistiky']
        self.storage = self.page.storage

        # Init cart global variables
        self.price = 0
        self.contents = {}
        self.id = random_id('P')

        self.buy_click()

    def buy_click(self):
        self.commands.button_click(
            self.ui.buyButton, self.buy
        )

    def buy(self):
        if len(self.contents) > 0:
            self.execute_purchase()
        else:
            self.commands.warning(
                'Prázdny košík',
                'Pred kúpou vložte, prosím, veci do košíka.')

    def execute_purchase(self):
        """
        Generate uctenka_[id].txt, add datapoint to 
        statistics, update sklad.txt amounts
        and remove everything from the cart.
        """
        self.create_receipt()
        self.add_stats()
        self.update_storage()
        self.clear_cart()
        self.purchase_message()

    def clear_cart(self):
        """Remove everything from the cart."""
        for item in list(self.contents.values()):
            item.delete()

    def add_stats(self):
        """Add datapoint from transaction to STATISTIKY.txt."""
        for code, item in self.contents.items():
            self.statistics.data_list.append([
                now(), 'P', self.id[1:], code,
                str(item.amount), str(item.price)])
        self.statistics.save_list()

    def update_storage(self):
        """Change amount of items in sklad.txt."""
        for code, item in self.contents.items():
            self.storage.data[code][0] = int(
                self.storage.data[code][0]) - item.amount
        self.storage.save_data()

    def update_price(self, value):
        """Update total price of a cart."""
        self.price += value
        self.ui.totalPrice.setText(
            "Spolu: "+str_price(self.price, 1)+" €")

    def create_receipt(self):
        """Create uctenka_[id].txt from current cart."""
        filename = 'uctenka_'+self.id+'.txt'
        self.filepath = os.path.join(PATH, 'source', 'data', filename)

        with open(self.filepath, 'w', encoding='utf-8') as receipt:
            receipt.writelines(receipt_template(
                self.id[1:], self.contents,
                self.price, self.page.cashier_name
            ))

    def purchase_message(self):
        self.commands.receipt_msg(self.id[1:], self.filepath)


class ItemCard(QtWidgets.QFrame):

    def __init__(
            self, page, layout, name: str,
            code: str, price: float, image: str):

        super(ItemCard, self).__init__(layout.parent())

        self.page = page
        self.ui = self.page.ui
        self.commands = self.page.commands

        self.parent_layout = layout

        self.name = camelify(name)
        self.display_name = name
        self.code = code
        self.price = price
        self.image = find_image(image)

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
            self.cart_item = CartItem(self)
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
        self.itemPrice = QtWidgets.QLabel(str(self.price) + ' €')
        self.itemPrice.setObjectName(self.name+"ItemPrice")
        self.nameLayout.addWidget(self.itemLabel)
        self.nameLayout.addWidget(self.itemPrice)
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
        self.commands.button_click(self.addButton, self.button_press)
        self.buttonLayout.addWidget(self.addButton)
        self.mainLayout.addWidget(self.itemButton)
        self.parent_layout.addWidget(self)


class CartItem(QtWidgets.QFrame):

    def __init__(self, item):
        self.item = item
        self.page = item.page
        self.ui = self.page.ui
        self.commands = self.page.commands

        self.parent_layout = self.ui.cartLayout
        super(CartItem, self).__init__(self.parent_layout.parent())

        self.code = self.item.code
        self.name = "cart"+self.item.name
        self.display_name = self.item.display_name

        self.price = self.item.price
        self.amount = self.item.amount
        self.total = self.item.price*self.item.amount

        self.update_page_cart()
        self.page.cart.update_price(self.total)

        self.draw_ui()

    def delete(self):
        """Delete this item from cart."""
        self.item.update_status()
        self.price_change(0)
        del self.page.cart.contents[self.code]
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
        self.page.cart.update_price(new_price)

    def update_page_cart(self):
        self.page.cart.contents[self.code] = self

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
        self.commands.button_click(self.cancelButton, self.delete)
        self.mainLayout.addWidget(
            self.cancelSection, 0, QtCore.Qt.AlignRight)
        self.parent_layout.addWidget(self)
