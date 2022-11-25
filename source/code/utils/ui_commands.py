# UI Commands Simplified
from PyQt5.QtWidgets import (
    QGraphicsScene, QWidget, QGraphicsView, QMessageBox, QLineEdit)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


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
    
    def plot_graph_trzby(self, graphics_view: QGraphicsView, figure, size=68.5):
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

    def clear_layout(self, layout):
        """Clear all items from existing layout object."""

        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    @staticmethod
    def error_message(message: str, additional_text=''):
        """Display simple error message."""

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setInformativeText(additional_text)
        msg.setWindowTitle("Error")
        msg.exec_()

    @staticmethod
    def info_message(message: str, additional_text=''):
        """Display simple error message."""

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setInformativeText(additional_text)
        msg.setWindowTitle("Information")
        msg.exec_()

    @staticmethod
    def warning_message(message: str, additional_text=''):
        """Display simple error message."""

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(message)
        msg.setInformativeText(additional_text)
        msg.setWindowTitle("Warning")
        msg.exec_()
