import numpy as np
import cv2
import argparse
import os.path


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1)*np.dot(d2, d2)))


def find_squares(img):
    img = cv2.GaussianBlur(img, (3, 3), 0)
    # cv2.imshow("Blurred", img)
    squares = []
    for gray in cv2.split(img):
        for thrs in xrange(0, 255, 5):
            if thrs == 0:
                binn = cv2.Canny(gray, 100, 200)
                binn = cv2.dilate(binn, None)
                cv2.imshow("Canny", binn)
            else:
                retval, binn = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
                # cv2.imshow("Test {}".format(thrs), binn)
            binn, contours, hierarchy = cv2.findContours(binn, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos(cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4]) for i in xrange(4)])
                    if max_cos < 0.20:
                        squares.append(cnt)
    return squares


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("videofile")
    argss = parser.parse_args()
    return argss


def filter_box(img, mincolor, maxcolor):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return cv2.inRange(hsv_img, mincolor, maxcolor)


def main():
    args = parse_args()
    print args.videofile
    if not os.path.exists(args.videofile):
        print "Video does not exist"
        return

    image = cv2.imread(args.videofile)
    # cv2.imshow("Original", image)

    filtered = filter_box(image, np.array([60, 40, 40], np.uint8), np.array([70, 255, 255], np.uint8))
    # cv2.imshow("Filtered", filtered)

    squares_found = find_squares(filtered)
    print squares_found
    cv2.drawContours(image, squares_found, -1, (0, 255, 0), 3)
    cv2.imshow('Squares', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()