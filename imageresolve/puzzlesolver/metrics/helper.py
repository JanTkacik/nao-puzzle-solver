def getrelativeposition(x1, y1, x2, y2):
    if x1 < x2:
        return 0  # first piece is on the left
    if x1 > x2:
        return 1  # right
    if y1 < y2:
        return 2  # up
    if y1 > y2:
        return 3  # down


def getcorrespondingsides(x1, y1, r1, x2, y2, r2):
    relpos = getrelativeposition(x1, y1, x2, y2)
    if relpos == 0:
        return getoppositeside(r1), r2
    if relpos == 1:
        return r1, getoppositeside(r2)
    if relpos == 2:
        return getcounterclockwiseside(r1), getclockwiseside(r2)
    if relpos == 3:
        return getclockwiseside(r1), getcounterclockwiseside(r2)


def gettouchingside(x1, y1, r1, x2, y2):
    relpos = getrelativeposition(x1, y1, x2, y2)
    if relpos == 0:
        return getoppositeside(r1)
    if relpos == 1:
        return r1
    if relpos == 2:
        return getcounterclockwiseside(r1)
    if relpos == 3:
        return getclockwiseside(r1)


def getoppositeside(r):
    if r == 0:
        return 1
    if r == 1:
        return 0
    if r == 2:
        return 3
    if r == 3:
        return 2


def getclockwiseside(r):
    if r == 0:
        return 2
    if r == 1:
        return 3
    if r == 2:
        return 1
    if r == 3:
        return 0


def getcounterclockwiseside(r):
    if r == 0:
        return 3
    if r == 1:
        return 2
    if r == 2:
        return 0
    if r == 3:
        return 1