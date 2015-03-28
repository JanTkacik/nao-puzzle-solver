import cv2
import collections
import argparse
import os


def main():
    args = parse_args()
    orig = cv2.imread(args.image)
    # cv2.imshow("Original image", orig)

    cropped = crop_orig(orig, args.rectanglesize)
    # cv2.imshow("Cropped image", cropped.image)

    # rect = get_rectangle(cropped.image, args.rectanglesize, 0, 0)
    # cv2.imshow("Rectangle 0,0", rect)

    directory = os.path.dirname(args.image)

    for x in range(0, cropped.x):
        for y in range(0, cropped.y):
            rect = get_rectangle(cropped.image, args.rectanglesize, x, y)
            # cv2.imshow("Rect_{}_{}".format(x, y), rect)
            path = os.path.join(directory, "{0}_{1}_{2}.png".format(args.rectanglesize, x, y))
            cv2.imwrite(path, rect)

    cv2.waitKey(0)
    pass


def get_rectangle(image, rectanglesize, x, y):
    ystart = y*rectanglesize
    xstart = x*rectanglesize
    return image[ystart:ystart+rectanglesize, xstart:xstart+rectanglesize]


def crop_orig(image, rectanglesize):
    xblocks = image.shape[1] / rectanglesize
    yblocks = image.shape[0] / rectanglesize
    imagewidth = xblocks * rectanglesize
    imageheight = yblocks * rectanglesize

    cropped = collections.namedtuple("Cropped", ["image", "x", "y"])
    return cropped(image[0:imageheight, 0:imagewidth], xblocks, yblocks)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    parser.add_argument("-x", "--rectanglesize", type=int, help="Rectangle size")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()


