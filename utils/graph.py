from dataclasses import dataclass

import numpy as np
from matplotlib import pyplot as plt

from searcher import Searcher
from utils.edges import Edge
from utils.nodes import Node


def split_xy(input_array):
    x, y = [], []
    for coords in input_array:
        x.append(coords[0])
        y.append(coords[1])
    return x, y


class Graph:
    nodes: list
    edges: dict
    adjacency_list: list
    searcher: Searcher

    def __init__(self):
        self.nodes = []
        self.edges = {}
        self.adjacency_list = []

    @staticmethod
    def hash_nodes(i1, i2):
        return hash((i1, i2))

    def add_node(self, x, y):
        self.nodes.append(Node(x, y))
        self.adjacency_list.append([])

    def remove_node(self, x, y):
        self.nodes.remove(Node(x, y))

    def add_edge(self, i1, i2):
        self.adjacency_list[i1].append(i2)
        self.edges[self.hash_nodes(i1, i2)] = Edge(self.nodes[i1], self.nodes[i2])

    def add_edges(self, from_idx, to_idxes):
        for i1, other_idxs in zip(from_idx, to_idxes):
            for i2 in other_idxs:
                self.add_edge(i1, i2)

    def change_edge(self, i1, i2, new_edge, bi_directional=True):
        self.edges[self.hash_nodes(i1, i2)] = new_edge
        if bi_directional:
            self.edges[self.hash_nodes(i2, i1)] = new_edge

    def remove_edge(self, i1, i2):
        self.adjacency_list[i2].remove(i1)
        self.edges.pop(self.hash_nodes(i1, i2), None)

    @property
    def matrix(self):
        n_count = len(self.nodes)
        adjacency_matrix = np.zeros((n_count, n_count))

        for idx, relations in enumerate(self.adjacency_list):
            for endpointIdx in relations:
                edge = self.edges[self.hash_nodes(idx, endpointIdx)]
                adjacency_matrix[idx, endpointIdx] = edge.get_length()

        return adjacency_matrix

    @property
    def nodes_tuple(self):
        return [n.node_tuple for n in self.nodes]

    def get_route(self, start, *args):
        self.searcher = Searcher(self.matrix)
        routes = {"total_distance": 0, "path": [], "subsections": []}
        for dest in args:
            # Generate tree, and get route to dest
            route = self.searcher.generate_tree(start)[dest]

            routes["subsections"].append(route)
            routes["path"].extend(route["path"])
            routes["total_distance"] += route["dist"]
            start = dest

        return routes

    def get_axis(self, route: list):
        axis = plt.axes()

        axis.plot(*split_xy(self.nodes_tuple), 'ro')

        for idx, node in enumerate(self.nodes):
            axis.annotate(idx, node.node_tuple)

        for edge in self.edges.values():
            axis.plot(*edge.plot_coords(), 'r-')

        if len(route) > 0:
            last_node = route[0]
            for node in route[1:]:
                try:
                    edge = self.edges[self.hash_nodes(last_node, node)]
                    axis.plot(*edge.plot_coords(), 'b-')
                    last_node = node
                except KeyError as _:
                    last_node = node
                    continue

        return axis
