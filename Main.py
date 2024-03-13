from PyQt5.QtWidgets import QApplication
from gui.GameWindow import GameWindow
from gui.SettingsWindow import SettingsWindow

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w1 = SettingsWindow()
    w1.show()
    w = GameWindow(w1)
    w.show()
    sys.exit(app.exec_())
