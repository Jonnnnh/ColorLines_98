from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

from game_logic.GameService import GameService


class HighscoreWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Highscores")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.load_data()
        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.close)
        self.layout.addWidget(self.closeButton)

    def load_data(self):
        highscores = GameService.load_highscores("highscores.txt")
        print(highscores)
        highscores.sort(key=lambda x: x[1], reverse=True)
        for name, score in highscores:
            self.layout.addWidget(QLabel(f"{name}: {score}"))