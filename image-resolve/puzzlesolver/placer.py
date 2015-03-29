def place(puzzle):
    if not puzzle.seedplaced():
        puzzle.placeseed()
        print "Seed placed"
        print puzzle

    while not puzzle.allset():
        added = False
        pos = puzzle.mostinformativepos()
        print "Most informative positions {0}".format(pos)
        for position in pos:
            x, y, neighbours = position
            print "Position: {0}".format(position)
            bbl = puzzle.getbestbuddies(position)
            print "Best buddies: {0}".format(bbl)
            if hasonlyonepiece(bbl):
                rotation = getrotation(x, y, neighbours, bbl)
                if rotation is not None:
                    puzzle.addtosol(x, y, bbl[0][0], rotation)
                    added = True
                    break
        if not added:
            for position in pos:
                print "Correct best buddy not found"
                nml = puzzle.getbestpossible(position)
                print "Best possible piece id {0} with rotation {1}".format(nml[0], nml[1])
                puzzle.addtosol(x, y, nml[0], nml[1])
                break
        print puzzle
    puzzle.showsol()

rotationmatrix = \
    [
        [2, 0, 3, 1],
        [0, 2, 1, 3],
        [1, 3, 2, 0],
        [3, 1, 0, 2]
    ]


def getrotation(x, y, neighbours, bestbudlist):
    rotation = -1

    for i in range(0, len(neighbours)):
        nx = neighbours[i][0]
        ny = neighbours[i][1]
        buddyside = bestbudlist[i][1]
        # on the left
        if x < nx:
            pieceside = 0
        # on the right
        if x > nx:
            pieceside = 1
        # on the bottom
        if y < ny:
            pieceside = 2
        # on the top
        if y > ny:
            pieceside = 3

        if rotation == -1:
            rotation = rotationmatrix[pieceside][buddyside]
        if rotation != rotationmatrix[pieceside][buddyside]:
            return None
    return rotation


def hasonlyonepiece(bestbudlist):
    pieces = {}
    for buddy in bestbudlist:
        pieces[buddy[0]] = buddy[1]

    if -1 in pieces:
        return False
    if len(pieces) == 1:
        return True
    return False