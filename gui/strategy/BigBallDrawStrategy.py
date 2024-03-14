from PyQt5.QtGui import QPainter

from gui.strategy.DrawStrategy import DrawStrategy
from models import Ball


class BigBallDrawStrategy(DrawStrategy):
    def draw(self, painter: QPainter, ball: Ball, x: int, y: int, size: int):
        painter.drawEllipse(x, y, size, size)