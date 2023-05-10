class Facet:
    def __init__(self, p1, p2, p3, id):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.is_outer = True
        self.id = id
        self.conflict_points = set()
        self.neighbours = [None, None, None]


