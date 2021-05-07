from dataclasses import dataclass


@dataclass
class Node:
    x: int
    y: int

    def dist(self, other):
        pass

    @property
    def node_tuple(self):
        return self.x, self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y