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
    #10.10.48.252
    IP = "10.10.48.252"
    PORT = 9559
    CameraID = 1

    # Read IP address from first argument if any.
    if len(sys.argv) > 1:
        IP = sys.argv[1]

    # Read CameraID from second argument if any.
    if len(sys.argv) > 2:
        CameraID = int(sys.argv[2])

    videoProxy = ALProxy("ALVideoDevice", IP, PORT)
    tts = ALProxy("ALTextToSpeech", IP, PORT)
    posture = ALProxy("ALRobotPosture", IP, PORT)

    posture.goToPosture("Crouch", 1.0)

    tts.setLanguage("English")
    
    resolution = vision_definitions.k4VGA  # 320 * 240
    colorSpace = vision_definitions.kRGBColorSpace
    imgClient = videoProxy.subscribe("_client", resolution, colorSpace, 5)
    # Select camera.
    videoProxy.setParam(vision_definitions.kCameraSelectID, CameraID)

    alImage = videoProxy.getImageRemote(imgClient)
    videoProxy.unsubscribe(imgClient)

    if alImage == None:        
        tts.say("I cannot see anything! Am I blind?")
        print "Cannot retreive image from NAO"
    else:
        tts.say("OK, let me see this puzzle")
        nparr = np.fromstring(alImage[6], np.uint8).reshape(alImage[1], alImage[0], alImage[2])
        img = cv2.cvtColor(nparr, cv2.COLOR_BGR2RGB)
    
        cv2.imwrite("Test.jpg", img)
        
        output = ext.extract(img)
        
        i = 0
        pieces = []
        for out in output:
            pieces.append(pcl.Piece(out, i))
            i += 1
        if len(pieces) == 0:
            tts.say("Oh intresting, but I cannot see any puzzle piece")
        else:
            tts.say("I have found {0} puzzles".format(len(pieces)))
            if len(pieces) == 6:
                tts.say("OK, I will try to solve it")
                puzzle = pzl.Puzzle(pieces, img, 1, 2)
                sol = slv.solve(puzzle)
                print sol
                cv2.imwrite("Result.jpg", puzzle.getvideoimage2(sol))
                cv2.imwrite("Result2.jpg", puzzle.getvideoimage())
                tts.say("Puzzle solved!")
            else:                
                tts.say("Sorry, I cannot solve this puzzle")

    #posture.goToPosture("Sit", 1.0)
