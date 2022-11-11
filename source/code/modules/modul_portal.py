# Modul Portal -
# Lists catalog of available products, has an option
# to search by code/name and to filter products.
# After ordering the selected items in given amounts,
# creates file uctenka_[id_transakcie].txt.

from PyQt5.QtWidgets import QGraphicsScene
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

from utils.file import DataFile
from utils.ui_commands import UI_Commands
from utils import tools


class Portal:

    def __init__(self, ui):
        """
        This class handles evrything done on the portal
        screen (button clicks, file loading...).
        """

        self.ui = ui
        self.commands = UI_Commands(self.ui)

        # Track button clicks
        self.commands.button_click(
            self.ui.portalButton, self.switch_screen)

        self.test_plot()

        # Read file 'tovar.txt' - not in prototype
        # self.tovar = DataFile('tovar')
        # self.goods = self.tovar.read()
        # self.version = self.tovar.get_version()

        # Update 'goods' variable every 3 seconds
        # tools.run_periodically(self.update_goods, 3)

    def update_goods(self):
        """
        Update 'goods' variable if version of the tovar.txt
        datafile has changed.
        """

        current_version = self.tovar.get_version()

        if current_version != self.version:
            self.goods = self.tovar.read()
            self.version = current_version

    def switch_screen(self):
        """Redirect to this portal screen."""

        self.commands.change_screen(self.ui.portal)

    def test_plot(self):
        """Just for testing purposes."""

        figure = Figure(figsize=(2, 2))
        axes = figure.gca()
        axes.set_title("Testing")
        x = np.linspace(1, 10)
        y = np.linspace(1, 10)
        y1 = np.linspace(11, 20)
        axes.plot(x, y, "-k", label="first one")
        axes.plot(x, y1, "-b", label="second one")
        axes.grid(True)

        canvas = FigureCanvas(figure)
        scene = QGraphicsScene()
        self.ui.testGraph.setScene(scene)
        scene.addWidget(canvas)
