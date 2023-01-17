# UI Commands Simplified
import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.pyplot import close

from .tools import find_icon


class UI_Commands():

    def __init__(self, ui):
        self.ui = ui
        self.graphs = []

    # ===================== GENERAL =====================
    def redirect(self, screen: QWidget):
        """
        Switch the current screen on the app window to 
        given screen name (redirect).
        """

        self.ui.screens.setCurrentWidget(screen)

    # ===================== BUTTONS =====================
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

    def freeze_button(self, button, duration=200):
        """Allow user only click button once per duration."""

        button.setEnabled(False)
        QTimer.singleShot(
            duration, lambda: button.setDisabled(False)
        )

    # ===================== LAYOUTS =====================
    def clear_layout(self, layout):
        """Clear all items from existing layout object."""

        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    # ===================== LINE EDITS =====================
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

    # ===================== GRAPHS =====================
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
        """Close najviac and najmenej graphs to save memory."""

        try:
            close(self.graphs[0])
            close(self.graphs[1])
        except:
            pass

    def close_graph_vyvoj_ceny(self):
        """close graph vyvoj_ceny to save memory."""

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
                int(x_date_unedited[i][0]),
                int(x_date_unedited[i][1]),
                int(x_date_unedited[i][2]))
            d2 = datetime.date(
                int(x_date_unedited[i+1][0]),
                int(x_date_unedited[i+1][1]),
                int(x_date_unedited[i+1][2]))
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
                    date_info.insert(i+b, [['Žiadne objednávky\nv tento deň']])
            else:
                days_number = (d2-d1).days-1
                days_number_before = days_number-(int(y[2])-1)
                if days_number_before != 0:
                    date_connection = '.'+x[1]+'.'+x[0][2:]
                    for date_number in range(
                            int(x[2]), int(x[2])+days_number_before):
                        b += 1
                        if len(str(date_number+1)) == 1:
                            date_number_changed = '0'+str(date_number+1)
                        else:
                            date_number_changed = str(date_number+1)
                        x_date.insert(i+b, date_number_changed+date_connection)
                        price_graph.insert(i+b, price_connection)
                        date_info.insert(
                            i+b, [['Žiadne objednávky\nv tento deň']])
                date_connection = '.'+y[1]+'.'+y[0][2:]
                for date_number in range(1, int(y[2])):
                    b += 1
                    if len(str(date_number)) == 1:
                        date_number_changed = '0'+str(date_number)
                    else:
                        date_number_changed = str(date_number)
                    x_date.insert(i+b, date_number_changed+date_connection)
                    price_graph.insert(i+b, price_connection)
                    date_info.insert(i+b, [['Žiadne objednávky\nv tento deň']])

    # ===================== LIST AND TAB =====================
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

    # ===================== DATES =====================
    def date_changed(self, edit, command):
        """
        Execute a command after user changes 
        datetime in QDateEdit widget.
        """

        edit.dateChanged.connect(command)

    def to_date_list(self, date_string):
        """
        Convert string of date in format: YYYY-MM-DD HH-mm-ss 
        to list in format: ['YYYY', 'MM', 'DD'].
        """

        return date_string.split()[0].split('-')

    def get_date(self, edit):
        """Get python datetime from QDateEdit."""

        return edit.dateTime.toPyDateTime()

    # ===================== POP-UPS =====================
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

        question = QMessageBox(
            QMessageBox.Question,
            "Confirm", message,
            buttons=QMessageBox.Yes | QMessageBox.No,
            parent=page,
        )
        question.setDefaultButton(QMessageBox.No)
        question.setStyleSheet(
            'background-color: rgb(248, 248, 248); font-weight: bold'
        )
        question.exec_()

        reply = question.standardButton(question.clickedButton())
        if reply == QMessageBox.Yes:
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

    def __init__(self, data, period=5000):
        super(Timer, self).__init__()
        self.period = period
        self.data = list(data.values())
        self.versions = [file.version for file in self.data]

    def run(self):
        self.timer = QTimer()
        self.timer.setInterval(self.period)
        self.timer.timeout.connect(self.process)
        self.timer.start()

    def finished(self):
        self.timer.stop()

    def process(self):
        for i, file in enumerate(self.data[:3]):
            self.update_var(file, i)
        self.update_stats()

    def update_var(self, file, i):
        file.get_version()
        current_version = file.version

        if current_version != self.versions[i]:
            self.versions[i] = current_version
            file.read_data()
            file.changed.emit(file.data)

    def update_stats(self):
        self.data[-1].get_version()
        current_version = self.data[-1].version

        if current_version != self.versions[-1]:
            self.versions[-1] = current_version
            self.data[-1].read_data()
            self.data[-1].changed_list.emit(self.data[-1].data_list)
