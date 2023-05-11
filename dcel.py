from facet import Facet
from orient import orient, orient_by_facet, ORIENT_COLL
from point import Point


class HEdge:
    def __init__(self, p1, p2, f_white, f_gray):
        self.p1 = p1
        self.p2 = p2
        self.f_white = f_white
        self.f_gray = f_gray


class Dcel:
    def __init__(self, points, facets):
        self.points = points
        self.facets = facets
        self.__f_id = 0
        self.conflicting_pairs_count = 0
        self.center = None

    @property
    def f_id(self):
        r = self.__f_id
        self.__f_id += 1
        return r

    def pyramid(self, p1, p2, p3, p4):
        mid = Point((p1.x + p2.x + p3.x + p4.x) / 4,
                    (p1.y + p2.y + p3.y + p4.y) / 4,
                    (p1.z + p2.z + p3.z + p4.z) / 4)
        self.center = mid

        if orient(p1, p2, p3, mid) == 1:
            self.facets.append(Facet(p1, p2, p3, self.f_id))
        else:
            self.facets.append(Facet(p1, p3, p2, self.f_id))
        if orient(p1, p2, p4, mid) == 1:
            self.facets.append(Facet(p1, p2, p4, self.f_id))
        else:
            self.facets.append(Facet(p1, p4, p2, self.f_id))

        if orient(p1, p3, p4, mid) == 1:
            self.facets.append(Facet(p1, p3, p4, self.f_id))
        else:
            self.facets.append(Facet(p1, p4, p3, self.f_id))
        if orient(p2, p3, p4, mid) == 1:
            self.facets.append(Facet(p2, p3, p4, self.f_id))
        else:
            self.facets.append(Facet(p2, p4, p3, self.f_id))

        self.facets[0].neighbours = [self.facets[3], self.facets[2], self.facets[1]]
        self.facets[1].neighbours = [self.facets[3], self.facets[2], self.facets[0]]
        self.facets[2].neighbours = [self.facets[3], self.facets[1], self.facets[0]]
        self.facets[3].neighbours = [self.facets[2], self.facets[1], self.facets[0]]

        self.validate()

        for i in self.points[4:]:
            for j in self.facets:
                if orient(j.p1, j.p2, j.p3, i) == -1:
                    i.conflics.add(j)
                    j.conflict_points.add(i)
                    self.conflicting_pairs_count += 1

    def find_he(self, p):
        hes = []
        for i in p.conflics:
            if i.is_outer:
                for j in i.neighbours:
                    if orient_by_facet(j, p) == 1:
                        m = self.get_shared_vertices(i, j)
                        if (m[0] == i.p1 and m[1] == i.p2) or (m[0] == i.p2 and m[1] == i.p3) or \
                                (m[0] == i.p3 and m[1] == i.p1):
                            hes.append(HEdge(m[0], m[1], i, j))
                        else:
                            hes.append(HEdge(m[1], m[0], i, j))
                        break
            if len(hes) > 0:
                break

        if len(hes) == 0:
            return None

        starting_point = hes[-1].p1
        initial_point = starting_point
        intrest_point = starting_point
        other_point = hes[-1].p2
        returned_to_start = False
        current_facet = hes[-1].f_white

        while returned_to_start == False:
            if intrest_point != other_point:
                if current_facet.p1 == initial_point:
                    if orient_by_facet(current_facet.neighbours[0], p) == 1:
                        m = self.get_shared_vertices(current_facet, current_facet.neighbours[0])
                        if m[0] == other_point:
                            hes.append(HEdge(m[0], m[1], current_facet, current_facet.neighbours[0]))
                            initial_point = hes[-1].p1
                            other_point = hes[-1].p2
                        elif m[1] == other_point:
                            hes.append(HEdge(m[1], m[0], current_facet, current_facet.neighbours[0]))
                            initial_point = hes[-1].p1
                            other_point = hes[-1].p2
                        if other_point == starting_point:
                            returned_to_start = True
                    else:
                        current_facet = current_facet.neighbours[0]
                        intrest_point = other_point

                elif current_facet.p2 == initial_point:
                    if orient_by_facet(current_facet.neighbours[1], p) == 1:
                        m = self.get_shared_vertices(current_facet, current_facet.neighbours[1])
                        if m[0] == other_point:
                            hes.append(HEdge(m[0], m[1], current_facet, current_facet.neighbours[1]))
                            initial_point = hes[-1].p1
                            other_point = hes[-1].p2
                        elif m[1] == other_point:
                            hes.append(HEdge(m[1], m[0], current_facet, current_facet.neighbours[1]))
                            initial_point = hes[-1].p1
                            other_point = hes[-1].p2
                        if other_point == starting_point:
                            returned_to_start = True
                    else:
                        current_facet = current_facet.neighbours[1]
                        intrest_point = other_point

                else:
                    if orient_by_facet(current_facet.neighbours[2], p) == 1:
                        m = self.get_shared_vertices(current_facet, current_facet.neighbours[2])
                        if m[0] == other_point:
                            hes.append(HEdge(m[0], m[1], current_facet, current_facet.neighbours[2]))
                            initial_point = hes[-1].p1
                            other_point = hes[-1].p2
                        elif m[1] == other_point:
                            hes.append(HEdge(m[1], m[0], current_facet, current_facet.neighbours[2]))
                            initial_point = hes[-1].p1
                            other_point = hes[-1].p2
                        if other_point == starting_point:
                            returned_to_start = True
                    else:
                        current_facet = current_facet.neighbours[2]
                        intrest_point = other_point
            else:
                if current_facet.p1 == intrest_point:
                    if orient_by_facet(current_facet.neighbours[2], p) == 1:
                        m = self.get_shared_vertices(current_facet, current_facet.neighbours[2])
                        if m[0] == other_point:
                            hes.append(HEdge(m[0], m[1], current_facet, current_facet.neighbours[2]))
                            initial_point = hes[-1].p1
                            other_point = hes[-1].p2
                        elif m[1] == other_point:
                            hes.append(HEdge(m[1], m[0], current_facet, current_facet.neighbours[2]))
                            initial_point = hes[-1].p1
                            other_point = hes[-1].p2
                        if other_point == starting_point:
                            returned_to_start = True
                    else:
                        current_facet = current_facet.neighbours[2]
                        intrest_point = other_point


                elif current_facet.p2 == intrest_point:
                    if orient_by_facet(current_facet.neighbours[0], p) == 1:
                        m = self.get_shared_vertices(current_facet, current_facet.neighbours[0])
                        if m[0] == other_point:
                            hes.append(HEdge(m[0], m[1], current_facet, current_facet.neighbours[0]))
                            initial_point = hes[-1].p1
                            other_point = hes[-1].p2
                        elif m[1] == other_point:
                            hes.append(HEdge(m[1], m[0], current_facet, current_facet.neighbours[0]))
                            initial_point = hes[-1].p1
                            other_point = hes[-1].p2
                        if other_point == starting_point:
                            returned_to_start = True
                    else:
                        current_facet = current_facet.neighbours[0]
                        intrest_point = other_point

                elif current_facet.p3 == intrest_point:
                    if orient_by_facet(current_facet.neighbours[1], p) == 1:
                        m = self.get_shared_vertices(current_facet, current_facet.neighbours[1])
                        if m[0] == other_point:
                            hes.append(HEdge(m[0], m[1], current_facet, current_facet.neighbours[1]))
                            initial_point = hes[-1].p1
                            other_point = hes[-1].p2
                        elif m[1] == other_point:
                            hes.append(HEdge(m[1], m[0], current_facet, current_facet.neighbours[1]))
                            initial_point = hes[-1].p1
                            other_point = hes[-1].p2
                        if other_point == starting_point:
                            returned_to_start = True
                    else:
                        current_facet = current_facet.neighbours[1]
                        intrest_point = other_point

        return hes

    def check_if_horizen(self, facet, p):
        o1 = orient_by_facet(facet.neighbours[0], p)
        o2 = orient_by_facet(facet.neighbours[1], p)
        o3 = orient_by_facet(facet.neighbours[2], p)

        if o1 == ORIENT_COLL or o2 == ORIENT_COLL or o3 == ORIENT_COLL:
            print("Points coll.\n")
            return None

        if o1 == -1 and o2 == -1 and o3 == -1:
            return None

        elif o1 == 1 and o2 == -1 and o3 == -1:
            m = self.get_shared_vertices(facet, facet.neighbours[0])
            return [HEdge(m[0], m[1], facet, facet.neighbours[0])]

        elif o1 == -1 and o2 == 1 and o3 == -1:
            m = self.get_shared_vertices(facet, facet.neighbours[1])
            return [HEdge(m[0], m[1], facet, facet.neighbours[1])]

        elif o1 == -1 and o2 == -1 and o3 == 1:
            m = self.get_shared_vertices(facet, facet.neighbours[2])
            return [HEdge(m[0], m[1], facet, facet.neighbours[2])]

        elif o1 == 1 and o2 == 1 and o3 == -1:
            m1 = self.get_shared_vertices(facet, facet.neighbours[0])
            m2 = self.get_shared_vertices(facet, facet.neighbours[1])
            return [HEdge(m1[0], m1[1], facet, facet.neighbours[0]),
                    HEdge(m2[0], m2[1], facet, facet.neighbours[1])]

        elif o1 == -1 and o2 == 1 and o3 == 1:
            m1 = self.get_shared_vertices(facet, facet.neighbours[1])
            m2 = self.get_shared_vertices(facet, facet.neighbours[2])
            return [HEdge(m1[0], m1[1], facet, facet.neighbours[1]),
                    HEdge(m2[0], m2[1], facet, facet.neighbours[2])]

        elif o1 == 1 and o2 == -1 and o3 == 1:
            m1 = self.get_shared_vertices(facet, facet.neighbours[0])
            m2 = self.get_shared_vertices(facet, facet.neighbours[2])
            return [HEdge(m1[0], m1[1], facet, facet.neighbours[0]),
                    HEdge(m2[0], m2[1], facet, facet.neighbours[2])]

        elif o1 == 1 and o2 == 1 and o3 == 1:
            m1 = self.get_shared_vertices(facet, facet.neighbours[0])
            m2 = self.get_shared_vertices(facet, facet.neighbours[1])
            m3 = self.get_shared_vertices(facet, facet.neighbours[2])
            return [HEdge(m1[0], m1[1], facet, facet.neighbours[0]),
                    HEdge(m2[0], m2[1], facet, facet.neighbours[1]),
                    HEdge(m3[0], m3[1], facet, facet.neighbours[2])]

    def assign_new_facets(self, horizon_edges, p):
        new_facets = []
        for i in horizon_edges:
            if orient(i.p1, i.p2, p, self.center) == 1:
                self.facets.append(Facet(i.p1, i.p2, p, self.f_id))
            else:
                self.facets.append(Facet(i.p1, p, i.p2, self.f_id))

            if i.f_gray.neighbours[0] == i.f_white:
                i.f_gray.neighbours[0] = self.facets[-1]
            elif i.f_gray.neighbours[1] == i.f_white:
                i.f_gray.neighbours[1] = self.facets[-1]
            elif i.f_gray.neighbours[2] == i.f_white:
                i.f_gray.neighbours[2] = self.facets[-1]

            if self.facets[-1].p1 != i.p1 and self.facets[-1].p1 != i.p2:
                self.facets[-1].neighbours[0] = i.f_gray

            elif self.facets[-1].p2 != i.p1 and self.facets[-1].p2 != i.p2:
                self.facets[-1].neighbours[1] = i.f_gray

            elif self.facets[-1].p3 != i.p1 and self.facets[-1].p3 != i.p2:
                self.facets[-1].neighbours[2] = i.f_gray

            new_facets.append(self.facets[-1])

            for j in i.f_white.conflict_points:
                if j != p:
                    try:
                        j.conflics.remove(i.f_white)
                    except:
                        pass
                    if orient_by_facet(self.facets[-1], j) == -1:
                        j.conflics.add(self.facets[-1])
                        self.facets[-1].conflict_points.add(j)
                        self.conflicting_pairs_count += 1

            for j in i.f_gray.conflict_points:
                if j != p:
                    try:
                        j.conflics.remove(i.f_white)
                    except:
                        pass
                    if orient_by_facet(self.facets[-1], j) == -1:
                        j.conflics.add(self.facets[-1])
                        self.facets[-1].conflict_points.add(j)
                        self.conflicting_pairs_count += 1

        for i in range(len(new_facets) - 1):
            self.share_edge(new_facets[i], new_facets[i + 1])
        self.share_edge(new_facets[0], new_facets[len(new_facets) - 1])

    def share_edge(self, face1, face2):
        matches = []

        if face1.p1 == face2.p1:
            matches.append((1, 1))
        elif face1.p1 == face2.p2:
            matches.append((1, 2))
        elif face1.p1 == face2.p3:
            matches.append((1, 3))

        if face1.p2 == face2.p1:
            matches.append((2, 1))
        elif face1.p2 == face2.p2:
            matches.append((2, 2))
        elif face1.p2 == face2.p3:
            matches.append((2, 3))

        if face1.p3 == face2.p1:
            matches.append((3, 1))
        elif face1.p3 == face2.p2:
            matches.append((3, 2))
        elif face1.p3 == face2.p3:
            matches.append((3, 3))

        if len(matches) == 2:
            if matches[0][0] != 1 and matches[1][0] != 1:
                face1.neighbours[0] = face2
            elif matches[0][0] != 2 and matches[1][0] != 2:
                face1.neighbours[1] = face2
            elif matches[0][0] != 3 and matches[1][0] != 3:
                face1.neighbours[2] = face2

            if matches[0][1] != 1 and matches[1][1] != 1:
                face2.neighbours[0] = face1
            elif matches[0][1] != 2 and matches[1][1] != 2:
                face2.neighbours[1] = face1
            elif matches[0][1] != 3 and matches[1][1] != 3:
                face2.neighbours[2] = face1

    def get_shared_vertices(self, face1, face2):
        matches = []

        if face1.p1 == face2.p1:
            matches.append(face1.p1)
        elif face1.p1 == face2.p2:
            matches.append(face1.p1)
        elif face1.p1 == face2.p3:
            matches.append(face1.p1)

        if face1.p2 == face2.p1:
            matches.append(face1.p2)
        elif face1.p2 == face2.p2:
            matches.append(face1.p2)
        elif face1.p2 == face2.p3:
            matches.append(face1.p2)

        if face1.p3 == face2.p1:
            matches.append(face1.p3)
        elif face1.p3 == face2.p2:
            matches.append(face1.p3)
        elif face1.p3 == face2.p3:
            matches.append(face1.p3)

        return matches

    def delete_faces(self, p):
        for i in p.conflics:
            i.is_outer = False

    def locate_neighbours(self, facet):
        for i in self.facets:
            if i != facet and i.is_outer == True:
                self.share_edge(facet, i)

    def validate(self):
        for i in self.facets:
            if i.is_outer == True:
                self.locate_neighbours(i)

    def get_results(self):
        ans = []
        for i in self.facets:
            if i.is_outer == True:
                if i.p1.id < i.p2.id and i.p1.id < i.p3.id:
                    ans.append((i.p1.id, i.p2.id, i.p3.id))
                elif i.p2.id < i.p1.id and i.p2.id < i.p3.id:
                    ans.append((i.p2.id, i.p3.id, i.p1.id))
                elif i.p3.id < i.p1.id and i.p3.id < i.p2.id:
                    ans.append((i.p3.id, i.p1.id, i.p2.id))
        sorted_lst = sorted(ans, key=lambda x: (x[0], x[1]))
        return sorted_lst

