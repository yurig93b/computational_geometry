from point import Point

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

