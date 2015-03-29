def place(puzzle):
    if not puzzle.seedplaced():
        puzzle.placeseed()
    pos = puzzle.mostinformativepos()

    for position in pos:
        bbl = puzzle.getbestbuddies(position)
        print bbl
        if hasonlyonepiece(bbl):
            x, y, neighbours = position
            rotation = getrotation(x, y, neighbours, bbl)
            if rotation is not None:
                puzzle.addtosol(x, y, bbl[0][0], rotation)
                break
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