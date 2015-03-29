def place(puzzle):
    if not puzzle.seedplaced():
        puzzle.placeseed()
    pos = puzzle.mostinformativepos()
    for position in pos:
        print position
    pass
