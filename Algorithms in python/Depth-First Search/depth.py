import sys
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
#depth first starts at the begining and then explores a branh before backtracking


class Graph:

    numberVertices = 0

    #constructor
    def __init__(self):
        self.graph = defaultdict(list)

    def addEdge(self, u, v):
        self.graph[u].append(v)


    def DFSUtil(self, v, visited):

        visited[v] = True

        ##mark the current node and print it
        print(v, end = ' ')

        #recure for all vertices
        #and print them

        for i in self.graph[v]:
            print('checking Node' + str(i))
            if visited[i] == False:
                self.DFSUtil(i,visited)

    
    def DFS(self,v):

        #mark all of the vertices as not visted
        #initalizing array of booleans
        print('number of nodes' + str(max(self.graph)+1))
        visited = [False]*(max(self.graph)+1)


        #call to recursive
        self.DFSUtil(v,visited)



#Here is the driver code

##created from our own object

g = Graph()
g.addEdge(2,0)
g.addEdge(2,3)
g.addEdge(0,1)
g.addEdge(0,5)
g.addEdge(1,4) 
##added backwards edges
g.addEdge(0,2)
g.addEdge(3,2)
g.addEdge(1,0)
g.addEdge(5,0)
g.addEdge(4,1) 
         


print("Following is DFS from (starting from vertex 2)") 
g.DFS(2) 










'''
#Graphing stuff at the end
graph = {(1,2),(1,7),(1,8),(2,3),(2,6),(3,4),(3,5),(8,9),(8,12),(9,10),(9,11)}

G = nx.Graph()

G.add_edges_from(graph)

pos = nx.spring_layout(G)  # positions for all node
nx.draw_networkx_nodes(G,pos,node_size = 700)
nx.draw_networkx_labels(G,pos, font_size=20, font_family='sans-serif')
nx.draw_networkx_edges(G, pos, width=6)


plt.show()
'''
