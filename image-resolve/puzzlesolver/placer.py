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
                puzzle.addtosol(x, y, bbl[0][0], bbl[0][1])
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


def hasonlyonepiece(bestbudlist):
    pieces = {}
    for buddy in bestbudlist:
        if buddy[0] in pieces:
            if buddy[1] != pieces[buddy[0]]:
                return False
        pieces[buddy[0]] = buddy[1]

    if -1 in pieces:
        return False
    if len(pieces) == 1:
        return True
    return False