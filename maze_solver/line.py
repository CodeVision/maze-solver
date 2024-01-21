class Line:
    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2

    def draw(self, canvas, fill_color):
        p1, p2 = self._p1, self._p2
        canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill=fill_color, width=2)
        canvas.pack()
