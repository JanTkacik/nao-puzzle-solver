import sys

from PyQt4.QtGui import QWidget, QImage, QApplication, QPainter
from naoqi import ALProxy

# To get the constants relative to the video.
import vision_definitions
import cv2
import numpy as np
import imageresolve.puzzlesolver.solver as slv
import imageextractor.imageextractor as ext
import imageresolve.puzzlesolver.model.puzzle as pzl
import imageresolve.puzzlesolver.model.piece as pcl

def convertimage(incomingimage):
    incomingimage = incomingimage.convertToFormat(4)
    width = incomingimage.width()
    height = incomingimage.height()
    ptr = incomingimage.bits()
    ptr.setsize(incomingimage.byteCount())
    arr = np.array(ptr).reshape(height, width, 4)
    return arr

if __name__ == '__main__':
    IP = "127.0.0.1"
    PORT = 9559
    CameraID = 1

    # Read IP address from first argument if any.
    if len(sys.argv) > 1:
        IP = sys.argv[1]

    # Read CameraID from second argument if any.
    if len(sys.argv) > 2:
        CameraID = int(sys.argv[2])

    videoProxy = ALProxy("ALVideoDevice", IP, PORT)
    resolution = vision_definitions.k4VGA  # 320 * 240
    colorSpace = vision_definitions.kRGBColorSpace
    imgClient = videoProxy.subscribe("_client", resolution, colorSpace, 5)
    # Select camera.
    videoProxy.setParam(vision_definitions.kCameraSelectID, CameraID)

    alImage = videoProxy.getImageRemote(imgClient)
    image = QImage(alImage[6], alImage[0], alImage[1], QImage.Format_RGB888)
    img = convertimage(image)

    img = cv2.imread("C:\\Users\\jantk_000\\Downloads\\IMG_20150422_111942_1.jpg")

    # cv2.imshow("Test", img)

    output = ext.extract(img)

    i = 0
    pieces = []
    for out in output:
        pieces.append(pcl.Piece(out, i))
        i += 1

    puzzle = pzl.Puzzle(pieces, img, 2, 3)
    slv.solve(puzzle)

    cv2.imshow("Result", puzzle.sol)
    cv2.waitKey(100000)



