from igraph import Graph, plot


class GraphDrawer:
    """
    This class contains methods specific to drawing so the other graph classes
    can be loaded without further dependencies need to be installed.
    """

    def __init__(self, graph, highlight=None):
        """
        :param graph: Graph object to use as start node
        :param highlight: a node containing one of this keywords is highlighted
        """
        self.graph = graph
        self.highlight = [] if highlight is None else highlight

        self.min_degree = graph.minimum_degree_node().degree
        self.max_degree = graph.maximum_degree_node().degree

    def __vertex_label_colors(self, x):
        # set start node to blue
        if x == self.graph:
            return '#0000ff'

        # set nodes containing keywords to red
        for keyword in self.highlight:
            if keyword in x.article.unescaped_identifier:
                return '#ff0000'

        # default value
        return '#000000'

    def __vertex_label_sizes(self, x):
        # set start node
        if x == self.graph:
            return 22

        '''
        # set nodes containing keywords
        for keyword in self.highlight:
            if keyword in x.article.unescaped_identifier:
                return 16

        # default value
        return 12
        '''

        # set node size depending on degree
        return 10 + 10 * (x.degree - self.min_degree) / (self.max_degree - self.min_degree)

    def save_to(self, file_path, size=(8196, 4096)):
        """
        Save this graph to the specified file. Format is implicitly given by
        file extension and automatically determined by igraph.

        :param file_path: file path
        :param size: image size
        :return:
        """
        # create graph
        g = Graph(directed=True)

        for node in self.graph:
            g.add_vertex(node.article.unescaped_identifier)

        for source in self.graph:
            for target in source.edges:
                g.add_edge(source.article.unescaped_identifier, target.article.unescaped_identifier)

        # create properties
        vertex_labels = list(map(lambda x: x.article.unescaped_identifier, self.graph))
        vertex_label_colors = list(map(self.__vertex_label_colors, self.graph))
        vertex_label_sizes = list(map(self.__vertex_label_sizes, self.graph))

        # plot graph to file
        # format is implicitly given by file extension and automatically
        # determined by igraph
        plot(g, file_path,
             # set image resolution
             bbox=(0, 0, size[0], size[1]),
             # set image margin to allow long labels to be displayed correctly
             margin=128,
             # allow curved edges to reduce intersections
             autocurve=True,
             # choose graph layout
             # layout='large_graph',
             layout='fr',
             niter=2000,
             # set vertex options
             vertex_size=5,
             vertex_color='#ff9999',
             vertex_frame_color='#777777',
             # set edge options
             edge_width=0.5,
             edge_color='#999999',
             edge_arrow_size=0.5,
             # set label options
             vertex_label=vertex_labels,
             vertex_label_color=vertex_label_colors,
             vertex_label_size=vertex_label_sizes)
