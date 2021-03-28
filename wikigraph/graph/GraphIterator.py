from queue import Queue


class GraphIterator:
    def __init__(self, start):
        # create queue with start element in it
        self.__bfs = Queue()
        self.__bfs.put(start)

        # create set for visited objects
        self.__visited = set()

    def __next__(self):
        while True:
            # stop if there are no elements left in queue
            if self.__bfs.empty():
                raise StopIteration

            # get next element from queue
            next_node = self.__bfs.get()

            # break while loop if the node is not already visited
            if next_node not in self.__visited:
                break

        # add note to visited set
        self.__visited.add(next_node)

        # add all not visited neighbours to bfs queue
        for e in next_node.edges:
            if e not in self.__visited:
                self.__bfs.put(e)

        # return current graph node
        return next_node
