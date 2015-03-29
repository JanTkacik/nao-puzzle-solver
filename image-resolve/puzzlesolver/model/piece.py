import numpy
import math
from puzzlesolver.metrics import dissimilarity


class Piece:
    metrics = [dissimilarity.dissimilarity]

    def __init__(self, image, pieceid, realx=-1, realy=-1, realdir=0):
        self.image = image
        self.realx = realx
        self.realy = realy
        self.realdir = realdir
        self.id = pieceid
        self.x = -1
        self.y = -1
        self.metrics = None
        self.bestbuddies = numpy.full((4, 2), -1, int)

    def calculatemetrics(self, pieces):
        #               4 sides, 4 sides on other piece, x metric, len pieces
        self.metrics = numpy.full((4, 4, len(Piece.metrics), len(pieces)), numpy.nan)
        for piece in pieces:
            if piece.id != self.id:
                for selfside in range(0, 4):
                    selfvec = self.getside(selfside)
                    for otherside in range(0, 4):
                        #  Self, Other      0         1         2         3
                        # ------------- --------- --------- --------- ---------
                        #            0   Rotated   Normal    Normal    Rotated
                        #            1   Normal    Rotated   Rotated   Normal
                        #            2   Normal    Rotated   Rotated   Normal
                        #            3   Rotated   Normal    Normal    Rotated
                        if otherside == selfside or (otherside + selfside == 3):
                            othervec = piece.getrotatedside(otherside)
                        else:
                            othervec = piece.getside(otherside)
                        for metricid in range(0, len(Piece.metrics)):
                            self.metrics[selfside][otherside][metricid][piece.id] = \
                                Piece.metrics[metricid](selfvec, othervec)

        for selfside in range(0, 4):
            for otherside in range(0, 4):
                vector = self.metrics[selfside][otherside][0]
                quartile = numpy.percentile(vector, 25)
                for i in range(0, vector.shape[0]):
                    vector[i] = math.exp(-(vector[i] / quartile))

    def calculatebestbuddies(self, pieces):
        for selfside in range(0, 4):
            if self.bestbuddies[selfside][0] == -1:
                bestmatch = numpy.nanargmax(self.metrics[selfside])
                bestmatchtuple = numpy.unravel_index(bestmatch, self.metrics[selfside].shape)

                buddyid = bestmatchtuple[2]
                buddypiece = pieces[buddyid]
                buddyside = bestmatchtuple[0]
                buddyvector = buddypiece.metrics[buddyside]
                buddymatch = numpy.nanargmax(buddyvector)
                buddymatchtuple = numpy.unravel_index(buddymatch, buddyvector.shape)

                # my buddy piece best match is me
                if buddymatchtuple[2] == self.id:
                    # even sides must match
                    if buddymatchtuple[0] == selfside:
                        # and metrics type
                        if buddymatchtuple[1] == bestmatchtuple[1]:
                            self.bestbuddies[selfside][0] = buddyid
                            self.bestbuddies[selfside][1] = buddyside
                            buddypiece.bestbuddies[buddyside][0] = self.id
                            buddypiece.bestbuddies[buddyside][1] = selfside
        # print "Best buddies for piece {0} are \r\n {1}".format(self, self.bestbuddies)

    def getside(self, sideid):
        if sideid == 0:
            return self.image[:, 0]
        if sideid == 1:
            return self.image[:, self.image.shape[1] - 1]
        if sideid == 2:
            return self.image[0, :]
        if sideid == 3:
            return self.image[self.image.shape[0] - 1, :]
        return None

    def getrotatedside(self, sideid):
        side = self.getside(sideid)
        return numpy.fliplr(side)

    def __str__(self):
        return "[{0}][{1},{2}][{3}]".format(self.id, self.realx, self.realy, self.realdir)