import model.piece
import model.puzzle
import cv2
import argparse
import os
import re
import placer
import shifter
import numpy

ispiecere = re.compile("^\d*_\d*_\d*\..*")


def main():
    args = parse_args()
    puzzle = loadpuzzle(args.imagesdirectory)
    solve(puzzle)
    print puzzle
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if puzzle.video is not None:
        puzzle.video.release()


def solve(puzzle):
    oldsol = None
    while True:
        placer.place(puzzle)
        moved = shifter.shift(puzzle)
        if not moved:
            break
        if puzzle.hasonlyonesegment():
            break
        if oldsol is not None:
            if (oldsol == puzzle.sol).all():
                break
        oldsol = numpy.copy(puzzle.sol)


def loadpuzzle(imagedir):
    pieces = []
    idnum = 0
    files = os.listdir(imagedir)
    for filename in files:
        if ispiece(filename):
            pieces.append(loadpiece(imagedir, filename, idnum))
            idnum += 1
        if filename == "orig.png":
            orig = cv2.imread(os.path.join(imagedir, filename))

    return model.puzzle.Puzzle(pieces, orig, os.path.join(imagedir, "video.avi"))
    # return model.puzzle.Puzzle(pieces, orig)


def loadpiece(imagedir, filename, idnum=-1):
    piecedata = getpiecedata(filename)
    image = cv2.imread(os.path.join(imagedir, filename))
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return model.piece.Piece(image, idnum, int(piecedata[1]), int(piecedata[2]))


def getpiecedata(filename):
    name, ext = os.path.splitext(filename)
    return re.split("_", name)


def ispiece(filename):
    return ispiecere.match(filename) is not None


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("imagesdirectory")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
