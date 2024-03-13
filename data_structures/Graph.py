import collections
from typing import Tuple, Dict, List

class Graph:

    def __init__(self, vertices: int):
        self._vertices = vertices
        self._adj_lists = collections.defaultdict(list)

    @property
    def vertices(self) -> int:
        return self._vertices

    @vertices.setter
    def vertices(self, vertices: int):
        self._vertices = vertices

    @property
    def adj_lists(self) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
        return self._adj_lists

    def add_edge(self, u: Tuple[int, int], v: Tuple[int, int]):
        self._adj_lists[u].append(v)
        self._adj_lists[v].append(u)

    def remove_edge(self, u: Tuple[int, int], v: Tuple[int, int]):
        if v in self._adj_lists[u]:
            self._adj_lists[u].remove(v)
        if u in self._adj_lists[v]:
            self._adj_lists[v].remove(u)
