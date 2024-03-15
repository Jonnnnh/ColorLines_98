import collections

from game_logic import Game
from models.Ball import Ball
from models.Size import Size

import random

class GameService:

    @staticmethod
    def start_game(game: Game):
        GameService.populate_balls(game, 5, Size.big)
        GameService.populate_balls(game, 3, Size.small)
        GameService.rework_graph(game)

    @staticmethod
    def populate_balls(game: Game, count: int, size: Size):
        for _ in range(count):
            if len(game.get_empty_cell()) == 0:
                break
            key = random.choice(game.get_empty_cell())
            game.area[key] = Ball(size, random.choice(game.color))

    @staticmethod
    def choose_cell(game: Game, cell: tuple):
        if cell not in game.area:
            print("\033[91mError: The selected cell is outside the playing field\033[0m")
            return
        if GameService.is_big_ball(game, cell[0], cell[1]):
            game.choosing_cell = cell

    @staticmethod
    def end_move(game: Game):
        GameService.transform_small_balls(game)
        if len(game.get_empty_cell()) > 0:
            GameService.populate_balls(game, 3, Size.small)
        else:
            print("\033[92mGame Over: No space left for new balls\033[0m")
            return
        game.choosing_cell = None
        GameService.rework_graph(game)

    @staticmethod
    def transform_small_balls(game: Game):
        for key, ball in game.area.items():
            if ball and ball.size == Size.small:
                ball.size = Size.big
                GameService.delete_balls(game, key)

    @staticmethod
    def is_big_ball(game: Game, row: int, col: int):
        return game.area.get((row, col)) is not None and game.area.get((row, col)).size == Size.big

    @staticmethod
    def is_small_ball(game: Game, row: int, col: int):
        return game.area.get((row, col)) is not None and game.area.get((row, col)).size == Size.small

    @staticmethod
    def move(game: Game, cell: tuple):
        if game.choosing_cell:
            GameService.move_ball(game, game.choosing_cell, cell)
        else:
            GameService.choose_cell(game, cell)

    @staticmethod
    def move_ball(game: Game, cell_start: tuple, cell_end: tuple):
        if game.area.get(cell_start) is None:
            print("\033[91mError: There is no ball to move in the start cell\033[0m")
            return
        if GameService.can_move_ball(game, cell_start, cell_end):
            game.area[cell_end], game.area[cell_start] = game.area[cell_start], None
            GameService.handle_post_move(game, cell_end)
        elif GameService.is_big_ball(game, cell_end[0], cell_end[1]):
            game.choosing_cell = cell_end
        else:
            print("\033[91mUnable to move the ball: cell unreachable or blocked\033[0m")

    @staticmethod
    def handle_post_move(game: Game, cell_end: tuple):
        GameService.delete_balls(game, cell_end)
        GameService.end_move(game)

    @staticmethod
    def search_line(game: Game, start_cell: tuple, delta_row: int, delta_col: int):
        line = [start_cell]
        color = game.area[start_cell].color if game.area[start_cell] else None
        current_cell = (start_cell[0] + delta_row, start_cell[1] + delta_col)

        while 0 <= current_cell[0] < game.size and 0 <= current_cell[1] < game.size:
            if game.area[current_cell] is not None and game.area[current_cell].color == color:
                line.append(current_cell)
                current_cell = (current_cell[0] + delta_row, current_cell[1] + delta_col)
            else:
                break

        return line

    @staticmethod
    def delete_balls(game: Game, cell: tuple):
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        deleted = False

        for delta_row, delta_col in directions:
            line = GameService.search_line(game, cell, delta_row, delta_col) + \
                    GameService.search_line(game, cell, -delta_row, -delta_col)[1:]
            if len(line) >= game.count_balls_line:
                for cell_to_delete in line:
                    game.area[cell_to_delete] = None
                game.points += len(line)
                deleted = True

        return deleted

    @staticmethod
    def can_move_ball(game: Game, cell_start: tuple, cell_end: tuple):
        if cell_start not in game.area or cell_end not in game.area:
            print("\033[91mError: One of the cells is outside the playing field\033[0m")
            return False
        return not GameService.is_big_ball(game, cell_end[0], cell_end[1]) and \
            GameService.is_bfs(game, cell_start, cell_end)

    @staticmethod
    def is_bfs(game: Game, s: tuple, d: tuple):
        visited = {key: False for key in game.area}
        queue = collections.deque([s])
        visited[s] = True

        while queue:
            n = queue.popleft()
            if n == d:
                return True
            for i in game.graph.adj_lists[n]:
                if not visited[i]:
                    queue.append(i)
                    visited[i] = True
        return False

    @staticmethod
    def rework_graph(game: Game):
        for cell in game.area.keys():
            game.graph.adj_lists[cell].clear()
            for adj in GameService.get_adj_cell(game, cell):
                if not game.area.get(adj) or game.area.get(adj).size == Size.small:
                    game.graph.adj_lists[cell].append(adj)

    @staticmethod
    def is_game_over(game: Game):
        if not game.get_empty_cell():
            print("\033[91mGame Over: No space left for new balls\033[0m")
            return True

        for key in game.area.keys():
            if game.area[key] and any(game.area.get(adj) is None for adj in GameService.get_adj_cell(game, key)):
                return False
        return True

    @staticmethod
    def get_adj_cell(game: Game, cell: tuple):
        cells = []
        if cell[0] - 1 >= 0:
            cells.append((cell[0] - 1, cell[1]))

        if cell[0] + 1 < game.size:
            cells.append((cell[0] + 1, cell[1]))

        if cell[1] - 1 >= 0:
            cells.append((cell[0], cell[1] - 1))

        if cell[1] + 1 < game.size:
            cells.append((cell[0], cell[1] + 1))

        return cells

    @staticmethod
    def load_highscores(filename="highscores.txt"):
        try:
            with open(filename, "r") as file:
                highscores = []
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) == 2:
                        name, points = parts
                        try:
                            points = int(points)
                            highscores.append((name, points))
                        except ValueError:
                            continue
                return highscores
        except FileNotFoundError:
            return []

    @staticmethod
    def save_highscore(name, points, filename="highscores.txt"):
        with open(filename, "a") as file:
            file.write(f"{name},{points}\n")