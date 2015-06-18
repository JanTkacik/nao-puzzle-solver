import sys
from naoqi import ALProxy

# To get the constants relative to the video.
import vision_definitions
import cv2
import numpy as np
import imageresolve.puzzlesolver.solver as slv
import imageextractor.imageextractor as ext
import imageresolve.puzzlesolver.model.puzzle as pzl
import imageresolve.puzzlesolver.model.piece as pcl

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

    nparr = np.fromstring(alImage[6], np.uint8).reshape(alImage[1], alImage[0], alImage[2])
    img = cv2.cvtColor(nparr, cv2.COLOR_BGR2RGB)

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



