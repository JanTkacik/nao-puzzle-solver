class Piece:
    def __init__(self, image, pieceid=-1, realx=-1, realy=-1):
        self.image = image
        self.realx = realx
        self.realy = realy
        self.id = pieceid
        self.x = -1
        self.y = -1

    def __str__(self):
        return "[{0}][{1},{2}]".format(self.id, self.realx, self.realy)