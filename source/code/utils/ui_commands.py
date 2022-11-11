# UI Commands Simplified

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
