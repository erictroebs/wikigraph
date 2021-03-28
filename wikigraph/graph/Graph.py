from functools import reduce

from wikigraph.graph.GraphIterator import GraphIterator


class Graph:
    """
    represents an arbitrary subgraph
    """

    def __init__(self, article):
        """
        :param article: article object to wrap
        """
        self.article = article
        self.edges = []

    def add_edge_to(self, other):
        """
        :param other: subgraph to add an edge to
        :return:
        """
        self.edges.append(other)

    @property
    def degree(self):
        return len(self.edges)

    def __iter__(self):
        return GraphIterator(self)

    def minimum_degree_node(self):
        """
        Find the node with minimum degree in this graph. If there are multiple
        nodes with the same minimum degree the first found in bfs order is
        returned.

        :return:
        """
        return reduce(lambda a, v: v if v.degree < a.degree else a, self, self)

    def maximum_degree_node(self):
        """
        Find the node with maximum degree in this graph. If there are multiple
        nodes with the same maximum degree the first found in bfs order is
        returned.

        :return:
        """
        return reduce(lambda a, v: v if v.degree > a.degree else a, self, self)

    def density(self):
        """
        calculate graph density
        :return:
        """
        # count edges in graph
        node_count = 0
        edge_count = 0

        for node in self:
            node_count += 1
            edge_count += node.degree

        # calculate density for a directed graph
        if node_count == 1:
            return 0
        else:
            return edge_count / ((node_count - 1) * node_count)

    def labels(self):
        """
        get a list of labels ordered as the nodes appear in bfs search

        :return: list of labels
        """
        # map graph nodes to their corresponding article's unescaped
        # identifiers
        return list(map(lambda x: x.article.unescaped_identifier, self))

    def adjacency(self):
        """
        get a two dimensional matrix containing the directed edges ordered as
        the nodes appear in bfs search

        :return: two dimensional adjacency matrix
        """
        # get list of graph nodes
        nodes = list(self)
        size = len(nodes)

        # create empty two dimensional list
        result = [[0 for _ in range(size)] for _ in range(size)]

        # set elements representing edges to 1
        # TODO This can probably be solved faster than in O(n^2).
        # iterate over matrix rows
        for row in range(size):
            row_artcl = nodes[row]

            # iterate over neighbours
            for col_artcl in row_artcl.edges:
                # find index corresponding to col_artcl
                col = nodes.index(col_artcl)

                # set entry in matrix to 1
                result[row][col] = 1

        return result
