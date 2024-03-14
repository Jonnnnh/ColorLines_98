from PyQt5.QtGui import QPainter

from gui.strategy.DrawStrategy import DrawStrategy
from models import Ball


class SmallBallDrawStrategy(DrawStrategy):
    def draw(self, painter: QPainter, ball: Ball, x: int, y: int, size: int):
        half_size = size // 2
        painter.drawEllipse(x + size // 4, y + size // 4, half_size, half_size)