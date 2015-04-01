import numpy
import random
import string
import cv2
from puzzlesolver.metrics.helper import *


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
        self.maxsegid = 0
        self.piecesposition = {}
        self.shiftside = 0

    def seedplaced(self):
        return self.sol.max() != -1

    def placeseed(self):
        seedid = random.randint(0, (self.xsize * self.ysize) - 1)
        seedpiece = self.pieces[seedid]
        posx = random.randint(0, self.xsize - 1)
        posy = random.randint(0, self.ysize - 1)
        rotation = random.randint(0, 3)
        self.addtosol(posx, posy, seedpiece.id, rotation)

    def mostinformativepos(self):
        mostneighbours = 0
        bestindexes = []
        for x in range(0, self.xsize):
            for y in range(0, self.ysize):
                if self.sol[x][y][0] == -1:
                    neighbours = self.getneighbours(x, y)
                    if len(neighbours) == mostneighbours:
                        bestindexes.append((x, y, neighbours))
                    if len(neighbours) > mostneighbours:
                        mostneighbours = len(neighbours)
                        bestindexes = [(x, y, neighbours)]

        return bestindexes

    def getneighbours(self, x, y):
        neighbours = []
        if x > 0:
            if self.sol[x - 1][y][0] != -1:
                neighbours.append(self.sol[x - 1][y])
        if x < self.xsize - 1:
            if self.sol[x + 1][y][0] != -1:
                neighbours.append(self.sol[x + 1][y])
        if y > 0:
            if self.sol[x][y - 1][0] != -1:
                neighbours.append(self.sol[x][y - 1])
        if y < self.ysize - 1:
            if self.sol[x][y + 1][0] != -1:
                neighbours.append(self.sol[x][y + 1])
        return neighbours

    def getbestbuddies(self, position):
        x, y, neighbours = position
        buddies = []
        for neigh in neighbours:
            neighpos = self.getpiecepos(neigh[0])
            neighpiece = self.pieces[neigh[0]]
            neighrot = neigh[1]
            bestbuddy = neighpiece.getbestbuddyfor(neighpos[0], neighpos[1], neighrot, x, y)
            if not bestbuddy[0] in self.piecesposition:
                buddies.append(bestbuddy)
            else:
                buddies.append(numpy.full(2, -1, int))
        return buddies

    def getpiecepos(self, pieceid):
        return self.piecesposition[pieceid]

    def getbestpossible(self, position):
        x, y, neighbours = position
        metrics = []
        for neigh in neighbours:
            neighpos = self.getpiecepos(neigh[0])
            neighpiece = self.pieces[neigh[0]]
            neighrot = neigh[1]
            side = gettouchingside(neighpos[0], neighpos[1], neighrot, x, y)
            metrics.append(neighpiece.metrics[side])
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
        self.sol[x][y][2] = self.getsegmentid(x, y, rotation)
        self.piecesposition[pieceid] = (x, y)

    def getsegmentid(self, x, y, r):
        neighbours = self.getneighbours(x, y)
        piece = self.pieces[self.sol[x][y][0]]
        segids = []
        for neigh in neighbours:
            otherposition = self.piecesposition[neigh[0]]
            if piece.isbestbuddywith(x, y, r, otherposition[0], otherposition[1], neigh[1]):
                segids.append(neigh[2])
            else:
                segids.append(-1)
        if len(segids) == 0:
            return self.getnewsegmentid()
        if -1 in segids:
            return self.getnewsegmentid()
        if len(frozenset(segids)):
            return segids[0]
        return -2

    def getlargestsegment(self):
        segcount = {}
        for i in range(0, self.xsize):
            for j in range(0, self.ysize):
                seg = self.sol[i][j][2]
                if seg in segcount:
                    segcount[seg] += 1
                else:
                    segcount[seg] = 1
        maxcount = 0
        maxseg = -1
        for count in segcount:
            if segcount[count] > maxcount:
                maxcount = segcount[count]
                maxseg = count

        return maxseg

    def getnewsegmentid(self):
        segid = self.maxsegid
        self.maxsegid += 1
        return segid

    def leaveonlybestsegment(self):
        best = self.getlargestsegment()
        for i in range(0, self.xsize):
            for j in range(0, self.ysize):
                seg = self.sol[i][j][2]
                if seg != best:
                    self.removepiece(i, j)

    def removepiece(self, x, y):
        old = self.sol[x][y][0]
        self.sol[x][y][0] = -1
        self.sol[x][y][1] = -1
        self.sol[x][y][2] = -1
        del self.piecesposition[old]

    def hasonlyonesegment(self):
        only = -2
        for x in range(0, self.xsize):
            for y in range(0, self.ysize):
                seg = self.sol[x][y][2]
                if seg == -1:
                    return False
                if only == -2:
                    only = seg
                if seg != only:
                    return False
        return True

    def replacesegment(self):
        minx, maxx, miny, maxy = self.getsegmentsize()
        xsize = maxx - minx + 1
        ysize = maxy - miny + 1

        if xsize <= self.ysize and ysize <= self.xsize:
            newsol = numpy.full((self.xsize, self.ysize, 3), -1, int)
            for x in range(minx, maxx + 1):
                for y in range(miny, maxy + 1):
                    newsol[y][maxx - x - minx] = self.sol[x][y]

            for x in range(0, self.xsize):
                for y in range(0, self.ysize):
                    rot = newsol[x][y][1]
                    if rot != -1:
                        newsol[x][y][1] = getclockwiseside(rot)
        else:
            newsol = numpy.copy(self.sol)
        self.clearboard()

        emptycols = range(0, self.xsize)
        fullcols = []
        emptyrows = range(0, self.ysize)
        fullrows = []

        for x in range(0, self.xsize):
            for y in range(0, self.ysize):
                if newsol[x][y][0] != -1:
                    if x in emptycols:
                        fullcols.append(x)
                        emptycols.remove(x)
                    if y in emptyrows:
                        fullrows.append(y)
                        emptyrows.remove(y)

        if self.shiftside == 0:
            self.shiftside = 1
            shift = min(fullcols)
            for x in range(0, self.xsize):
                for y in range(0, self.ysize):
                    if newsol[x][y][0] != -1:
                        self.addtosol(x - shift, y, newsol[x][y][0], newsol[x][y][1])
            return

        if self.shiftside == 1:
            self.shiftside = 2
            shift = self.xsize - 1 - max(fullcols)
            for x in range(0, self.xsize):
                for y in range(0, self.ysize):
                    if newsol[x][y][0] != -1:
                        self.addtosol(x + shift, y, newsol[x][y][0], newsol[x][y][1])
            return

        if self.shiftside == 2:
            self.shiftside = 3
            shift = min(fullrows)
            for x in range(0, self.xsize):
                for y in range(0, self.ysize):
                    if newsol[x][y][0] != -1:
                        self.addtosol(x, y - shift, newsol[x][y][0], newsol[x][y][1])
            return

        if self.shiftside == 3:
            self.shiftside = 0
            shift = self.ysize - 1 - max(fullrows)
            for x in range(0, self.xsize):
                for y in range(0, self.ysize):
                    if newsol[x][y][0] != -1:
                        self.addtosol(x, y + shift, newsol[x][y][0], newsol[x][y][1])
            return

    def clearboard(self):
        self.maxsegid = 0
        for x in range(0, self.xsize):
            for y in range(0, self.ysize):
                if self.sol[x][y][0] != -1:
                    self.removepiece(x, y)

    def getsegmentsize(self):
        minx, maxx, miny, maxy = self.xsize + 1, 0, self.ysize + 1, 0
        for i in range(0, self.xsize):
            for j in range(0, self.ysize):
                if self.sol[i][j][2] != -1:
                    if i < minx:
                        minx = i
                    if i > maxx:
                        maxx = i
                    if j < miny:
                        miny = j
                    if j > maxy:
                        maxy = j
        return minx, maxx, miny, maxy

    def generatesegmentsquare(self, segid):
        return numpy.full_like(self.pieces[0].image, segid * 15)

    def showsol(self):
        dummy = numpy.full_like(self.pieces[0].image, 0)
        columns = []
        columnsseg = []
        for i in range(0, self.xsize):
            columns.append([])
            columnsseg.append([])
            for j in range(0, self.ysize):
                sol = self.sol[i][j]
                columnsseg[i].append(self.generatesegmentsquare(sol[2]))
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
        imagesegcols = []
        for col in columns:
            imagecols.append(numpy.vstack(col))
        for segcol in columnsseg:
            imagesegcols.append(numpy.vstack(segcol))
        image = numpy.hstack(imagecols)
        imageseg = numpy.hstack(imagesegcols)

        cv2.imshow("Original", self.orig)
        cv2.imshow("Solved", image)
        cv2.imshow("Segments", imageseg)

        self.getlargestsegment()

    def __str__(self):
        data = ["Puzzle {0}x{1}\r\n".format(self.xsize, self.ysize)]
        for y in range(0, self.ysize):
            for x in range(0, self.xsize):
                data.append("[{0},{1},{2}] ".format(self.sol[x][y][0], self.sol[x][y][1], self.sol[x][y][2]))
            data.append("\r\n")
        return string.join(data, '')