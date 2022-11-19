import os
import shutil

from PyQt5 import QtWidgets, QtCore, QtGui

from utils.ui_commands import UI_Commands
from utils.ENV_VARS import PATH


class Databaza:

    def __init__(self, ui):
        """
        This class handles everything done on the databaza
        screen (button clicks, item listing...).
        """

        self.ui = ui
        self.commands = UI_Commands(self.ui)

        self.commands.button_click(
            self.ui.databazaButton, self.switch_screen)

        self.commands.button_click(
            self.ui.addItem, self.add_item)

        self.commands.list_item_selected(
            self.ui.listWidget, self.change_item)

    def switch_screen(self):
        """Redirect to this databaza screen."""

        self.commands.redirect(self.ui.databaza)

    def add_item(self):
        """Display empty item details to enter new."""

        ItemDetails(self.ui, self, self.ui.right_database,
                    '', '', add_button=True)

    def change_item(self):
        """
        Display item details on the right side of the
        databaza screen allow user to modify them.
        """

        text = self.ui.listWidget.currentItem().text().split()
        print(text)
        code = text[0].lstrip("#")
        name = ''.join(text[1:]) if len(text) > 1 else code
        ItemDetails(self.ui, self, self.ui.right_database,
                    name, code)



class ItemDetails(QtWidgets.QFrame):

    def __init__(self, ui, page, parent, display_name: str, code: str, image_path="", add_button=False):
        super(ItemDetails, self).__init__(parent)

        self.ui = ui
        self.page = page
        self.commands = UI_Commands(self.ui)
        self.name = "itemDetails"
        self.display_name = display_name
        self.image_path = image_path
        self.code = code
        self.adding = add_button
        self.button_text = "Pridať produkt" if add_button else "Uložiť zmeny"

        self.draw_ui()

    def update_list(self):
        self.text = self.lineEdit.text()
        self.new_code = self.lineEdit_2.text()

        if self.text != "" and self.new_code != "":
            self.new_text = "#"+self.new_code+" "+self.text
            if self.new_text != self.ui.listWidget.currentItem().text():
                if self.adding:
                    self.ui.listWidget.addItem(self.new_text)
                else:
                    self.ui.listWidget.currentItem().setText(self.new_text)

    def pick_image(self):
        file = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open File", "", "Images (*);; WEBP (*.webp);; JPG (*.jpg;*.jpeg;*.jpe;*jfif);; PNG (*.png)")

        if file:
            self.image_path = file[0]
            self.filename = self.image_path.split("/", maxsplit=256)[-1]
            self.save_image()
            self.update_image()

    def save_image(self):
        source_path = self.image_path
        new_path = os.path.join(PATH, 'assets', 'images')
        try:
            shutil.copy(source_path, new_path)
        except:
            pass
        self.image_path = os.path.join(new_path, self.filename)

    def update_image(self):
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
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
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
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
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
            self.image.setStyleSheet(
                "background-color: rgb(58, 95, 214); color: rgb(235, 235, 235)")
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
        self.pushButton.setStyleSheet("background-color: rgb(58, 95, 214);\n"
                                      "color: rgb(235, 235, 235)")
        self.pushButton.setObjectName(self.name+"SaveButton")
        self.commands.button_click(self.pushButton, self.update_list)
        self.buttonLayout.addWidget(self.pushButton)
        self.mainLayout.addWidget(self.saveButtonSection)
        self.commands.clear_layout(self.ui.verticalLayout_12)
        self.ui.verticalLayout_12.addWidget(self)
