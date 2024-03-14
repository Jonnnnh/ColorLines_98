from abc import ABC, abstractmethod
from PyQt5.QtGui import QPainter
from models.Ball import Ball

class DrawStrategy(ABC):
    @abstractmethod
    def draw(self, painter: QPainter, ball: Ball, x: int, y: int, size: int):
        pass