from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self._root = Tk()
        self._root.title = "Maze Solver"
        self._root.protocol("WM_DELETE_WINDOW", self.close)

        self._canvas = Canvas(self._root, height=height, width=width, background="white")
        self._canvas.pack(fill=BOTH, expand=1)
        self.running = False

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color="black"):
        line.draw(self._canvas, fill_color)

