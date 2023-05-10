import itertools

class Point(object):
    newid = 0

    def __init__(self, x, y, z):
        self.id = Point.newid
        Point.newid += 1

        self.x = x
        self.y = y
        self.z = z
        self.conflics = set()

    def __str__(self):
        return f"Point ({self.x},{self.y},{self.z})"

    def __repr__(self):
        return f"Point ({self.x},{self.y},{self.z})"

