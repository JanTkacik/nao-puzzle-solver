def shift(puzzle):
    puzzle.leaveonlybestsegment()
    moved = puzzle.replacesegment()
    if not moved:
        print "Cannot move puzzle"
    print puzzle
    return moved