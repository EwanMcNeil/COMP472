from collections import defaultdict

##graph using adacency list rep

class Graph:

    def __init__(self):
        

        #default dictonaily to store the graph
        self.graph = defaultdict(list)

    def addEdge(self,u,v):
        self.graph[u].append(v)


    #function to make a breadth first seach of the graph

    def BFS(self,s):

        #mark all the vertices not visited
        visited = [False] * (len(self.graph)) 

        queue = []
        #mark the source node as visted and enqueue it

        queue.append(s)
        visited[s]= True

        while queue:

            #dequeue a vertex from the queue and print it
            s = queue.pop(0)
            print(s, end = " ")

            #get all adjacent vertives of the dequeued vertex s
            #if adjacent has not been vistited then mark it and enqueue it

            #goes through all the nodes connected to it
            for i in self.graph[s]:
                if visited[i] == False: 
                    queue.append(i)
                    visited[i] = True



##this is the driver code for the algo
g = Graph() 
g.addEdge(0, 1) 
g.addEdge(0, 2) 
g.addEdge(1, 2) 
g.addEdge(2, 0) 
g.addEdge(2, 3) 
g.addEdge(3, 3) 
  
print ("Following is Breadth First Traversal"
                  " (starting from vertex 2)") 
g.BFS(2) 