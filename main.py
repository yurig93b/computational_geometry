import numpy as np

from dcel import Dcel
from point import Point


def ch(points, point_len):
    dcel = Dcel(points, [])
    dcel.simplex(points[0], points[1], points[2], points[3])

    for i in range(4, point_len):
        if len(points[i].conflics) == 0:
            continue
        else:
            h = dcel.find_he(points[i])
            if h != None:
                dcel.assign_new_facets(h, points[i])
                dcel.delete_faces(points[i])

    ans = dcel.get_results()
    for i in ans:
        print(i[0], i[1], i[2])


def parse_file(filename):
    with open(filename, 'r') as f:
        l = f.readlines()

        point_len = -1
        points = []

        for line in l:
            if point_len == -1:
                point_len = int(line)
            else:
                data = [int(i) for i in line.strip().split(" ")]
                p = Point(data[0], data[1], data[2])
                points.append(p)

        return points, point_len


def main():
    points, point_len = parse_file("sampleinput.txt")
    np.random.shuffle(points)
    ch(points, point_len)


if __name__ == '__main__':
    main()

