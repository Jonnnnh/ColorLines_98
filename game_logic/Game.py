from data_structures.Graph import Graph
from models.Color import Color

class Game:

    def __init__(self, size, count_color: int, count_balls_line: int):
        self._size = size
        self._count_balls_line = count_balls_line
        self._color = list(Color)[:count_color]
        self._graph = Graph(size ** 2)
        self._area = {(i, j): None for i in range(size) for j in range(size)}
        self._choosing_sell = None
        self._initialize_graph_adjacency_lists()
        self._points = 0

    def _initialize_graph_adjacency_lists(self):
        for key in self._area.keys():
            self._graph.adj_lists[key] = []

    @property
    def graph(self):
        return self._graph

    @property
    def area(self):
        return self._area

    @property
    def choosing_cell(self):
        return self._choosing_sell

    @choosing_cell.setter
    def choosing_cell(self, choosing_cell):
        self._choosing_sell = choosing_cell

    @property
    def size(self):
        return self._size

    @property
    def color(self):
        return self._color

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        self._points = points

    @property
    def count_balls_line(self):
        return self._count_balls_line

    def get_empty_cell(self):
        return [key for key, value in self._area.items() if value is None]