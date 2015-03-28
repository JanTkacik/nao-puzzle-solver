# Compatibility will be in format compatibilityType dictionary of l,r,u,d - l,r,u,d


class Compatibility:
    def __init__(self, piecea, pieceb):
        self.a = piecea
        self.b = pieceb
        self.comp = {}
