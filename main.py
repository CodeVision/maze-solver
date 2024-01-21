from maze_solver.window import Window
from maze_solver.line import Line
from maze_solver.point import Point
from maze_solver.cell import Cell
from maze_solver.maze import Maze


if __name__ == "__main__":
    win = Window(800, 600)

    maze = Maze(25, 25, 22, 30, 25, 25, win)
    maze.solve()

    win.wait_for_close()
