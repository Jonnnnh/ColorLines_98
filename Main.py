from PyQt5.QtWidgets import QApplication
from gui.GameWindow import GameWindow
from gui.SettingsWindow import SettingsWindow


def main():
    try:
        app = QApplication(sys.argv)
        settings_window = SettingsWindow()
        settings_window.show()

        game_window = GameWindow(settings_window)
        game_window.show()

        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == '__main__':
    import sys

    main()
