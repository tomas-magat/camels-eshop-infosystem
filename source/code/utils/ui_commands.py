# UI Commands Simplified
import time
import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QObject
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from .tools import find_icon


class UI_Commands():

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

    def date_entries(self, date_edits: list, dates_list):
        """
        After user changes datetime in one of QDateEdit widgets,
        return a list of dates in specified range.
        """

        def command(): return self.dates_range(date_edits, dates_list)
        self.init_date_entries(date_edits)
        self.set_date_edits(date_edits)

        for edit in date_edits:
            edit.dateChanged.connect(command)

    def set_date_edits(self, date_edits):
        """After date changed in a field, validate the other field."""

        date_edits[0].dateChanged.connect(
            lambda: self._set_date(date_edits))
        date_edits[1].dateChanged.connect(
            lambda: self._set_date(date_edits))

    def init_date_entries(self, date_edits: list):
        """
        Initialize valid dates in given date edits on first run.
        """

        self.date_limits(
            date_edits[0], datetime.date(2022, 12, 12), datetime.date.today(), max_sub=1
        )
        self.date_limits(
            date_edits[1], datetime.date(2022, 12, 12), datetime.date.today(), min_add=1
        )
        date_edits[1].setDate(datetime.date.today())

    def date_limits(
        self, date_edit: QDateEdit, date_min: datetime.date,
        date_max: datetime.date, min_add: int = 0, max_sub: int = 0
    ):
        """Sets minimum and maximum date of given date_edit."""

        min_date = date_min + \
            datetime.timedelta(days=min_add)
        date_edit.setMinimumDate(min_date)
        max_date = date_max - datetime.timedelta(days=max_sub)
        date_edit.setMaximumDate(max_date)

    def _set_date(self, date_edits):
        self.date_limits(
            date_edits[0],
            datetime.date(2022, 12, 12),
            date_edits[1].date().toPyDate(),
            max_sub=1
        )
        self.date_limits(
            date_edits[1],
            date_edits[0].date().toPyDate(),
            datetime.date.today(),
            min_add=1
        )

    def dates_range(self, date_edits, date_list):
        """Return list of dates in specific range."""

        date_from = date_edits[0].dateTime().toPyDateTime()
        date_to = date_edits[1].dateTime().toPyDateTime()

        result = [datetime.datetime.strptime(datepoint, "%Y-%m-%d %H-%M-%S")
                  for datepoint in list(set(date_list))]

        for i, datepoint in enumerate(result):
            if date_from > datepoint or datepoint > date_to:
                result.pop(i)

        result = [datepoint.strftime("%Y-%m-%d %H-%M-%S")
                  for datepoint in sorted(result)]

        # print(date_from, date_to, result)

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


class Timer(QObject):
    """
    Represents a Timer that updates data variables periodically,
    but without freezing the main app thread (used with QThread).
    """

    def __init__(self, data, period=3.0):
        super(Timer, self).__init__()
        self.period = period
        self.data = list(data.values())
        self.versions = [file.version for file in self.data]

    def run(self):
        while True:
            self.update_vars()
            time.sleep(self.period)

    def update_vars(self):
        for i in range(len(self.data)):
            self.update_var(i)

    def update_var(self, i):
        self.data[i].get_version()
        current_version = self.data[i].version

        if current_version != self.versions[i]:
            self.data[i].read()
            self.versions[i] = current_version
            self.data[i].changed.emit(self.data[i].data)
