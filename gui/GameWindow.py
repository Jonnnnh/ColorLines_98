from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QInputDialog, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor
from PyQt5.QtCore import Qt

from gui.HighscoreWindow import HighscoreWindow
from gui.RulesWindow import RulesWindow
from gui.strategy.BigBallDrawStrategy import BigBallDrawStrategy
from gui.strategy.SmallBallDrawStrategy import SmallBallDrawStrategy
from models.Ball import Ball
from game_logic.Game import Game
from game_logic.GameService import GameService
from models.Size import Size
from gui.SettingsWindow import SettingsWindow


class GameWindow(QMainWindow):
    CANVAS_SIZE = 720
    CANVAS_WIDTH = 745
    CANVAS_HEIGHT = 980
    FIXED_SIZE = 200
    CELL_BORDER_WIDTH = 3
    SELECTED_CELL_COLOR = QColor(153, 154, 153)
    LINE_COLOR = QColor(0, 0, 0)
    BACKGROUND_COLOR = QColor(255, 255, 255)

    def __init__(self, w: SettingsWindow):
        super().__init__()
        self.w = w
        self.game = None
        self.points = QLabel(self)
        self.label = QLabel(self)
        self.rules_shown = False
        self.init_ui()

    def init_ui(self):
        uic.loadUi('Untitled.ui', self)
        self.setWindowTitle("ColorLines98")

        self.pushButton.setFixedSize(self.FIXED_SIZE, 100)
        self.pushButton.clicked.connect(self.start_game)

        canvas = QPixmap(self.CANVAS_SIZE, self.CANVAS_SIZE)
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)

        layout = QGridLayout(self.centralwidget)

        layout.addWidget(self.pushButton, 0, 0, 1, 2, alignment=Qt.AlignCenter)
        layout.addWidget(self.points, 1, 0, alignment=Qt.AlignLeft)
        layout.addWidget(self.label, 2, 0, 1, 2)

        self.setFixedSize(self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        self.center_window()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_game(self):
        print("Starting game with settings:", self.w.count_cells, self.w.count_colors, self.w.count_balls_line, self.w.difficulty)
        if not self.rules_shown:
            rules_window = RulesWindow()
            rules_window.exec_()
            self.rules_shown = True
        self.initialize_game()
        self.update_ui_for_new_game()

    def initialize_game(self):
        print("Initializing game...")
        self.game = Game(self.w.count_cells, self.w.count_colors, self.w.count_balls_line, self.w)
        print("Game object created successfully:", self.game) if self.game else print("Failed to create game object")
        GameService.start_game(self.game)

    def update_ui_for_new_game(self):
        self.draw_game()
        self.pushButton.setText("Restart")
        self.points.setText(str(self.game.points))

    def draw_cells(self):
        print("Drawing cells...")

        canvas_size = self.CANVAS_SIZE
        game_size = self.game.size
        size = int(canvas_size / game_size)

        painter = QPainter(self.label.pixmap())
        painter.setPen(QPen(self.LINE_COLOR, self.CELL_BORDER_WIDTH))
        painter.setBrush(self.BACKGROUND_COLOR)
        painter.drawRect(0, 0, canvas_size, canvas_size)

        if self.game.choosing_cell is not None:
            painter.setBrush(QColor(153, 154, 153))
            painter.drawRect(self.game.choosing_cell[1] * size, self.game.choosing_cell[0] * size, size, size)
            painter.setBrush(QColor(255, 255, 255))

        for i in range(1, self.game.size):
            painter.drawLine(i * size, 0, i * size, canvas_size)
            painter.drawLine(0, i * size, canvas_size, i * size)

        painter.end()
        self.update()

    def draw_game(self):
        print("Drawing game...")
        self.draw_cells()
        self.draw_balls()

    def draw_balls(self):
        print("Drawing balls...")
        canvas_size = self.CANVAS_SIZE
        game_size = self.game.size
        cell_size = int(canvas_size / game_size)
        painter = QPainter(self.label.pixmap())

        big_strategy = BigBallDrawStrategy()
        small_strategy = SmallBallDrawStrategy()

        for key, ball in self.game.area.items():
            if isinstance(ball, Ball):
                painter.setBrush(QColor(*ball.color.value))
                x, y = key[1] * cell_size, key[0] * cell_size

                strategy = big_strategy if ball.size == Size.big else small_strategy
                strategy.draw(painter, ball, x, y, cell_size)

        painter.end()
        self.update()

    def mousePressEvent(self, event):
        if self.game:
            print("Mouse pressed...")

            click_x = event.x() - self.label.x()
            click_y = event.y() - self.label.y()

            cell_size = self.CANVAS_SIZE / self.game.size

            if 0 <= click_x <= self.CANVAS_SIZE and 0 <= click_y <= self.CANVAS_SIZE:

                cell_x = int(click_x // cell_size)
                cell_y = int(click_y // cell_size)
                print("\033[94mSelected cell:\033[0m", (cell_y, cell_x))

                GameService.move(self.game, (cell_y, cell_x))
                self.draw_game()
                self.update_game_status()
            else:
                print("\033[91mClick outside of game area\033[0m")

    def update_game_status(self):
        self.points.setText(str(self.game.points))
        if GameService.is_game_over(self.game):
            print("\033[92mGame over!\033[0m")
            self.points.setText("You lose: " + str(self.game.points))
            self.show_game_over_dialog()

    def show_game_over_dialog(self):
        name, ok = QInputDialog.getText(self, "Highscore", "Enter your name:")
        if ok and name:
            GameService.save_highscore(name, self.game.points)
            highscore_window = HighscoreWindow(self)
            highscore_window.exec_()
            QMessageBox.information(self, "Game Over", "Thank you for playing! Your score has been saved")

    def closeEvent(self, event):
        self.w.close()
        event.accept()
