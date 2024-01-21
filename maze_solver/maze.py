import random
import time

from maze_solver.window import Window
from maze_solver.cell import Cell
from maze_solver.point import Point

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win: Window = None,
                 seed = None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._sleep = 0.0005

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls(0, 0)
        self._reset_cells_visited()

        self._sleep = 0.05

    def _create_cells(self):
        self._cells = []

        for c in range(self._num_cols):
            col = []
            for r in range(self._num_rows):
                col.append(Cell(self._win))
            self._cells.append(col)

        for col in range(len(self._cells)):
            for row in range(len(self._cells[col])):
                self._draw_cell(col, row)

    def _draw_cell(self, col, row):
        top_left = Point(self._x1 + col * self._cell_size_x, self._y1 + row * self._cell_size_y)
        bottom_right = Point(self._x1 + (col + 1) * self._cell_size_x, self._y1 + (row + 1) * self._cell_size_y)

        self._cells[col][row].draw(top_left, bottom_right)

        self._animate()

    def _animate(self):
        if self._win is None:
            return

        self._win.redraw()

        time.sleep(self._sleep)

    def _break_entrance_and_exit(self):
        top_left_cell = self._cells[0][0]
        top_left_cell.top_wall = False
        self._draw_cell(0, 0)

        right = len(self._cells) - 1
        bottom = len(self._cells[right]) - 1
        bottom_right_cell = self._cells[right][bottom]
        bottom_right_cell.bottom_wall = False
        self._draw_cell(right, bottom)

    def _neighbors(self, col, row):
        neighbors = []
        for n in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if col + n[0] >= 0 and col + n[0] < len(self._cells) and \
                row + n[1] >= 0 and row + n[1] < len(self._cells[col]):
                neighbors.append((col + n[0], row + n[1]))
        return neighbors

    def _get_cell(self, cell):
        return self._cells[cell[0]][cell[1]]

    def _remove_walls(self, a, b):
        if a[0] > b[0]:
            self._get_cell(a).left_wall = False
            self._get_cell(b).right_wall = False
        elif a[0] < b[0]:
            self._get_cell(a).right_wall = False
            self._get_cell(b).left_wall = False
        elif a[1] > b[1]:
            self._get_cell(a).top_wall = False
            self._get_cell(b).bottom_wall = False
        elif a[1] < b[1]:
            self._get_cell(a).bottom_wall = False
            self._get_cell(b).top_wall = False

    def _break_walls(self, col, row):
        current = (col, row)
        self._cells[col][row].visited = True
        while True:
            to_visit = []
            for n in self._neighbors(col, row):
                if not self._cells[n[0]][n[1]].visited:
                    to_visit.append(n)

            if len(to_visit) == 0:
                self._draw_cell(col, row)
                return

            dir = random.choice(to_visit)
            self._remove_walls((col, row), dir)
            self._break_walls(dir[0], dir[1])

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, col, row):
        self._animate()

        current = self._get_cell((col, row))
        current.visited = True

        if col == self._num_cols - 1 and row == self._num_rows - 1:
            return True

        for n in self._neighbors(col, row):
            neighbor = self._get_cell(n)
            if neighbor.visited:
                continue

            if ((n[0] > col and not current.right_wall and not neighbor.left_wall) or
                (n[0] < col and not current.left_wall and not neighbor.right_wall) or
                (n[1] > row and not current.bottom_wall and not neighbor.top_wall) or
                (n[1] < row and not current.top_wall and not neighbor.bottom_wall)):
                current.draw_move(neighbor)
                result = self._solve_r(n[0], n[1])
                if result:
                    return True
                current.draw_move(neighbor, True)
        return False
