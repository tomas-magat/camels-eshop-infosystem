import shutil
import re

from PyQt5 import QtWidgets, QtCore, QtGui

from utils.tools import *


class Databaza:
    """
    This class handles everything done on the databaza
    screen (button clicks, item listing...).
    """

    def __init__(self, app):
        self.ui = app.ui
        self.commands = app.commands
        self.data = app.data

        # Init lists of categories
        self.lists = [
            self.ui.listWidget,
            self.ui.listWidget_shirts,
            self.ui.listWidget_pants,
            self.ui.listWidget_boots,
            self.ui.listWidget_hoodies,
            self.ui.listWidget_accesories,
        ]

        # Init global variables
        self.tabs = self.ui.tabWidget_databaza
        self.no_res = False
        self.adding = False

        self.init_actions()
        self.init_data()

    def init_actions(self):
        self.redirect_action()
        self.search_action()
        self.item_actions()
        self.lists_actions()

    def init_data(self):
        self.goods = self.data['tovar']
        self.prices = self.data['cennik']
        self.storage = self.data['sklad']
        self.statistika = self.data['statistiky']
        self.goods.version_changed(self.reload_items)
        self.tabs.setCurrentIndex(0)
        self.update_category()

    # ==================== ACTIONS =======================
    def redirect_action(self):
        self.commands.button_click(
            self.ui.databazaButton, self.switch_screen
        )

    def lists_actions(self):
        for listw in self.lists:
            self.commands.list_item_selected(listw, self.change_item)

        self.commands.tab_selected(
            self.tabs, self.update_category
        )

    def item_actions(self):
        self.commands.button_click(
            self.ui.deleteItem, self.delete_item
        )
        self.commands.button_click(
            self.ui.addItem, self.add_item
        )

    def search_action(self):
        self.commands.form_submit(
            [self.ui.searchButton_database, self.ui.searchField_database],
            self.search
        )

    # ===================== LOADING =======================
    def reload_items(self, data):
        self.lists[self.category].clear()
        self.load_items(data)

    def load_items(self, data):
        for code, vals in filter_category(
                data, self.category).items():
            self.load_item(code, vals)

    def load_item(self, code, vals):
        self.lists[self.category].addItem('#' + code + ' ' + vals[0])

    def switch_screen(self):
        """Redirect to this databaza screen."""
        self.commands.redirect(self.ui.databaza)

    def add_item(self):
        """Display empty item details to enter new."""
        self.adding = True
        self.clear_no_results()
        prefilled_code = '' if self.category == 0 else find_code(self.category)
        ItemDetails(self, self.ui.right_database, '',
                    prefilled_code, adding=True)

    def change_item(self):
        """
        Display item details on the right side of the
        databaza screen and allow user to modify them.
        """
        if self.adding:
            self.adding = False
        try:
            text = self.lists[self.category].currentItem().text().split()
            code = text[0].lstrip("#")
            name = ' '.join(text[1:]) if len(text) > 1 else code
            image = self.goods.data[code][1]

            ItemDetails(self, self.ui.right_database, name, code, image)
        except:
            pass

    def delete_item(self):
        if self.clear_no_results() and not self.adding:
            text = self.lists[self.category].currentItem().text().split()
            item_name = ' '.join(text[1:])
            self.commands.confirm(
                self.ui, f"Chcete natrvalo vymazať produkt {item_name}?",
                ok_command=self.delete_item_txt)

    def delete_item_txt(self):
        text = self.lists[self.category].currentItem().text().split()
        code = text[0].lstrip("#")

        self.lists[self.category].takeItem(
            self.lists[self.category].currentRow())
        del self.goods.data[code]
        self.goods.save_data()
        if self.storage.data.get(code) != None:
            del self.storage.data[code]
            self.storage.save_data()
        if self.prices.data.get(code) != None:
            del self.prices.data[code]
            self.prices.save_data()

    def update_category(self):
        self.category = self.tabs.currentIndex()
        self.reload_items(self.goods.data)
        self.lists[self.category].setCurrentRow(0)

    def search(self):
        """
        Get the value of search field and find matching items.
        """
        self.query = self.ui.searchField_database.text()
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
        self.lists[self.category].clear()
        prvok = 'Produkt sa nenasiel'
        self.lists[self.category].addItem(prvok)
        self.no_res = True

    def clear_no_results(self):
        if self.no_res:
            self.reload_items(self.goods.data)
            self.no_res = False
            return False
        return True


class ItemDetails(QtWidgets.QFrame):

    def __init__(
            self, page, parent, display_name: str,
            code: str, image_path="", adding=False):

        super(ItemDetails, self).__init__(parent)

        self.page = page
        self.ui = self.page.ui
        self.commands = self.page.commands

        self.name = "itemDetails"
        self.display_name = display_name
        self.filename = image_path
        self.image_path = find_image(self.filename)
        self.code = code

        self.patterns = {
            'code': re.compile("^[0-5]\d{3}$"),
            'name': re.compile('^[^!.?"#]+$'),
        }

        self.adding = adding
        self.button_text = "Pridať produkt" if self.adding else "Uložiť zmeny"

        self.draw_ui()

    def submit(self):
        """Update listWidget with currently entered values."""
        new_name = self.lineEdit.text()
        new_code = self.lineEdit_2.text()

        if self.validate_fields(new_code, new_name) \
                and self.unique_code(new_code):
            if self.adding:
                self.create(new_code, new_name)
            else:
                self.update(new_code, new_name)

    def create(self, code, name):
        self.page.goods.data[code] = [name, self.filename]
        self.page.goods.save_data()
        self.adding = False
        self.page.adding = False
        self.page.lists[self.page.category].setCurrentRow(
            self.page.lists[self.page.category].count()-1
        )

    def update(self, code, name):
        if code != self.code:
            self.update_code(self.page.prices, code)
            self.update_code(self.page.storage, code)
            self.update_code(self.page.goods, code)
            self.update_stats_code(code)

        elif name != self.name or self.filename != '':
            self.page.goods.data[code] = [name, self.filename]
            self.page.goods.save_data()

        self.display_name, self.code = name, code

    def update_code(self, data, code):
        datapoint = data.data.get(self.code)
        if datapoint != None:
            data.data[code] = datapoint
            del data.data[self.code]
            data.save_data()

    def update_stats_code(self, code):
        stats_list = self.page.statistika.data_list
        for datapoint in stats_list:
            if datapoint[3] == self.code:
                datapoint[3] = code
        self.page.statistika.save_list()

    def validate_fields(self, code, name):
        code_valid = self.patterns['code'].match(code)
        name_valid = self.patterns['name'].match(name)
        image_valid = self.filename != ''

        if code_valid and name_valid and image_valid:
            return True
        elif code_valid == None:
            self.commands.warning("Zadajte správny kód produktu")
        elif name_valid == None:
            self.commands.warning("Zadajte vhodný názov produktu")
        elif not image_valid:
            self.commands.warning("Vyberte obrázok produktu")
        return False

    def unique_code(self, code):
        other_codes = list(self.page.goods.data.keys())
        if not self.adding:
            other_codes.remove(self.code)

        if code not in other_codes:
            return True
        else:
            self.commands.error("Zadaný kód už existuje, vyberte iný")
            return False

    def pick_image(self):
        """Let user select image and save it."""

        file = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", "",
            "Images (*);; WEBP (*.webp);; JPG (*.jpg;*.jpeg;*.jpe;*jfif);; PNG (*.png)"
        )

        self.image_path = file[0]
        if self.image_path != '':
            if valid_image(self.image_path):
                self.filename = self.image_path.split("/", maxsplit=256)[-1]
                self.save_image()
                self.update_image()

    def save_image(self):
        """Copy selected image to the assets/images/ directory."""

        source = self.image_path
        dist = find_image(self.filename)

        try:
            shutil.copy(source, dist)
        except:
            pass

        self.image_path = dist

    def update_image(self):
        """Update currently displayed image."""

        self.image.setMinimumSize(QtCore.QSize(247, 247))
        self.image.setStyleSheet(
            "background-color: transparent;")
        self.image.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(self.image_path),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.image.setIcon(icon3)
        self.image.setIconSize(QtCore.QSize(247, 247))

    def draw_ui(self):
        self.setObjectName(self.name)
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setObjectName(self.name+"Layout")
        self.itemNameSection = QtWidgets.QWidget(self)
        self.itemNameSection.setMaximumSize(QtCore.QSize(16777215, 80))
        self.itemNameSection.setObjectName(self.name+"NameSection")
        self.nameLayout = QtWidgets.QVBoxLayout(self.itemNameSection)
        self.nameLayout.setObjectName(self.name+"NameLayout")
        self.entryStyle = """QLineEdit { 
                background-color: white;
                border-style: outset;
                border-width: 2px;
                border-radius: 12px;
                border-color: #cad2c5;
                padding-left: 4px;
            }
            QLineEdit:hover { 
                background-color: rgb(218, 218, 218);
                border-color: beige;
            }"""
        self.lineEdit = QtWidgets.QLineEdit(
            self.display_name, self.itemNameSection)
        self.lineEdit.setMinimumHeight(24)
        self.lineEdit.setStyleSheet(self.entryStyle)
        self.lineEdit.setPlaceholderText("Zadajte názov produktu")
        self.lineEdit.setObjectName(self.name+"NameEdit")
        self.nameLayout.addWidget(self.lineEdit)
        self.mainLayout.addWidget(self.itemNameSection)
        self.itemCodeSection = QtWidgets.QWidget(self)
        self.itemCodeSection.setMaximumSize(QtCore.QSize(16777215, 50))
        self.itemCodeSection.setObjectName(self.name+"CodeSection")
        self.codeLayout = QtWidgets.QVBoxLayout(self.itemCodeSection)
        self.codeLayout.setObjectName(self.name+"CodeLayout")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.code, self.itemCodeSection)
        self.lineEdit_2.setStyleSheet(self.entryStyle)
        self.lineEdit_2.setMinimumHeight(24)
        self.lineEdit_2.setObjectName(self.name+"CodeEdit")
        self.lineEdit_2.setPlaceholderText("Zadajte kód produktu")
        self.codeLayout.addWidget(self.lineEdit_2)
        self.mainLayout.addWidget(self.itemCodeSection)
        self.itemImageSection = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.itemImageSection.sizePolicy().hasHeightForWidth())
        self.itemImageSection.setSizePolicy(sizePolicy)
        self.itemImageSection.setObjectName(self.name+"ImageSection")
        self.imageLayout = QtWidgets.QVBoxLayout(self.itemImageSection)
        self.imageLayout.setObjectName("imageLayout")
        self.image = QtWidgets.QPushButton(self.itemImageSection)
        self.image.setStyleSheet("border:none;")
        self.image.setMinimumHeight(24)
        if not self.adding and self.image_path != '':
            self.update_image()
        else:
            self.image.setStyleSheet("background-color: #cad2c5;"
                                     "color: #2F3E46;"
                                     "border-radius: 12px;"
                                     "border: 5px solid #cad2c5;")
            font = QtGui.QFont()
            font.setBold(True)
            self.image.setFont(font)
            self.image.setText("Vyberte obrázok")
        self.commands.button_click(self.image, self.pick_image)
        self.image.setObjectName(self.name+"image")
        self.imageLayout.addWidget(self.image)
        self.mainLayout.addWidget(self.itemImageSection)
        self.saveButtonSection = QtWidgets.QWidget(self)
        self.saveButtonSection.setObjectName(self.name+"ButtonSection")
        self.buttonLayout = QtWidgets.QVBoxLayout(self.saveButtonSection)
        self.buttonLayout.setObjectName(self.name+"ButtonLayout")
        self.pushButton = QtWidgets.QPushButton(self.button_text)
        self.pushButton.setMinimumHeight(24)
        self.pushButton.setStyleSheet("background-color: #cad2c5;"
                                      "color: #2F3E46;"
                                      "border-radius: 12px;"
                                      "border: 5px solid #cad2c5;")
        self.pushButton.setObjectName(self.name+"SaveButton")
        font = QtGui.QFont()
        font.setBold(True)
        self.pushButton.setFont(font)
        self.commands.button_click(self.pushButton, self.submit)
        self.buttonLayout.addWidget(self.pushButton)
        self.mainLayout.addWidget(self.saveButtonSection)
        self.commands.clear_layout(self.ui.verticalLayout_12)
        self.ui.verticalLayout_12.addWidget(self)
