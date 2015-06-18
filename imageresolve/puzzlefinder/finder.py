import argparse
import cv2
import os.path
import numpy


def main():
    args = parse_args()
    print args.videofile
    if not os.path.exists(args.videofile):
        print "Video does not exist"
        return

    frame = cv2.imread(args.videofile)
    cv2.imshow("Original", frame)

    edgesorig = cv2.Canny(frame, 100, 200)
    cv2.imshow("Edges orig", edgesorig)

    # for rho, theta in lines[0]:
    #    a = numpy.cos(theta)
    #    b = numpy.sin(theta)
    #    x0 = a*rho
    #    y0 = b*rho
    #    x1 = int(x0 + 1000*(-b))
    #    y1 = int(y0 + 1000*a)
    #    x2 = int(x0 - 1000*(-b))
    #    y2 = int(y0 - 1000*a)

    #    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # cv2.imshow("Original lines", frame)

    # filtered = filter_box(frame, numpy.array([30, 10, 10], numpy.uint8), numpy.array([70, 255, 255], numpy.uint8))
    # cv2.imshow("Filtered", filtered)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def filter_box(image, mincolor, maxcolor):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv_img, mincolor, maxcolor)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("videofile")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()