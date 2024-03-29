# Modul Sklad -
# Show amount of products.
# Alerts you to products with low quantity.
# Can generate (automatic/half-automatic/manual) order,
# creating objednavka_[id_transakcie].txt

# TODO
# tajna message pre picklemaster09

from PyQt5 import QtWidgets, QtCore, QtGui

from utils.tools import *


class Sklad:

    def __init__(self, app):
        """
        This class handles everything done on the sklad
        screen (button clicks, item listing...).
        """

        self.ui = app.ui
        self.commands = app.commands
        self.data = app.data

        # Init global variables
        self.cart = Cart(self)
        self.total_price = 0
        self.sort_state = 1
        self.order_mode = 3
        self.highlight_threshold = int(self.ui.Alert.text())
        # ['Automatic = 'auto' / semiautomatic ='semi', kod tovaru, HowManyToBuy, CountWhenToBuy]
        self.orderRules = []

        # Set Vsetko page
        self.ui.itemCategories_2.setCurrentIndex(0)

        # Init category layouts
        self.layouts = [
            self.ui.verticalLayout_18,
            self.ui.verticalLayout_37,
            self.ui.verticalLayout_20,
            self.ui.verticalLayout_28,
            self.ui.verticalLayout_31,
            self.ui.verticalLayout_35
        ]

        self.init_actions()
        self.init_data()

    def init_actions(self):
        self.manual()
        self.order_modes()
        self.redirect_action()
        self.search_action()
        self.sort_action()
        self.catalog_action()
        self.alert_action()

    def init_data(self):
        self.goods = self.data['tovar']
        self.prices = self.data['cennik']
        self.storage = self.data['sklad']
        self.statistics = self.data['statistiky']
        self.versions_check()
        self.update_category()

    # ==================== ACTIONS =======================
    def redirect_action(self):
        self.commands.button_click(
            self.ui.skladButton,
            self.switch_screen
        )

    def search_action(self):
        self.commands.form_submit(
            [self.ui.searchButton_4, self.ui.searchField_3],
            self.search
        )

    def sort_action(self):
        self.commands.button_click(
            self.ui.sortButton_2, self.sort
        )

    def catalog_action(self):
        self.commands.tab_selected(
            self.ui.itemCategories_2, self.update_category
        )

    def alert_action(self):
        self.commands.form_submit(
            [self.ui.alert_button, self.ui.Alert],
            self.alert
        )

    # ==================== REDIRECTS =======================
    def switch_screen(self):
        """Redirect to this sklad screen."""

        self.commands.redirect(self.ui.sklad)

    # ==================== SEARCH =======================
    def search(self):
        """
        Get the value of search field and find matching items.
        """
        self.query = self.ui.searchField_3.text()
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
        self.commands.freeze_button(self.ui.sortButton_2)

    def update_sort_state(self):
        """Update sort button and change sort state."""
        if self.sort_state == 1:
            self.update_sort_button("up_arrow.png", "Highest price")
            self.sort_state = 2
            self.load_sorted_items()
        elif self.sort_state == 2:
            self.update_sort_button("down_arrow.png", "Lowest price")
            self.sort_state = 3
            self.load_sorted_items()
        else:
            self.update_sort_button("up_down_arrow.png", "Sort by price")
            self.sort_state = 1
            self.load_counts_items()

    def load_sorted_items(self):
        """Sort item codes and load sorted items into catalog."""
        sorted_codes = sort_items(
            self.sort_state, price_type='buy', category=self.category
        )
        self.result = {}

        for code in sorted_codes:
            if code in self.goods.data.keys():
                self.result[code] = self.goods.data[code]

        self.reload_items(self.result)

    def load_counts_items(self):
        """Sort item codes and load sorted items into catalog."""
        sorted_codes = sort_counts(
            category=self.category
        )
        self.result = {}

        for code, val in self.goods.data.items():
            if code not in sorted_codes:
                self.result[code] = val
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
        self.ui.sortButton_2.setText(text)
        self.ui.sortButton_2.setIcon(icon)

    # ===================== LOADING =======================
    def reload_items(self, data):
        """
        Clear catalog of current selected category and load new items.
        """
        self.commands.clear_layout(self.layouts[self.category])
        self.load_items(data)

    def load_items(self, data):
        """Display item cards in the catalog."""
        data = filter_category(data, self.category)
        for code, vals in data.items():
            self.load_item(code, vals)

    def load_item(self, code, vals):
        price = self.prices.data.get(code)
        count = self.storage.data.get(code)
        count = [0] if count == None else count

        if price != None:
            ItemCard(
                self, self.layouts[self.category], vals[0],
                code, float(price[0]), vals[1], int(
                    count[0]), self.highlight_threshold
            )

    # ==================== SKLAD UPDATING =======================
    def update_category(self):
        """
        Set selected category and load items of that category.
        """
        self.category = self.ui.itemCategories_2.currentIndex()
        self.load_counts_items()

    def versions_check(self):
        """Check for Datafile versions and update on change."""
        self.storage.version_changed(self.load_counts_items)

        self.goods.version_changed(self.load_counts_items)

        self.storage.version_changed(
            lambda: self.update_database(self.goods.data))

        self.prices.version_changed(self.load_counts_items)

    # =================== UPDATE ORDER STATE ====================
    def automatic(self):
        self.order_mode = 1
        self.ui.input_widget.setVisible(True)
        self.ui.buyButton_7.setText('Nastaviť')

    def semiautomatic(self):
        self.order_mode = 2
        self.ui.input_widget.setVisible(True)
        self.ui.buyButton_7.setText('Nastaviť')

    def manual(self):
        self.order_mode = 3
        self.ui.input_widget.setVisible(False)
        self.ui.buyButton_7.setText('Kúpiť')

    def order_modes(self):
        """Set order mode based on currently selected radio button."""

        self.commands.button_click(
            self.ui.automatic, self.automatic)

        self.commands.button_click(
            self.ui.semiautomatic, self.semiautomatic)

        self.commands.button_click(
            self.ui.manual, self.manual)

    # =================== UPDATE SKLAD DB ===================
    def update_database(self, data):
        """Update sklad database according to order_rules whenever its version is changed"""
        for code, item in data.items():

            if code in (element1 for sublist in self.orderRules for element1 in sublist):
                current_count = self.storage.data.get(code)
                current_count = 0 if current_count == None else current_count[0]

                for index_of_item, lst in enumerate(self.orderRules):
                    for element2 in lst:
                        if element2 == code:
                            index = index_of_item

                if int(current_count) <= int(self.orderRules[index][3]):
                    if self.orderRules[index][0] == 'auto':
                        self.refill_sklad(code, item, index)

                    if self.orderRules[index][0] == 'semi':
                        self.commands.confirm(
                            self.ui, f"Chcete doskladniť produkt {item[0]}?",
                            ok_command=lambda: self.refill_sklad(code, item, index))

    def refill_sklad(self, code, item, index):
        self.storage.data[code] = [int(self.orderRules[index][2])]
        self.storage.save_data()
        self.commands.info(f'Tovar {item[0]} #{code} bol naskladnený.')
        self.cart.purchase_message()
        self.add_stats_for_automated(code, item, index)

    def add_stats_for_automated(self, code, item, index):
        """Add datapoint from transaction to STATISTIKY.txt."""
        self.statistics.data_list.append([
            now(), 'N', self.cart.id[1:], code,
            str(int(self.orderRules[index][2])), str(self.prices.data.get(code)[0])])
        self.statistics.save_list()

    # =========================== ALERT =========================
    def alert(self):
        new_highlight = int(self.ui.Alert.text())
        if new_highlight != self.highlight_threshold:
            self.highlight_threshold = new_highlight
            self.reload_items(self.result)


class Cart:
    """This class represents a cart with its contents and price."""

    def __init__(self, page):
        self.page = page
        self.ui = page.ui
        self.commands = page.commands

        # Init data
        self.statistics = self.page.data['statistiky']
        self.storage = self.page.data['sklad']

        # Init cart global variables
        self.price = 0
        self.contents = {}
        self.id = random_id('N')

        self.buy_click()

    def buy_click(self):
        self.commands.button_click(
            self.ui.buyButton_7, self.buy
        )

    def buy(self):
        if len(self.contents) > 0:
            try:
                if int(self.page.ui.HowManyToBuy.text()) > 0:
                    self.execute_purchase()
                    self.page.update_database(self.page.goods.data)
                else:
                    self.commands.warning(
                        'Prosím skontrolujte údaje objednávky',
                        'Pole \'Doplniť do počtu\' musí byť kladné nenulové číslo')
            except:
                self.commands.warning(
                    'Prosím skontrolujte údaje objednávky',
                    'Pole \'Doplniť do počtu\' musí byť kladné nenulové číslo')
        else:
            self.commands.warning(
                'Prázdny košík',
                'Pred objednávkou vložte, prosím, veci do košíka.')

    def execute_purchase(self):
        """
        Generate objednavka_[id].txt, add datapoint to 
        statistics, update sklad.txt amounts
        and remove everything from the cart.
        """
        self.create_receipt()
        HowManyToBuy = self.page.ui.HowManyToBuy.text()
        CountWhenToBuy = self.page.ui.CountWhenToBuy.text()

        # MANUAL
        if self.page.order_mode == 3:
            self.add_stats()
            self.update_storage()
            self.clear_cart()
            self.purchase_message()

        # SEMIAUTOMATIC
        if self.page.order_mode == 2:
            if int(HowManyToBuy) > int(CountWhenToBuy):
                self.create_rule('semi', HowManyToBuy, CountWhenToBuy)
                self.clear_cart()
                self.commands.info(
                    'Poloautomatická objednávka bola zaregistrovaná')
            else:
                self.commands.warning(
                    'Údaj \'Doplniť do počtu\' musí byť väčší než údaj \'Doplniť pri počte\'')

        # AUTOMATIC
        if self.page.order_mode == 1:
            if int(HowManyToBuy) > int(CountWhenToBuy):
                self.create_rule('auto', HowManyToBuy, CountWhenToBuy)
                self.clear_cart()
                self.commands.info(
                    'Automatická objednávka bola zaregistrovaná')
            else:
                self.commands.warning(
                    'Údaj \'Doplniť do počtu\' musí byť väčší než údaj \'Doplniť pri počte\'')

        print(self.page.orderRules)

    def create_rule(self, rule_type: str, HowManyToBuy, CountWhenToBuy):
        """
        Add order rule instruction to orderRules 
        for every item in itemCart.
        Note that if rule for specific code already exists,
        rewrite the old rule and aply the new one.
        """
        for code in self.contents.items():
            if len(self.page.orderRules) == 0:
                self.page.orderRules.append(
                    [rule_type, code[0], HowManyToBuy, CountWhenToBuy])
            if code[0] in (item for sublist in self.page.orderRules for item in sublist):
                for i, lst in enumerate(self.page.orderRules):
                    for element in lst:
                        if element == code[0]:
                            self.page.orderRules[i] = [
                                rule_type, code[0], HowManyToBuy, CountWhenToBuy]
            else:
                self.page.orderRules.append(
                    [rule_type, code[0], HowManyToBuy, CountWhenToBuy])

    def clear_cart(self):
        """Remove everything from the cart."""
        for item in list(self.contents.values()):
            item.delete()

    def add_stats(self):
        """Add datapoint from transaction to STATISTIKY.txt."""
        for code, item in self.contents.items():
            self.statistics.data_list.append([
                now(), 'N', self.id[1:], code,
                str(item.amount), str(item.price)])
        self.statistics.save_list()

    def update_storage(self):
        """Change amount of items in sklad.txt."""
        for code, item in self.contents.items():
            current_count = self.storage.data.get(code)
            current_count = 0 if current_count == None else current_count[0]
            self.storage.data[code] = [int(current_count) + item.amount]
        self.storage.save_data()

    def update_price(self, value):
        """Update total price of a cart."""
        self.price += value
        self.ui.totalPrice_2.setText(
            "Spolu: "+str_price(self.price, 1)+" €")

    def create_receipt(self):
        """Create uctenka_[id].txt from current cart."""
        filename = 'objednavka_'+self.id+'.txt'
        self.filepath = os.path.join(PATH, 'source', 'data', filename)

        with open(self.filepath, 'w', encoding='utf-8') as receipt:
            self.order_receipt_template(receipt)

    def purchase_message(self):
        receipt_icon = QtGui.QIcon()
        msg = QtWidgets.QMessageBox()
        receipt_icon.addPixmap(QtGui.QPixmap(find_icon('receipt.svg')),
                               QtGui.QIcon.Normal, QtGui.QIcon.Off)
        msg.setWindowTitle(f"Sale {self.id[1:]} - confirmed")
        msg.setText('<b><p style="padding: 0px;  margin: 0px;">'
                    'Pokladničný doklad bol úspešne vygenerovaný.</p>' +
                    f'<br><a href="file:{self.filepath}">'
                    f'Otvor objednávku č. {self.id}</a>')
        msg.setIconPixmap(QtGui.QPixmap(find_icon('receipt.svg')))
        msg.exec_()

    def order_receipt_template(self, receipt):
        receipt.write('Camels E-shop s.r.o.')
        receipt.write('\nCislo objednavky: '+self.id)
        receipt.write('\nVytvorene dna: '+now())
        receipt.write('\n\n=================================\n')
        items = [
            item.display_name+'\n\t'+str(item.amount)+'ks x ' +
            str_price(item.price)+'\t\t' +
            str_price(item.price, item.amount)+' €\n'
            for item in list(self.contents.values())
        ]
        receipt.writelines(items)
        receipt.write('\n=================================')
        receipt.write('\nSpolu cena: '+str_price(self.price)+' €')
        receipt.write('\nDPH(20%): '+str_price(self.price*0.2)+' €')


class ItemCard(QtWidgets.QFrame):

    def __init__(
            self, page, layout, name: str,
            code: str, price: float, image: str, count: float, highlight_threshold: int):

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
        self.count = count
        self.highlight_threshold = highlight_threshold

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
            self.spinBox.setValue(1)
            self.itemButton.setMaximumWidth(110)
            self.addButton.setText("Add to cart")

    def draw_ui(self):
        self.setMinimumSize(QtCore.QSize(200, 60))
        self.setMaximumSize(QtCore.QSize(16777215, 60))
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setObjectName("Frame")
        if self.count <= self.highlight_threshold:
            self.setStyleSheet("#Frame{border: 2px solid red}")
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
        self.itemLabel = QtWidgets.QLabel(self.display_name+"  #"+self.code+"\nCena:"+str(
            self.price)+" €"+"    Na sklade: " + str(self.count))
        self.itemLabel.setObjectName(self.name+"ItemLabel")
        self.nameLayout.addWidget(self.itemLabel)
        self.mainLayout_2.addWidget(self.itemName)
        self.itemCount = QtWidgets.QWidget(self)
        self.itemCount.setMaximumSize(QtCore.QSize(60, 16777215))
        self.itemCount.setObjectName(self.name+"Count")
        self.countLayout = QtWidgets.QVBoxLayout(self.itemCount)
        self.countLayout.setObjectName(self.name+"CountLayout")
        self.spinBox = QtWidgets.QSpinBox(self.itemCount)
        self.spinBox.setValue(1)
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

    def __init__(self, item):
        self.item = item
        self.page = item.page
        self.ui = self.page.ui
        self.commands = self.page.commands

        self.parent_layout = self.ui.verticalLayout_34
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
