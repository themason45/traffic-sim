import numpy as np
import matplotlib.pyplot as plt

from utils.graph import Graph
from searcher import Searcher


def splitxy(input_array):
    x, y = [], []
    for coords in input_array:
        x.append(coords[0])
        y.append(coords[1])
    return x, y


nodes = np.array([(1.64, 6.81),
                  (4.1, 5.77),
                  (2.7, 4.89),
                  (3.54, 3.01),
                  (1.54, 0.95),
                  (4.34, 1.85),
                  (7.4, 1.83),
                  (6.26, 0.27),
                  (7.54, 4.23),
                  (6.64, 6.09),
                  (9.68, 7.69),
                  (13.24, 4.29),
                  (11.46, 3.19),
                  (12.5, 2),
                  (9.58, 1.17),
                  (14.68, 1.49)
                  ])

adjacencies = np.array([
    [0, [1]],
    [1, [0, 2, 9]],
    [2, [1, 3]],
    [3, [2, 4, 5, 8]],
    [4, [3]],
    [5, [3, 6]],
    [6, [5, 7]],
    [7, [6]],
    [8, [3, 9, 11]],
    [9, [8, 10]],
    [10, [9]],
    [11, [8, 12]],
    [12, [11, 13]],
    [13, [12, 14, 15]],
    [14, [13]],
    [15, [13]]
], dtype=object)

nCount = len(nodes)
adjacency_matrix = np.zeros((nCount, nCount))

if __name__ == '__main__':
    for relation in adjacencies:
        start_point = nodes[relation[0]]
        for endpointIdx in relation[1]:
            endpoint = nodes[endpointIdx]

            dist = np.sqrt(np.power(endpoint[0] - start_point[0], 2) + np.power(endpoint[1] - start_point[1], 2))
            adjacency_matrix[relation[0], endpointIdx] = dist

            plt.plot([endpoint[0], start_point[0]], [endpoint[1], start_point[1]], 'ro-')

    for i in range(nCount):
        plt.annotate(i, (nodes[i][0], nodes[i][1]))

    searcher = Searcher(mat=adjacency_matrix)
    start_node_idx = 0

    routes = searcher.generate_tree(start_node_idx)

    start_point = nodes[start_node_idx]
    for idx in routes[8]["path"] + searcher.generate_tree(8)[2]["path"] + searcher.generate_tree(2)[11]["path"]:
        end_point = nodes[idx]
        plt.arrow(start_point[0], start_point[1], end_point[0] - start_point[0], end_point[1] - start_point[1],
                  head_width=0.5, head_length=0.5, color='blue', zorder=3, length_includes_head=True)
        start_point = end_point

    plt.plot(*splitxy(nodes), 'ro', label="hi")

    graph = Graph()
    for node in nodes:
        graph.add_node(node[0], node[1])

    print(graph.adjacency_list)
    print(graph.matrix)
    # plt.show()
