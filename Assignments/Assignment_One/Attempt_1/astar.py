import numpy as np


class Node:

    def __init__(seld,parent =None, position = None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


    def return_path(current_node, maze):
        path = []
        no_rows,no_columns = np.shape(maze)
        #creates initalized result maze with -1 in every position

        result = [[-1 for i in range(no_columns)] for j in range(no_rows)]
        current = current_node

        while current_node is not None:
            path.append(currnt position)
            current = current.parent
        
        path = path[::-1]
        start_value = 0

        for i in range(len(path)):
            result[path[i][0]][path[i][1]] = start_value
            start_value += 1
        return result

    def search(maze,cost,start,end):

        start_node = Node(None, tuple(start))
        start_node.g = 
