def get_sides(a, b, sidea, sideb):
    avec = a.get_side(sidea)
    bvec = b.get_side(sideb)

    # Side A is left
    if sidea == 0:
        if sideb == 0:
            return avec, reverse(bvec)

    return 0


def reverse(vector):
    pass