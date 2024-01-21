from __future__ import annotations

from maze_solver.window import Window
from maze_solver.point import Point
from maze_solver.line import Line

class Cell:
    def __init__(self, window: Window = None):
        self.left_wall = True
        self.right_wall = True
        self.top_wall = True
        self.bottom_wall = True

        self.visited = False

        self._win = window

    def walls(self):
        return (self.top_wall, self.right_wall, self.bottom_wall, self.left_wall)

    def draw(self, top_left: Point, bottom_right: Point):
        if self._win is None:
            return

        self.__top_left = top_left
        self.__bottom_right = bottom_right

        bottom_left = Point(top_left.x, bottom_right.y)
        top_right = Point(bottom_right.x, top_left.y)

        color = self.top_wall and "black" or "white"
        self._win.draw_line(Line(top_left, top_right), color)

        color = self.right_wall and "black" or "white"
        self._win.draw_line(Line(top_right, bottom_right), color)

        color = self.bottom_wall and "black" or "white"
        self._win.draw_line(Line(bottom_right, bottom_left), color)

        color = self.left_wall and "black" or "white"
        self._win.draw_line(Line(top_left, bottom_left), color)

    def middle(self):
        middle_x = (self.__top_left.x + self.__bottom_right.x) / 2
        middle_y = (self.__top_left.y + self.__bottom_right.y) / 2

        return Point(middle_x, middle_y)

    def draw_move(self, to_cell: Cell, undo=False):
        color = undo and "red" or "gray"

        self._win.draw_line(Line(self.middle(), to_cell.middle()), color)
