from math import comb
import attr

import numpy as np

from utils.nodes import Node


def split_xy(input_array):
    x, y = [], []
    for coords in input_array:
        x.append(coords[0])
        y.append(coords[1])
    return x, y


@attr.s(auto_attribs=True)
class Edge:
    """
    The type can vary between straight, and curved
    """
    start: Node
    end: Node
    _length: float = 0

    def get_length(self):
        if self._length:
            return self._length
        else:
            self._length = np.sqrt(np.power(self.end.x - self.start.x, 2) + np.power(self.end.y - self.start.y, 2))
        return self._length

    def plot_coords(self, precision=1):
        return [self.end.x, self.start.x], [self.end.y, self.start.y]


# noinspection PyDataclass
@attr.s(auto_attribs=True)
class CurvedEdge(Edge):
    control_points: list
    _length: float = 0
    last_precision: int = 100
    points: list = []

    def generate_points(self, precision=100):
        self.points = []
        self.last_precision = precision

        in_points = [self.start.node_tuple]
        in_points.extend(self.control_points)
        in_points.append(self.end.node_tuple)

        n = len(in_points) - 1

        for t in np.arange(0, 1, 1 / precision):
            rt = 0  # Keep a running total for the sum function
            for i, pt in enumerate(in_points):
                P = np.array(pt)
                rt += (comb(n, i) * np.power(1 - t, n - i) * np.power(t, i) * P)
            self.points.append(rt)

    def generate_length(self):
        last_point = self.points[0]
        for point in self.points:
            self._length += np.sqrt(np.power(point[0] - last_point[0], 2) + np.power(point[1] - last_point[1], 2))
            last_point = point

    def get_length(self, precision=100):
        if self._length:
            return self._length
        if len(self.points) == 0:
            self.generate_points(precision)

        self.generate_length()
        return self._length

    def plot_coords(self, precision=100):
        self.generate_points(precision)
        return split_xy(self.points)
