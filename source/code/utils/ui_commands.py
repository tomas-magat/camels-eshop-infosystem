# UI Commands Simplified
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from .tools import find_icon


class UI_Commands:

    def __init__(self, ui):
        self.ui = ui

    def redirect(self, screen: QWidget):
        """
        Switch the current screen on the app window to 
        given screen name (redirect).
        """

        self.ui.screens.setCurrentWidget(screen)

    def button_click(self, button, command):
        """After button clicked execute given command."""

        button.clicked.connect(command)

    def buttons_click(self, buttons: list,  command):
        """After any of the given buttons clicked execute command."""

        for button in buttons:
            button.clicked.connect(command)

    def delete_button_click(self, button):
        """After button clicked remove its parent."""

        button.clicked.connect(
            lambda: button.parentWidget().deleteLater())

    def form_submit(self, widgets: list, command):
        """
        After pressing enter key in any of the line edits
        or pressing the submit button of the form execute command.
        """

        for widget in widgets:
            if type(widget) == QLineEdit:
                widget.returnPressed.connect(command)
            else:
                self.button_click(widget, command)

    def plot_graph(self, graphics_view: QGraphicsView, figure, size=58.5):
        """Add matplotlib graph to 'UI canvas' (graphics_view)."""

        figure.set_dpi(size)

        canvas = FigureCanvas(figure)

        scene = QGraphicsScene()
        graphics_view.setScene(scene)
        scene.addWidget(canvas)

    def list_item_selected(self, list_widget, command):
        """
        Works with QListWidget. After clicking on
        item in QListWidget execute given command.
        Command must be a function that takes 1 argument: 
        int (index of the item that was selected)
        """

        list_widget.currentRowChanged.connect(command)

    def tab_selected(self, tab_widget, command):
        """Do command if tab in a tabwidget selected."""

        tab_widget.currentChanged.connect(command)

    def clear_layout(self, layout):
        """Clear all items from existing layout object."""

        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def date_changed(self, date_edit: QDateEdit, command):
        """
        After user changes datetime in QDateEdit widget,
        run a command with 1 parameter: datetime.
        """

        value = date_edit.dateTime().toPyDateTime()
        date_edit.dateTimeChanged.connect(lambda: command(value))

    def receipt_msg(self, id: str, filepath, type: str = 'účtenku'):
        """Display message about created receipt."""

        receipt_icon = QIcon()
        msg = QMessageBox()
        receipt_icon.addPixmap(QPixmap(find_icon('receipt.svg')),
                               QIcon.Normal, QIcon.Off)
        msg.setWindowTitle(f"Sale {id} - confirmed")
        msg.setText('<b><p style="padding: 0px;  margin: 0px;">'
                    'Pokladničný doklad bol úspešne vygenerovaný.</p>' +
                    f'<br><a href="file:{filepath}">'
                    f'Otvor {type} č. {id}</a>')
        msg.setIconPixmap(QPixmap(find_icon('receipt.svg')))
        msg.exec_()

    def error(self, message: str, additional_text=''):
        """Display simple error message."""

        Message(message, QMessageBox.Critical, 'Error', additional_text)

    def info(self, message: str, additional_text=''):
        """Display simple info message."""

        Message(message, QMessageBox.Information,
                'Information', additional_text)

    def warning(self, message: str, additional_text=''):
        """Display simple warrning message."""

        Message(message, QMessageBox.Warning, 'Warning', additional_text)

    def confirm(self, page, message: str, ok_command):
        """Display message to confirm the action."""

        answer = QMessageBox.question(
            page, 'Confirm', message, QMessageBox.Yes | QMessageBox.No)

        if answer == QMessageBox.Yes:
            ok_command()


class Message(QMessageBox):

    def __init__(self, message: str, icon, window_title: str,
                 additional_text=''):

        super(Message, self).__init__()

        self.setIcon(icon)
        self.setText(message)
        self.setInformativeText(additional_text)
        self.setWindowTitle(window_title)
        self.exec_()
