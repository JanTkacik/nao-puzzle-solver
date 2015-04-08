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
            bestbuddy = getbestpossiblebuddy(bbl)
            print "Best buddy: {0}".format(bestbuddy)
            if bestbuddy[0] != -1:
                puzzle.addtosol(x, y, bestbuddy[0], bestbuddy[1])
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


def getbestpossiblebuddy(bestbudlist):
    if len(bestbudlist) == 1:
        return bestbudlist[0]

    buddycnt = {}
    pieces = {}
    for buddy in bestbudlist:
        if buddy[0] in pieces:
            if buddy[1] == pieces[buddy[0]]:
                buddycnt[(buddy[0], buddy[1])] += 1
            else:
                buddycnt[(buddy[0], buddy[1])] = 1
        else:
            pieces[buddy[0]] = buddy[1]
            buddycnt[(buddy[0], buddy[1])] = 1

    maxcnt = 0
    maxbuddy = (-1, -1)
    for buddy in buddycnt:
        if buddy != (-1, -1):
            if buddycnt[buddy] > maxcnt:
                maxcnt = buddycnt[buddy]
                maxbuddy = buddy
    return maxbuddy

