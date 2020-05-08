#working off example on https://stackabuse.com/basic-ai-concepts-a-search-algorithm/


from collections import deque

class Graph:

    def __init__(self,adjacency_list):
        self.adjacency_list = adjacency_list

    def get_neighbors(self, v):
        return self.adjacency_list[v]


    
     # heuristic function with equal values for all nodes
     # which isnt really calculating anything?
    def h(self, n):
        H = {
            'A': 1,
            'B': 1,
            'C': 1,
            'D': 1
        }

        return H[n]

    
    def a_star_algo(self,start_node,stop_node):
        #open_list is a list of nodes that have been visited
        #but neighbors not
        #closes list is a list of nodes which have been vistied 
        #and whos neighbords have been inspected


        open_list = set([start_node])
        closed_list = set()


        #g contains currwnt distances from start node to all other nodes
        #defualt value if its not found in the map is inf
        #curly braces define a dict
        g = {}

        g[start_node] = 0

        #parents contain an adjacency map of all nodes

        parents = {}
        parents[start_node] = start_node

        while len(open_list) > 0:
            n = None

            #find the node with the lowest value of f() the evaulation fuction
            #always sets the first to v thats why the first part is 
            #and the finds the next best move
            for v in open_list:
                if n == None or g [v] + self.h(v) < g[n] + self.h(n):
                    n = v




            ## these are the checks to see if its either not possible
            ## or if algo is done
            if n == None:
                print('Path does not exist!')
                return None
            #if the current node is the ending node
            # then you take the right path
            if n ==stop_node:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]
                
                reconst_path.append(start_node)

                reconst_path.reverse()
                print('Path found: {}'.format(reconst_path))
                return reconst_path



        
            #now we have the current node with the lowest value of f()
             #have to add in the current neighbors

            for(m, weight) in self.get_neighbors(n):
            #if the current node isnt in open list and closes
            # we have to add it to the open list and not n as its parent
            #weight stacks it seems
                 if m not in open_list and m not in closed_list:
                     open_list.add(m)
                     parents[m] = n
                     g[m] = g[n] + weight

            
                     #see if its wuicik to first visit n them m
                 else:
                     if g[m] > g[n] + weight:
                      g[m] = g[n] + weight
                      parents[m] = n

                     if m in closed_list:
                        closed_list.remove(m)
                        open_list.add(m)



             #g(n) is the cost of the path from the start node to n, and h(n) is a heuristic function that estimates the cost of the cheapest path from n to the goal.
             #now you remove n from the open list and add it to the closes
             #beacuse all the neighbors were inspected and the g() calculated
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None


##driver code


#the "weight" here is equal to the 
adjacency_list = {
    'A': [('B', 1), ('C', 3), ('D', 7)],
    'B': [('D', 5)],
    'C': [('D', 12)]
}
graph1 = Graph(adjacency_list)
graph1.a_star_algo('A', 'D')
        