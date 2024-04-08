from deq import Deq
from r2point import R2Point
import math

points = Deq()
line_points = []


class Figure:
    """ Абстрактная фигура """

    @staticmethod
    def set_points(p=None, q=None):
        global line_points
        line_points = []
        if p is None and q is None:
            x1, y1, x2, y2 = map(float,
                                 input('координаты точек концов отрезкаx x1 y1 x2 y2 ->').split())
        else:
            x1, y1, x2, y2 = p.x_y()[0], p.x_y()[1], q.x_y()[0], q.x_y()[1]
        line_points.append(x1)
        line_points.append(y1)
        line_points.append(x2)
        line_points.append(y2)

    @staticmethod
    def edin_okrest(x, y):
        if abs((line_points[3] - line_points[1]) * (x - line_points[0]) - (line_points[2] - line_points[0]) * (
                y - line_points[1])) / math.sqrt(
            (line_points[3] - line_points[1]) ** 2 + (line_points[2] - line_points[0]) ** 2) <= 1:
            return True
        else:
            return False

    def counter(self):
        return self.k

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        self.k = 0
        points.clear()
        points.push_first(p)
        if not self.edin_okrest(p.x_y()[0], p.x_y()[1]):
            self.k += 1
        return Point(p, self.k)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p, k):
        self.k = k
        self.p = p

    def add(self, q):
        if self.p == q:
            return self
        else:
            points.push_first(q)
            if not self.edin_okrest(q.x_y()[0], q.x_y()[1]):
                self.k += 1
        return Segment(self.p, q, self.k)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q, k):
        self.k = k
        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            points.push_first(r)
            if not self.edin_okrest(r.x_y()[0], r.x_y()[1]):
                self.k += 1
            return Polygon(self.p, self.q, r, self.k)
        elif r.is_inside(self.p, self.q):
            return self
        elif self.p.is_inside(r, self.q):
            if not self.edin_okrest(r.x_y()[0], r.x_y()[1]):
                self.k += 1
            if not self.edin_okrest(self.p.x_y()[0], self.p.x_y()[1]):
                self.k -= 1
            return Segment(r, self.q, self.k)
        else:
            if not self.edin_okrest(r.x_y()[0], r.x_y()[1]):
                self.k += 1
            if not self.edin_okrest(self.q.x_y()[0], self.q.x_y()[1]):
                self.k -= 1
            return Segment(self.p, r, self.k)


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c, k):
        self.k = k
        points.clear()
        points.push_first(b)
        if b.is_light(a, c):
            points.push_first(a)
            points.push_last(c)
        else:
            points.push_last(a)
            points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        self.points = points

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(points.size()):
            if t.is_light(points.last(), points.first()):
                break
            points.push_last(points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(points.last(), points.first()):
            if not self.edin_okrest(t.x_y()[0], t.x_y()[1]):
                self.k += 1

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= points.first().dist(points.last())
            self._area += abs(R2Point.area(t,
                                           points.last(),
                                           points.first()))

            # удаление освещённых рёбер из начала дека
            p = points.pop_first()
            while t.is_light(p, points.first()):
                if not self.edin_okrest(p.x_y()[0], p.x_y()[1]):
                    self.k -= 1
                self._perimeter -= p.dist(points.first())
                self._area += abs(R2Point.area(t, p, points.first()))
                p = points.pop_first()
            points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = points.pop_last()
            while t.is_light(points.last(), p):
                if not self.edin_okrest(t.x_y()[0], t.x_y()[1]):
                    self.k -= 1
                self._perimeter -= p.dist(points.last())
                self._area += abs(R2Point.area(t, p, points.last()))
                p = points.pop_last()
            points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(points.first()) + \
                               t.dist(points.last())
            points.push_first(t)
        self.points = points
        return self
