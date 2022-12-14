import os
import shutil

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
from utils.ui_commands import UI_Commands
from utils.tools import find_image, find_code, search_items
from utils.file import DataFile
import re


class Databaza:

    def __init__(self, ui):
        """
        This class handles everything done on the databaza
        screen (button clicks, item listing...).
        """

        self.ui = ui
        self.commands = UI_Commands(self.ui)

        self.lists = [
            self.ui.listWidget,
            self.ui.listWidget_shirts,
            self.ui.listWidget_pants,
            self.ui.listWidget_boots,
            self.ui.listWidget_hoodies,
            self.ui.listWidget_accesories,
        ]
        self.tab = self.ui.tabWidget_databaza
        self.category = 0

        self.commands.button_click(
            self.ui.databazaButton, self.switch_screen)

        self.commands.button_click(
            self.ui.deleteItem, self.delete_item)

        self.commands.button_click(
            self.ui.addItem, self.add_item)

        for listw in self.lists:
            self.commands.list_item_selected(
                listw, self.change_item)

        self.commands.tab_selected(
            self.tab, self.update_category
        )

        self.commands.form_submit(
            [self.ui.searchButton_database, self.ui.searchField_database],
            self.search
        )

        self.goods = DataFile('tovar')
        self.prices = DataFile('cennik')
        self.storage = DataFile('sklad')
        self.tab.setCurrentIndex(0)
        self.update_category()

    def reload_items(self, data):
        self.lists[self.category].clear()
        self.load_items(data)
        self.lists[self.category].setCurrentRow(0)

    def load_items(self, data):
        for code, vals in data.items():
            self.load_item(code, vals)

    def load_item(self, code, vals):
        codes = '12345' if self.category == 0 else str(self.category)

        if code[0] in codes:
            self.lists[self.category].addItem('#' + code + ' ' + vals[0])

    def switch_screen(self):
        """Redirect to this databaza screen."""

        self.commands.redirect(self.ui.databaza)

    def add_item(self):
        """Display empty item details to enter new."""

        prefilled_code = '' if self.category == 0 else find_code(self.category)
        ItemDetails(self, self.ui.right_database, '',
                    prefilled_code, add_button=True)

    def change_item(self):
        """
        Display item details on the right side of the
        databaza screen and allow user to modify them.
        """
        try:
            text = self.lists[self.category].currentItem().text().split()
            code = text[0].lstrip("#")
            name = ' '.join(text[1:]) if len(text) > 1 else code
            image = self.goods.data[code][1]

            ItemDetails(self, self.ui.right_database, name, code, image)
        except:
            pass

    def delete_item(self):
        self.commands.confirm(
            self.ui, "Chcete natrvalo vymazať produkt?",
            ok_command=self.delete_item_txt)

    def delete_item_txt(self):
        text = self.lists[self.category].currentItem().text().split()
        code = text[0].lstrip("#")
        self.lists[self.category].takeItem(
            self.lists[self.category].currentRow())
        del self.goods.data[code]
        self.goods.save_data()

    def update_category(self):
        self.category = self.tab.currentIndex()
        self.goods.read()
        self.reload_items(self.goods.data)

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


class ItemDetails(QtWidgets.QFrame):

    def __init__(self, page, parent, display_name: str, code: str,
                 image_path="", add_button=False):

        super(ItemDetails, self).__init__(parent)

        self.page = page
        self.ui = self.page.ui
        self.commands = self.page.commands

        self.name = "itemDetails"
        self.display_name = display_name
        self.image_path = find_image(image_path)
        self.filename = image_path
        self.code = code

        self.adding = add_button
        self.button_text = "Pridať produkt" if self.adding else "Uložiť zmeny"

        self.draw_ui()

    def edit_items(self, new_code, new_name, new_text):
        self.page.lists[self.page.category].currentItem().setText(new_text)
        if new_code != self.code:
            self.page.lists[self.page.category].currentItem().setText(
                new_text)
            prices_data = self.page.prices.data.get(self.code)
            if prices_data != None:
                self.page.prices.data[new_code] = prices_data
                del self.page.prices.data[self.code]
                self.page.prices.save_data()

            storage_code = self.page.storage.data.get(self.code)
            if storage_code != None:
                self.page.storage.data[new_code] = storage_code
                del self.page.storage.data[self.code]
                self.page.storage.save_data()

            goods_code = self.page.goods.data.get(self.code)
            self.page.goods.data[new_code] = goods_code
            del self.page.goods.data[self.code]
            self.page.goods.save_data()
            self.page.goods.read()
        else:
            self.page.goods.data[new_code] = [
                new_name, self.filename]
            self.page.goods.save_data()
            self.page.goods.read()

        self.code = new_code
        self.name = new_name

    def update_list(self):
        """Update listWidget with currently entered values."""

        new_name = self.lineEdit.text()
        new_code = self.lineEdit_2.text()

        pattern = re.compile("^[0-5]+$")
        pattern2 = re.compile("^[A-Za-z ]+$")
        other_codes = list(self.page.goods.data.keys())
        if not self.adding:
            other_codes.remove(self.code)
        unique = new_code not in other_codes

        if pattern.match(new_code) and pattern2.match(new_name) and unique:
            new_text = "#"+new_code+" "+new_name

            if self.adding:
                self.page.goods.data[new_code] = [new_name, self.filename]
                self.page.goods.save_data()
                self.page.goods.read()
                self.page.lists[self.page.category].addItem(new_text)
                self.adding = False
            else:
                old_text = self.page.lists[self.page.category].currentItem(
                ).text()
                if new_text != old_text:
                    self.edit_items(new_code, new_name, new_text)
        else:
            print('zla hodnota')
            msg = QMessageBox()
            msg.setWindowTitle("Error")
            msg.setText("Zadajte spravnu hodnotu")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def pick_image(self):
        """Let user select image and save it."""

        file = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", "",
            "Images (*);; WEBP (*.webp);; JPG (*.jpg;*.jpeg;*.jpe;*jfif);; PNG (*.png)"
        )

        if file:
            self.image_path = file[0]
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
        self.lineEdit = QtWidgets.QLineEdit(
            self.display_name, self.itemNameSection)
        self.lineEdit.setMinimumHeight(20)
        self.lineEdit.setStyleSheet(
            "background-color: rgb(255, 255, 255); border-radius: 10px; padding-left:5px;")
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
        self.lineEdit_2.setStyleSheet(
            "background-color: rgb(255, 255, 255); border-radius: 10px; padding-left:5px;")
        self.lineEdit_2.setMinimumHeight(20)
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
        if not self.adding and self.image_path != '':
            self.update_image()
        else:
            self.image.setStyleSheet("background-color: #cad2c5;"
                                     "color: #2F3E46;"
                                     "border-radius: 11px;"
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
        self.pushButton.setStyleSheet("background-color: #cad2c5;"
                                      "color: #2F3E46;"
                                      "border-radius: 11px;"
                                      "border: 5px solid #cad2c5;")
        self.pushButton.setObjectName(self.name+"SaveButton")
        font = QtGui.QFont()
        font.setBold(True)
        self.pushButton.setFont(font)
        self.commands.button_click(self.pushButton, self.update_list)
        self.buttonLayout.addWidget(self.pushButton)
        self.mainLayout.addWidget(self.saveButtonSection)
        self.commands.clear_layout(self.ui.verticalLayout_12)
        self.ui.verticalLayout_12.addWidget(self)
