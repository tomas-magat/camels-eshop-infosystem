# UI Commands Simplified
from PyQt5.QtWidgets import QGraphicsScene
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot


class UI_Commands:

    def __init__(self, ui):
        self.ui = ui

    def change_screen(self, screen):
        """
        Switch the current screen on the app window to 
        given screen name (redirect).
        """

        self.ui.screens.setCurrentWidget(screen)

    def button_click(self, button, command):
        """After button clicked execute given command."""

        button.clicked.connect(command)

    def multiple_button_click(self, buttons=[],  command=None):
        """After any of the given buttons clicked execute command."""

        for button in buttons:
            button.clicked.connect(command)

    def delete_button_click(self, button):
        """After button clicked remove its parent."""

        button.clicked.connect(lambda: button.parentWidget().deleteLater())

    def plot_graph(self, graphics_view, figure, size=60):
        """Add matplotlib graph to 'UI canvas' (graphics_view)."""

        figure.set_dpi(size)

        canvas = FigureCanvas(figure)

        scene = QGraphicsScene()
        graphics_view.setScene(scene)
        scene.addWidget(canvas)

    def create_pyqtgraph(self, widget, x, y):
        """
        Create simple graph with x and y data using 
        pyqtgraph PlotWidget and add it to UI graphicsScene.
        """

        self.graphWidget = pg.PlotWidget()
        self.graphWidget.plot(x, y)

        scene = QGraphicsScene()
        widget.setScene(scene)
        scene.addWidget(self.graphWidget)
