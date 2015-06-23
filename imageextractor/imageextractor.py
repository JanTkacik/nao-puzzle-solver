import cv2
import numpy as np

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1)*np.dot(d2, d2)))

def trasnformCropToRectangle(img,pts,sz):

    sorted_pts = sorted(pts, key = lambda x: (x[0], x[1]))
    if sorted_pts[0][1]> sorted_pts[1][1]: #[x0 > x1]
        leftUp=sorted_pts[1]
        rightUp=sorted_pts[0]
    else:
        leftUp=sorted_pts[0]
        rightUp=sorted_pts[1]

    if sorted_pts[2][1]> sorted_pts[3][1]: #[x0 > x1]
        leftDown=sorted_pts[3]
        rightDown=sorted_pts[2]
    else:
        leftDown=sorted_pts[2]
        rightDown=sorted_pts[3]

    pts1 = np.float32([leftDown,leftUp,rightDown,rightUp])
    pts2 = np.float32([[0,0],[sz,0],[0,sz],[sz,sz]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img,M,(sz,sz))
    return dst




def find_squares(img):
    #img = cv2.GaussianBlur(img, (3, 3), 0)
    # cv2.imshow("Blurred", img)
    squares = []
    for gray in cv2.split(img):
        for thrs in xrange(0, 1, 10):
            if thrs == 0:
                binn = cv2.Canny(gray, 100, 200)
                binn = cv2.dilate(binn, None)
                #cv2.imshow("Canny", binn)
            else:
                retval, binn = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
                # cv2.imshow("Test {}".format(thrs), binn)
            contours, hierarchy = cv2.findContours(binn, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            #x = cv2.findContours(binn, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos(cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4]) for i in xrange(4)])
                    if max_cos < 0.30:
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


# is clr in HSV in range?
def inRange(clr, low, high):
    if(clr[0]>=low[0] and clr[1]>=low[1] and clr[2]>=low[2]
       and clr[0]<=high[0] and clr[1]<=high[1] and clr[2]<=high[2]):
        return True
    return False


def filterGreenEdges(img,low,high,thresh=0,shift=5):
    imax = img.shape[0]
    jmax = img.shape[1]
    icenter=imax//2
    jcenter=jmax//2
    for i in xrange(imax//2+1-thresh):
        for iabs in (-1,1):
            jact=0
            if (icenter + i*iabs >= 0 and icenter + i*iabs < imax):
                while jact < jmax and inRange(img[icenter + i*iabs][jact] ,low,high):
                    jact = jact + 1
                jact = jact+shift #posun okraju o shift
                if(jact >=jmax):
                    for j in xrange(jmax):
                        img[icenter+i*iabs][j] = img[icenter+(i-1)*iabs][0] # o jedna vzadu
                else:
                    for j in xrange(jact):
                        img[icenter+i*iabs][j] = img[icenter+i*iabs][jact] # prepagacia do strany
            jact=jmax-1
            if (icenter + i*iabs >= 0 and icenter + i*iabs < imax):
                while jact >= 0 and inRange(img[icenter + i*iabs][jact] ,low,high):
                    jact = jact -1
                jact = jact-shift #posun okraju o shift
                if(jact >=0): # empty row was handled with jact = 0 branch
                    j = jact+1
                    while(j <jmax):
                        img[icenter+i*iabs][j] = img[icenter+i*iabs][jact] # prepagacia do strany
                        j=j+1

    for j in xrange(jmax//2+1-thresh):
        for jabs in (-1,1):
            iact=0
            if (jcenter + j*jabs >= 0 and jcenter + j*jabs < jmax):
                while iact < imax and inRange(img[iact][jcenter + j*jabs] ,low,high):
                    iact = iact + 1
                iact = iact+shift #posun okraju o shift
                if(iact >=imax):
                    for i in xrange(imax):
                        img[i][jcenter+j*jabs] = img[0][jcenter+(j-1)*jabs] # o jedna vzadu
                else:
                    for i in xrange(iact):
                        img[i][jcenter+j*jabs] = img[iact][jcenter+j*jabs] # prepagacia hore
            iact=imax-1
            if (jcenter + j*jabs >= 0 and jcenter + j*iabs < jmax):
                while iact >= 0 and inRange(img[iact][jcenter + j*jabs] ,low,high):
                    iact = iact -1
                iact = iact-shift #posun okraju o shift
                if(iact >=0): # empty row was handled with jact = 0 branch
                    i = iact+1
                    while(i <imax):
                        img[i][jcenter+j*jabs] = img[iact][jcenter+j*jabs] # prepagacia hore
                        i=i+1


    for x in (((0,thresh),(0,thresh),img[thresh][thresh]),
              ((imax-thresh-1,imax),(0,thresh),img[imax-thresh-2][thresh]),
              ((0,thresh),(jmax-thresh-1,jmax),img[thresh][jmax-thresh-2]),
              ((imax-thresh-1,imax),(jmax-thresh-1,jmax),img[imax-thresh-2][jmax-thresh-2])):
        for i in xrange(x[0][0],x[0][1]):
            for j in xrange(x[1][0],x[1][1]):
                if (inRange(img[i][j],low,high)):
                    img[i][j]=x[2]
    return img


def centerWihtinSquare (s,center,thrash = 4):
    sc =[(s[0][0]+s[1][0]+s[2][0]+s[3][0])//4, (s[0][1]+s[1][1]+s[2][1]+s[3][1])//4]
    return  abs(sc[0]-center[0]) < thrash and abs(sc[1]-center[1]) < thrash


def findOneSquarePerPuzzle( squares ):
    puzzlesquares = []
    for s in squares:
        center =[(s[0][0]+s[1][0]+s[2][0]+s[3][0])//4, (s[0][1]+s[1][1]+s[2][1]+s[3][1])//4]
        intersect = [i for i in puzzlesquares if centerWihtinSquare(i,center)]
        if not intersect :
            puzzlesquares.append(s)
    return puzzlesquares


def filterSquaresBySize(squares, thresh = 0.3):
    if len(squares) == 0:
        return []
    sizes=[]
    for s in squares:
        center =[(s[0][0]+s[1][0]+s[2][0]+s[3][0])//4, (s[0][1]+s[1][1]+s[2][1]+s[3][1])//4]
        act=0
        for i in xrange(4):
            act=act + abs(center[0]-s[i][0]) + abs(center[1]-s[i][1])
        act=act//4
        sizes.append(act)
    sizes.sort()
    if len(sizes) > 0:
        median = sizes[((len(sizes) + 1)//2) - 1]
    else:
        return []
    filtered_squares=[]

    i=0
    for s in sizes:
        if ((median * (1-thresh)) <= s <= (median * (1+thresh))):
            filtered_squares.append(squares[i])
        i=i+1
    return filtered_squares


def extract(image):
    # args = parse_args()
    # print args.videofile
    # if not os.path.exists(args.videofile):
    #     print "Video does not exist"
    #     return
    #
    # image = cv2.imread(args.videofile)
    # cv2.imshow("Original", image)

    filtered = filter_box(image, np.array([50, 40, 40], np.uint8), np.array([75, 255, 255], np.uint8))
    cv2.imwrite("Filtered.jpg", filtered)

    squares_found = find_squares(filtered)
    print "Found {0} puzzles".format(len(squares_found))
    squares_found = filterSquaresBySize(squares_found)
    print "After size filtering {0} puzzles".format(len(squares_found))
    squares_found = findOneSquarePerPuzzle(squares_found)
    print "After center filtering {0} puzzles".format(len(squares_found))


    index = 0
    outputSize = 100
    output = []
    for sqr in squares_found:
        dst = trasnformCropToRectangle(image,sqr,outputSize)
        index = index+1

        #cv2.imwrite('/home/martas/Video/output/{0}_{1}a.jpg'.format(outputSize,index),dst)

        hsv_dst = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
        hsv_dst = filterGreenEdges(hsv_dst,np.array([40, 40, 40], np.uint8),np.array([70, 255, 255], np.uint8))
        bgr_dst = cv2.cvtColor(hsv_dst, cv2.COLOR_HSV2BGR)
        #bgr_dst = cv2.medianBlur(bgr_dst,11)

        # cv2.imshow('dst {0}'.format(index),dst)
        cv2.imwrite('{0}_{1}b.jpg'.format(outputSize,index),bgr_dst)
        output.append(bgr_dst)
    # print squares_found
    cv2.drawContours(image, squares_found, -1, (0, 255, 0), 3)
    cv2.imwrite('Squares.jpg', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return output
