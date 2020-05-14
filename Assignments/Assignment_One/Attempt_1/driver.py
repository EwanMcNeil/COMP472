##first attempt at Assignment one 
##Read in crime_dt.sph
## it is a shape fi
import numpy as np
import pandas as pd
import geopandas as gpd
import shapefile
from matplotlib import colors
import numpy as np
from matplotlib import pyplot as plt
from shapely.geometry.polygon import Polygon
from descartes import PolygonPatch
from collections import deque


def crimesWithinBounds(xBot,xTop,yBot,yTop):
    global shapeRecords
    count = 0
    for i in range(len(shapeRecords)):
        x = shapeRecords[i].shape.__geo_interface__["coordinates"][0]
        y = shapeRecords[i].shape.__geo_interface__["coordinates"][1]

        if xBot <= x <= xTop:
           if yBot <= y <= yTop:
                count += 1
    return count


#trying to build the graph to both display the blocks
#but also be the basis for the A*



class Graph:
    def __init__(self,adjacency_list):
        self.adjacency_list = adjacency_list
        print(self.adjacency_list)
    def get_neighbors(self, v):
        return self.adjacency_list[v]



     # heuristic function with equal values for all nodes
     # which isnt really calculating anything?
     # for now just changing to one
    # def h(self, n):
    #     H = {
    #         'A': 1,
    #         'B': 1,
    #         'C': 1,
    #         'D': 1
    #     }

    #     return H[n]
    def h(self):
        return 1

    
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
                if n == None or g [v] + self.h() < g[n] + self.h():
                    n = v

            print("Current Node", v)



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







#size is the multipler so I think as you go along you 
#add a bit each time
def getTable(size):
    table = dict()

    xBot = -73.59
    xTop = -73.59+size
    yBot = 45.49
    yTop = 45.49 +size

    #count gives an index for each box
    #we start at bottom left here
    count = 0
    ## this needs to be a two loop with max bounds


    ##starts at the bottom goes 
    
    while(yTop <= 45.53):
        while(xTop <= -73.55):
         xBot = float('%.3f'%(xBot))
         xTop = float('%.3f'%(xTop))
         yBot = float('%.3f'%(yBot))
         yTop = float('%.3f'%(yTop))
         crime = crimesWithinBounds(xBot,xTop,yBot,yTop)
         info = (crime,xBot, xTop, yBot, yTop)
         table[count] = info
         count += 1
         xBot += size
         xTop += size
         print(info)
        xBot = -73.59
        xTop = -73.59+size
        yBot += size
        yTop += size
    return table


def getMean(table):
    count = 0
    total = 0
    while(count < len(table)):
        tup = table[count]
        total += tup[0]
        count += 1
    mean = total/len(table)
    return mean


def thresholdGraph(blockSize,threshold,table):
    
    global safetyMatrix
    global vertices
    fig = plt.figure(None, dpi=90)
    ax = fig.add_subplot(111)
  
    verticeCount = 0
    count = 0
    xCount = 0
    yCount = 0
    xylength = int(0.039/blockSize)


    while(yCount < xylength):
        while(xCount < xylength):
         tup = table[count]
         crime = tup[0]
         xBot=tup[1]
         xTop=tup[2]
         yBot=tup[3]
         yTop=tup[4]

         coord = (xBot,yBot) 
         vertices[verticeCount] = coord
         verticeCount += 1

         coord = (xTop,yBot) 
         vertices[verticeCount] = coord
         verticeCount += 1

         polygon = Polygon([(xBot, yBot),(xBot,yTop),(xTop,yTop),(xTop,yBot)])
         if(crime < threshold):
             safetyMatrix[xCount,yCount] = 1 
             patch = PolygonPatch(polygon, fc= 'red')
         else:
             patch = PolygonPatch(polygon, fc= 'blue')
         ax.add_patch(patch)
         count += 1
         xCount += 1
         print("x,y,count" ,xCount,yCount,count)
        xCount = 0
        yCount += 1

    safetyMatrix = safetyMatrix.transpose()
    safetyMatrix = np.flip(safetyMatrix, axis=None)
    print(safetyMatrix)
    axes = plt.gca()
    axes.set_xlim([-73.59,-73.55])
    axes.set_ylim([45.49,45.53])
    ax.set_xticks(np.arange(-73.59,-73.55,blockSize));
    ax.set_yticks(np.arange(45.49,45.53,blockSize));
    plt.xticks(rotation=45) 
    plt.show()


def createAdjacency(size,mean):
    global vertices
    graph = dict()

    count = 0

    while(count< len(vertices)): 
        tuple = vertices[count]
        x = tuple[0]
        y = tuple[1]

        #I think you can do this
        graph[count] = []

        point1 = findVertice(x-size,y+size)
        point2 = findVertice(x,y+size)
        point3 = findVertice(x+size,y+size)
        point4 = findVertice(x+size,y)
        point5 = findVertice(x+size,y-size)
        point6 = findVertice(x,y-size)
        point7 = findVertice(x-size,y-size)
        point8 = findVertice(x-size,y)

        #this is me resolving maybe make a better 
        #data structure
        quadrent1Crime =  crimesWithinBounds(x-size,x,y,y+size)
        quadrent2Crime = crimesWithinBounds(x,x+size,y,y+size)
        quadrent3Crime = crimesWithinBounds(x,x+size,y-size,y)
        quadrent4Crime = crimesWithinBounds(x-size,x,y-size,y)

        #true is less (blue)
        #false is more (yellow) 
        oneBool = False
        twoBool = False
        threeBool = False
        fourBool =False

        if(quadrent1Crime < mean):
            oneBool = True
        
        if(quadrent2Crime < mean):
            twoBool = True
        
        if(quadrent3Crime< mean):
            threeBool = True
        
        if(quadrent4Crime< mean):
            fourBool = True
        #finding out the attachments


        #diagonals over blue
        if(oneBool):
            if(point1 != None):
                tuple = (point1,1.5)
                graph[count].append(tuple)

        if(twoBool):
            if(point3 != None):
                tuple = (point3,1.5)
                graph[count].append(tuple)
        
        if(threeBool):
            if(point5 != None):
                tuple = (point5,1.5)
                graph[count].append(tuple)

        if(fourBool):
            if(point7 != None):
                tuple = (point7,1.5)
                graph[count].append(tuple)

        #Straight ones
        if((oneBool) or (twoBool)):
            if(point2 != None):
                if((oneBool) and (twoBool)):
                    tuple = (point2,1.3)
                    graph[count].append(tuple)
                else:
                    tuple = (point2,1)
                    graph[count].append(tuple)
        

        if((twoBool) or (threeBool)):
            if(point4 != None):

                if((twoBool) and  (threeBool)):
                    tuple = (point4,1.3)
                    graph[count].append(tuple)
                else:
                    tuple = (point4,1)
                    graph[count].append(tuple)

        if((threeBool) or (fourBool)):
            if(point6 != None):
                
                if((threeBool) and (fourBool)):
                 tuple = (point6,1.3)
                 graph[count].append(tuple)
                else:
                    tuple = (point6,1)
                    graph[count].append(tuple)

        if((fourBool) or (oneBool)):
            if(point8 != None):
                
                if((oneBool) and  (twoBool)):
                    tuple = (point8,1.3)
                    graph[count].append(tuple)
                else:
                    tuple = (point8,1)
                    graph[count].append(tuple)
        print("COUNT", count)
        print(graph[count])
        count += 1
    print(graph)
    return graph



def findVertice(x, y):
    global vertices
    count = 0
  
    while(count <len(vertices)):
        tuple = vertices[count]
        xSearch = tuple[0]
        ySearch = tuple[1]
        if(x == xSearch) and (y == ySearch):
            return count
        count += 1
    return None



##driver calls
shpPath = 'Shape/crime_dt.shp'
#creating global matrix with size of the grid
shape = shapefile.Reader(shpPath, encoding='ISO-8859-1')
shapeRecords = shape.shapeRecords()
vertices = dict()
blockSize = 0.003

#creating global matrix with size of the grid
xylength = int(0.039/0.003)
safetyMatrix = np.zeros((xylength, xylength))
#safetyMatrix = [[0 for x in range(xylength)] for y in range(xylength)]



table = getTable(blockSize)
mean = getMean(table)
print("the mean is " + str(mean))



#need a global list of vertices
#and an ajacency list
#vertices will be added as a list from the bottom of the blocks
#with the bottom being zero




thresholdGraph(blockSize,mean,table)

adjaencyGraph = createAdjacency(blockSize,mean)


graph1 = Graph(adjaencyGraph)

print(graph1.a_star_algo(3,333))


print(safetyMatrix)
##need to transpose the safetyMatrix


    


    
    






  


