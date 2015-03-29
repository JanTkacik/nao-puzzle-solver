import numpy
import random
import string


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
        # solution is vector of 3 integers - pieceId, rotation, segmentId
        self.sol = numpy.full((self.xsize, self.ysize, 3), -1, int)
        self.calculatemetrics()

    def seedplaced(self):
        return self.sol.max() != -1

    def placeseed(self):
        seedid = random.randint(0, (self.xsize * self.ysize) - 1)
        seedpiece = self.pieces[seedid]
        posx = random.randint(0, self.xsize - 1)
        posy = random.randint(0, self.ysize - 1)
        rotation = random.randint(0, 3)
        self.sol[posx][posy][0] = seedpiece.id
        self.sol[posx][posy][1] = rotation

    def mostinformativepos(self):
        best = 0
        bestindex = []
        for x in range(0, self.xsize):
            for y in range(0, self.ysize):
                current = 0
                if x > 0:
                    if self.sol[x - 1][y][0] != -1:
                        current += 1
                if x < self.xsize - 1:
                    if self.sol[x + 1][y][0] != -1:
                        current += 1
                if y > 0:
                    if self.sol[x][y - 1][0] != -1:
                        current += 1
                if y < self.ysize - 1:
                    if self.sol[x][y + 1][0] != -1:
                        current += 1
                if current == best:
                    bestindex.append((x, y))
                if current > best:
                    best = current
                    bestindex = [(x, y)]

        return bestindex

    def calculatemetrics(self):
        for piece in self.pieces:
            piece.calculatemetrics(self.pieces)
        for piece in self.pieces:
            piece.calculatebestbuddies(self.pieces)

    def __str__(self):
        data = ["Puzzle {0}x{1}\r\n".format(self.xsize, self.ysize)]
        for y in range(0, self.ysize):
            for x in range(0, self.xsize):
                data.append("[{0},{1}] ".format(self.sol[x][y][0], self.sol[x][y][1]))
            data.append("\r\n")
        return string.join(data, '')