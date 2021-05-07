import numpy as np
from matplotlib import pyplot as plt

from utils.edges import CurvedEdge
from utils.graph import Graph

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

if __name__ == '__main__':
    graph = Graph()
    for node in nodes:
        graph.add_node(node[0], node[1])

    graph.add_edges(range(0, 16), [
        [1], [0, 2, 9], [1, 3], [2, 4, 5, 8], [3], [3, 6],
        [5, 7], [6], [3, 9, 11], [8, 10], [9], [8, 12], [11, 13], [12, 14, 15], [13], [13]])

    graph.change_edge(0, 1, CurvedEdge(graph.nodes[0], graph.nodes[1], [(3, 7)]))
    graph.change_edge(3, 8, CurvedEdge(graph.nodes[3], graph.nodes[8], [(4, 4), (6, 3)]))
    ax = graph.get_axis(graph.get_route(4, 9)["path"])
    plt.show()

    # OV:
    # NV: 2.7578651335402546
    # ce = CurvedEdge(Node(0, 0), Node(5, 0), [(4, 1), (1, 0)])
    # plt.plot(*ce.plot_coords(), 'r-')
    # plt.show()
    # print(ce.get_length())
