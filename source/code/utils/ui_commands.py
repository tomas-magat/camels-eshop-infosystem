# UI Commands Simplified
import time
import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QObject
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.pyplot import close

from .tools import find_icon


class UI_Commands():

    def __init__(self, ui):
        self.ui = ui
        self.graphs = []

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

    def clear_layout(self, layout):
        """Clear all items from existing layout object."""

        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

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

    def text_changed(self, line_edit: QLineEdit, command):
        """
        After the text value in line_edit changes execute the command.
        """

        line_edit.textChanged.connect(command)

    def track_graph(self, figure):
        """If graph exists track its figure to be closed later."""

        self.graphs.append(figure)

    def close_all_graphs(self):
        """Close all existing graphs to save memory."""

        for figure in self.graphs:
            try:
                close(figure)
            except:
                pass

    def close_najviac_najmenej_graphs(self):
        """Close najviac and najmenej graphs to save memory"""

        try:
            close(self.graphs[0])
            close(self.graphs[1])
        except:
            pass

    def close_graph_vyvoj_ceny(self):
        '''close graph vyvoj_ceny to save memory'''

        for figure in self.graphs[2:]:
            try:
                close(figure)
            except:
                pass

    def plot_graph(self, graphics_view: QGraphicsView, figure, size=58.5):
        """Add matplotlib graph to 'UI canvas' (graphics_view)."""

        figure.set_dpi(size)

        canvas = FigureCanvas(figure)
        scene = QGraphicsScene()

        graphics_view.setScene(scene)
        scene.addWidget(canvas)

    def product_sorted_graph(self, main_list, x_date, price_graph, date_info):
        """
        Create 2 lists from statistiky.txt 
        needed to plot the graph vyvoj_ceny
        """
        deka = main_list[0][0]
        deta = deka.split()[0]
        x_date_unedited = [deka.split()[0].split('-')]
        price_graph_unedited = [0]
        for i in main_list:
            split_date = i[0].split()
            if x_date_unedited[-1] != split_date[0].split('-'):
                x_date_unedited += split_date[0].split('-'),
                date_info += [i],
            else:
                date_info[-1] += [i]
            if split_date[0] == deta:
                if i[1] == 'N':
                    price_graph_unedited[-1] -= int(i[4])*float(i[5])
                else:
                    price_graph_unedited[-1] += int(i[4])*float(i[5])
            else:
                deta = split_date[0]
                if i[1] == 'N':
                    price_graph_unedited += price_graph_unedited[-1] -\
                        int(i[4])*float(i[5]),
                else:
                    price_graph_unedited += price_graph_unedited[-1] +\
                        int(i[4])*float(i[5]),
        for i in price_graph_unedited:
            price_graph += round(i, 2),
        for i in x_date_unedited:
            x_date += i[2]+'.'+i[1]+'.'+i[0][2:],
        b = 0
        for i in range(len(x_date_unedited)-1):
            d1 = datetime.date(
                int(x_date_unedited[i][0]), int(x_date_unedited[i][1]), int(x_date_unedited[i][2]))
            d2 = datetime.date(
                int(x_date_unedited[i+1][0]), int(x_date_unedited[i+1][1]), int(x_date_unedited[i+1][2]))
            x = x_date_unedited[i]
            y = x_date_unedited[i+1]
            price_connection = round(price_graph_unedited[i], 2)
            if x[0] == y[0] and x[1] == y[1]:
                date_connection = '.'+x[1]+'.'+x[0][2:]
                for date_number in range(int(x[2])+1, int(y[2])):
                    b += 1
                    if len(str(date_number)) == 1:
                        date_number_changed = '0'+str(date_number)
                    else:
                        date_number_changed = str(date_number)
                    x_date.insert(i+b, date_number_changed+date_connection)
                    price_graph.insert(i+b, price_connection)
                    date_info.insert(i+b, [['žiadne objednávky\nv tento deň']])
            else:
                days_number = (d2-d1).days-1
                days_number_before = days_number-(int(y[2])-1)
                if days_number_before != 0:
                    date_connection = '.'+x[1]+'.'+x[0][2:]
                    for date_number in range(int(x[2]), int(x[2])+days_number_before):
                        b += 1
                        if len(str(date_number+1)) == 1:
                            date_number_changed = '0'+str(date_number+1)
                        else:
                            date_number_changed = str(date_number+1)
                        x_date.insert(i+b, date_number_changed+date_connection)
                        price_graph.insert(i+b, price_connection)
                        date_info.insert(
                            i+b, [['žiadne objednávky\nv tento deň']])
                date_connection = '.'+y[1]+'.'+y[0][2:]
                for date_number in range(1, int(y[2])):
                    b += 1
                    if len(str(date_number)) == 1:
                        date_number_changed = '0'+str(date_number)
                    else:
                        date_number_changed = str(date_number)
                    x_date.insert(i+b, date_number_changed+date_connection)
                    price_graph.insert(i+b, price_connection)
                    date_info.insert(i+b, [['žiadne objednávky\nv tento deň']])

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

    def date_changed(self, edit, command):
        """
        Execute a command after user changes 
        datetime in QDateEdit widget.
        """

        edit.dateChanged.connect(command)

    def get_date(self, edit):
        """Get python datetime from QDateEdit."""

        return edit.dateTime.toPyDateTime()

    # def init_date_edits(self, date_edits: list):
    #     """
    #     Initialize valid dates in given date edits on first run.
    #     """

    #     self.date_limits(
    #         date_edits[0], datetime.date(2022, 12, 12), datetime.date.today(), max_sub=1
    #     )
    #     self.date_limits(
    #         date_edits[1], datetime.date(2022, 12, 12), datetime.date.today(), min_add=1
    #     )
    #     date_edits[1].setDate(datetime.date.today())

    # def date_limits(
    #     self, date_edit: QDateEdit,
    #     date_min=datetime.date(2022, 12, 12),
    #     date_max=datetime.date.today(),
    #     min_add: int = 0, max_sub: int = 0
    # ):
    #     """Sets minimum and maximum date of given date_edit."""

    #     min_date = date_min + datetime.timedelta(days=min_add)
    #     date_edit.setMinimumDate(min_date)

    #     max_date = date_max - datetime.timedelta(days=max_sub)
    #     date_edit.setMaximumDate(max_date)

    # def set_limits(self, date_edits: list):
    #     self.date_limits(
    #         date_edits[0],
    #         date_max=date_edits[1].date().toPyDate(),
    #         max_sub=1
    #     )
    #     self.date_limits(
    #         date_edits[1],
    #         date_min=date_edits[0].date().toPyDate(),
    #         min_add=1
    #     )

    @staticmethod
    def receipt_msg(id: str, filepath, type: str = 'účtenku'):
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

    @staticmethod
    def error(message: str, additional_text=''):
        """Display simple error message."""

        Message(message, QMessageBox.Critical, 'Error', additional_text)

    @staticmethod
    def info(message: str, additional_text=''):
        """Display simple info message."""

        Message(message, QMessageBox.Information,
                'Information', additional_text)

    @staticmethod
    def warning(message: str, additional_text=''):
        """Display simple warrning message."""

        Message(message, QMessageBox.Warning, 'Warning', additional_text)

    @staticmethod
    def confirm(page, message: str, ok_command):
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

    def __init__(self, data, period=5.0):
        super(Timer, self).__init__()
        self.period = period
        self.data = list(data.values())
        self.versions = [file.version for file in self.data]

    def run(self):
        while True:
            self.update_vars()
            time.sleep(self.period)

    def update_vars(self):
        for i, file in enumerate(self.data[:3]):
            self.update_var(file, i)
        self.update_stats()

    def update_var(self, file, i):
        file.get_version()
        current_version = file.version

        if current_version != self.versions[i]:
            file.read_data()
            self.versions[i] = current_version
            file.changed.emit(file.data)

    def update_stats(self):
        self.data[-1].get_version()
        current_version = self.data[-1].version

        if current_version != self.versions[-1]:
            self.data[-1].read_data()
            self.versions[-1] = current_version
            self.data[-1].changed_list.emit(self.data[-1].data_list)
