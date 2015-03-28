class Puzzle:
    def __init__(self, pieces):
        maxx = 0
        maxy = 0
        for piece in pieces:
            if piece.realx > maxx:
                maxx = piece.realx
            if piece.realy > maxy:
                maxy = piece.realy

        self.xsize = maxx + 1
        self.ysize = maxy + 1
        self.pieces = pieces

    def __str__(self):
        return "Puzzle {0}x{1}".format(self.xsize, self.ysize)