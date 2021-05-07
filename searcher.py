import numpy as np


class Searcher:
    mat: np.ndarray  # type: np.ndarray
    shape: tuple
    out: list
    V: int

    def __init__(self, mat: np.ndarray):
        self.mat = mat
        self.shape = mat.shape
        self.V = self.shape[0]

    @staticmethod
    def min_distance(dist, queue) -> int:
        """
        Find the vertex with the lowest distance value out of the vertices that are not
        not in the tree

        :param dist:
        :param queue:
        :return:
        """
        minimum = np.infty
        min_index = -1

        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i]
                min_index = i
        return min_index

    def path_tree(self, src, parent, j):
        # noinspection PyTypeChecker
        self.out[src]["path"].append(j)
        if parent[j] == -1:
            return
        self.path_tree(src, parent, parent[j])

    def generate_tree(self, src):
        """
        Generates a tree using Dijkstra's shortest path algorithm
        Code adapted from: https://www.geeksforgeeks.org/printing-paths-dijkstras-shortest-path-algorithm/?ref=lbp

        :param src:
        :return:
        """
        self.out = [{"dist": -1, "path": []} for _ in range(self.V)]
        graph = self.mat

        row = len(graph)
        col = len(graph[0])

        dist = [np.infty] * row
        parent = [-1] * row

        dist[src] = 0
        queue = []
        for i in range(row):
            queue.append(i)

        while queue:
            u = self.min_distance(dist, queue)
            queue.remove(u)

            for i in range(col):
                if graph[u][i] and i in queue:
                    if dist[u] + graph[u][i] < dist[i]:
                        # Set the distance value, as well as the node's closest parent
                        dist[i] = dist[u] + graph[u][i]
                        parent[i] = u

        del i
        for i in range(len(dist)):
            self.out[i]["dist"] = dist[i]
            self.path_tree(i, parent, i)
            self.out[i]["path"].reverse()

        return self.out
