from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QPushButton

from game_logic.GameLogic import GameService


class HighscoreWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('highscoreDialog.ui', self)
        self.load_data()
        self.closeButton = self.findChild(QPushButton, 'closeButton')
        self.closeButton.clicked.connect(self.close)

    def load_data(self):
        highscores = GameService.load_highscores()
        highscores.sort(key=lambda x: x[1], reverse=True)
        tableWidget = self.findChild(QTableWidget, 'highscoreTableWidget')
        tableWidget.setRowCount(len(highscores))
        for row, (name, score) in enumerate(highscores):
            tableWidget.setItem(row, 0, QTableWidgetItem(name))
            tableWidget.setItem(row, 1, QTableWidgetItem(str(score)))
