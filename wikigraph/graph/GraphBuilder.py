from queue import Queue

from wikigraph.graph.Graph import Graph
from wikigraph.wikipedia.Article import Article


class GraphBuilder:
    def __init__(self, maximum_node_count, maximum_depth, maximum_references=None, exclude=None):
        """
        :param maximum_node_count: maximum node count in graph
        :param maximum_depth: maximum depth in graph
        :param maximum_references: maximum references extracted per article
        :param exclude: either a list of article identifiers to skip or a
                        callback function which accepts the article object as
                        a parameter and returns True if it should be skipped
        """
        self.maximum_node_count = maximum_node_count
        self.maximum_depth = maximum_depth
        self.maximum_references = maximum_references

        self.__node_cache = None
        self.__node_count = None
        self.__bfs_queue = None
        self.reset()

        if callable(exclude):
            self.exclude = exclude
        elif isinstance(exclude, list):
            self.exclude = lambda a: a.identifier in exclude
        else:
            self.exclude = lambda a: a.identifier == exclude

    def reset(self):
        """
        reset some properties which are modified when building a graph
        :return:
        """
        self.__node_cache = {}
        self.__node_count = 0
        self.__bfs_queue = Queue()

    def __enter__(self):
        self.reset()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.reset()

    def build_from(self, article: Article):
        """
        create a graph recursively starting with the specified article

        :param article: article to start with
        :return:
        """
        # create the initial graph node
        graph = self.__create(article, 0)

        # parse further articles until the breadth first search list is empty
        # or the maximum node count is reached
        while not self.__bfs_queue.empty() and self.__node_count < self.maximum_node_count:
            # get next article from list
            bfse = self.__bfs_queue.get()
            origin_node, depth, article = bfse['origin'], bfse['depth'], bfse['article']

            # skip article if it is contained in exclude list
            if self.exclude(article):
                continue

            # create node from it
            node = self.__create(article, depth)

            # add edge from origin to the created node
            origin_node.add_edge_to(node)

        # return the initial graph node so it can be used outside the
        # GraphBuilder class
        return graph

    def __create(self, article: Article, depth):
        # If article has been pushed to the node cache by another call
        # we do not need to execute the creation and parsing again.
        if article.identifier in self.__node_cache:
            return self.__node_cache[article.identifier]

        # create a new node and push it to node cache
        node = Graph(article)

        self.__node_cache[article.identifier] = node
        self.__node_count += 1

        # extract linked articles
        articles = article.linked_articles()
        if self.maximum_references is not None:
            articles = articles[:self.maximum_references]

        for artcl in articles:
            # Create an entry in the breadth first search list so it is
            # explored in a future step. The edge will be added after the
            # entry is parsed itself in the build_from method.
            # Also ensure the maximum depth limit is not exceeded.
            if depth < self.maximum_depth:
                self.__bfs_queue.put({
                    'origin': node,
                    'depth': depth + 1,
                    'article': artcl
                })

        # return node so it can be used outside this method
        # this is needed to add more edges or use the initial node outside of
        # the GraphBuilder class
        return node
