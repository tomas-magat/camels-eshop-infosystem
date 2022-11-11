# UI Commands Simplified
from PyQt5.QtWidgets import QGraphicsScene
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


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

    def plot_graph(self, graphics_view, *args, size=(3, 3), title='', grid=True):
        """Show matplotlib graph on 'canvas' (graphics_view)."""

        figure = self.create_graph(size, title, grid, args)

        canvas = FigureCanvas(figure)
        scene = QGraphicsScene()
        graphics_view.setScene(scene)
        scene.addWidget(canvas)

    @staticmethod
    def create_graph(size, title, grid, *args):
        """
        Create matplotlib figure with specified parameters:

        Arguments:
        data (list of lists) = list of [x, y, color] values

        Default arguments:
        size (tuple) = (x, y) size of the graph
        title (str) = title on the top of the graph
        grid (bool) = shows grid in the graph background
        """

        figure = Figure(figsize=size)
        axes = figure.gca()
        axes.set_title(title)

        for i in range(len(args[0])//3):
            axes.plot(args[0][i*3], args[0][i*3+1], args[0][i*3+2])

        axes.grid(grid)

        return figure
