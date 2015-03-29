import numpy
import random
import string
import cv2


class Puzzle:
    def __init__(self, pieces, orig):
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
        self.orig = orig

    def seedplaced(self):
        return self.sol.max() != -1

    def placeseed(self):
        seedid = random.randint(0, (self.xsize * self.ysize) - 1)
        seedpiece = self.pieces[seedid]
        posx = random.randint(0, self.xsize - 1)
        posy = random.randint(0, self.ysize - 1)
        rotation = random.randint(0, 3)
        # rotation = 0
        self.sol[posx][posy][0] = seedpiece.id
        self.sol[posx][posy][1] = rotation

    def mostinformativepos(self):
        best = 0
        bestindex = []
        for x in range(0, self.xsize):
            for y in range(0, self.ysize):
                if self.sol[x][y][0] == -1:
                    neighbours = []
                    if x > 0:
                        if self.sol[x - 1][y][0] != -1:
                            neighbours.append((x - 1, y))
                    if x < self.xsize - 1:
                        if self.sol[x + 1][y][0] != -1:
                            neighbours.append((x + 1, y))
                    if y > 0:
                        if self.sol[x][y - 1][0] != -1:
                            neighbours.append((x, y - 1))
                    if y < self.ysize - 1:
                        if self.sol[x][y + 1][0] != -1:
                            neighbours.append((x, y + 1))
                    if len(neighbours) == best:
                        bestindex.append((x, y, neighbours))
                    if len(neighbours) > best:
                        best = len(neighbours)
                        bestindex = [(x, y, neighbours)]

        return bestindex

    def getbestbuddies(self, position):
        x, y, neighbours = position
        buddies = []
        for neigh in neighbours:
            currentsol = self.sol[neigh[0]][neigh[1]]
            piece = self.pieces[currentsol[0]]
            if x < neigh[0]:
                side = 0
            if x > neigh[0]:
                side = 1
            if y > neigh[1]:
                side = 3
            if y < neigh[1]:
                side = 2
            buddies.append(piece.bestbuddies[side])
        return buddies

    def getbestpossible(self, position):
        x, y, neighbours = position
        metrics = []
        for neigh in neighbours:
            currentsol = self.sol[neigh[0]][neigh[1]]
            piece = self.pieces[currentsol[0]]
            if x < neigh[0]:
                side = 0
            if x > neigh[0]:
                side = 1
            if y > neigh[1]:
                side = 3
            if y < neigh[1]:
                side = 2
            metrics.append(piece.metrics[side])
        # TODO rotation wise summing
        if len(metrics) == 1:
            summ = numpy.add(metrics[0], numpy.zeros_like(metrics[0]))
        if len(metrics) == 2:
            summ = numpy.add(metrics[0], metrics[1])
        if len(metrics) == 3:
            summ = numpy.add(metrics[0], numpy.add(metrics[1], metrics[2]))
        if len(metrics) == 4:
            summ = numpy.add(numpy.add(metrics[0], metrics[1]), numpy.add(metrics[2], metrics[3]))

        pieceid = -1
        rotation = -1
        while True:
            flatmax = numpy.nanargmax(summ)
            maxtuple = numpy.unravel_index(flatmax, summ.shape)
            pieceid = maxtuple[2]
            if self.isset(pieceid):
                summ[maxtuple[0]][maxtuple[1]][maxtuple[2]] = -1
            else:
                rotation = maxtuple[0]
                break

        return pieceid, rotation

    def allset(self):
        return not self.isset(-1)

    def isset(self, pieceid):
        for y in range(0, self.ysize):
            for x in range(0, self.xsize):
                if self.sol[x][y][0] == pieceid:
                    return True
        return False

    def calculatemetrics(self):
        for piece in self.pieces:
            piece.calculatemetrics(self.pieces)
        for piece in self.pieces:
            piece.calculatebestbuddies(self.pieces)

    def addtosol(self, x, y, pieceid, rotation):
        self.sol[x][y][0] = pieceid
        self.sol[x][y][1] = rotation
        self.sol[x][y][2] = -1

    def showsol(self):
        dummy = numpy.full_like(self.pieces[0].image, 0)
        columns = []
        for i in range(0, self.xsize):
            columns.append([])
            for j in range(0, self.ysize):
                sol = self.sol[i][j]
                if sol[0] == -1:
                    columns[i].append(dummy)
                else:
                    if sol[1] == 0:
                        columns[i].append(self.pieces[sol[0]].image)
                    if sol[1] == 1:
                        columns[i].append(numpy.rot90(self.pieces[sol[0]].image, 2))
                    if sol[1] == 2:
                        columns[i].append(numpy.rot90(self.pieces[sol[0]].image, 1))
                    if sol[1] == 3:
                        columns[i].append(numpy.rot90(self.pieces[sol[0]].image, 3))
        imagecols = []
        for col in columns:
            imagecols.append(numpy.vstack(col))
        image = numpy.hstack(imagecols)

        cv2.imshow("Original", self.orig)
        cv2.imshow("Solved", image)

    def __str__(self):
        data = ["Puzzle {0}x{1}\r\n".format(self.xsize, self.ysize)]
        for y in range(0, self.ysize):
            for x in range(0, self.xsize):
                data.append("[{0},{1}] ".format(self.sol[x][y][0], self.sol[x][y][1]))
            data.append("\r\n")
        return string.join(data, '')