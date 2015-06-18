import math

p = float(3) / 10
q = float(1) / 16
# q devided by p
qp = float(5) / 24


def dissimilarity(avec, bvec):
    comp = 0
    for x in range(0, avec.shape[0]):
        for y in range(0, avec.shape[1]):
            distance = math.fabs(int(avec[x][y]) - int(bvec[x][y]))
            comp += math.pow(distance, p)
    return math.pow(comp, qp)
