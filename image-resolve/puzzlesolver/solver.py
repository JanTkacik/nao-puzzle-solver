import model.piece
import model.puzzle
import cv2
import argparse
import os
import re

ispiecere = re.compile("^\d*_\d*_\d*\..*")


def main():
    args = parse_args()
    puzzle = loadpuzzle(args.imagesdirectory)
    print(puzzle)


def loadpuzzle(imagedir):
    pieces = []
    idnum = 0
    files = os.listdir(imagedir)
    for filename in files:
        if ispiece(filename):
            pieces.append(loadpiece(imagedir, filename, idnum))
            idnum += 1
    return model.puzzle.Puzzle(pieces)


def loadpiece(imagedir, filename, idnum=-1):
    piecedata = getpiecedata(filename)
    image = cv2.imread(os.path.join(imagedir, filename))
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