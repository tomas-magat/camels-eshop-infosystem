# UI Simplified
class UI_Commands:
    def __init__(self, ui):
        self.ui = ui

    def change_screen(self, screen):
        """
        Changes current screen on the main window by using 
        UI.stackedWidget.setCurrentWidget() function to given 
        screen name (Defaults to index).
        """

        self.ui.stackedWidget.setCurrentWidget(screen)

    def button_click(self, button, command):
        """After button clicked execute given command."""

        button.clicked.connect(command)

    def multiple_button_click(self, buttons=[],  command=None):
        """After any of the given buttons clicked execute command."""

        for button in buttons:
            button.clicked.connect(command)
