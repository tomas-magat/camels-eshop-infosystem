from PyQt5 import QtWidgets, QtCore, QtGui

from utils.ui_commands import UI_Commands
from utils import tools


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

        self.commands.change_screen(self.ui.databaza)

    def add_item(self):
        """Display empty item details to enter new."""

        ItemDetails(self.ui, self, self.ui.right_database,
                    '', '', '', add_button=True)

    def change_item(self, index):
        """Display item details and option to modify them."""

        text = self.ui.listWidget.currentItem().text().split()
        code = text[0].lstrip("#")
        name = text[-1]
        image_path = "../../../assets/images/image.png"
        ItemDetails(self.ui, self, self.ui.right_database,
                    name, code, image_path)


class ItemDetails(QtWidgets.QFrame):

    def __init__(self, ui, page, parent, display_name: str, code: str, image_path: str, add_button=False):
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
