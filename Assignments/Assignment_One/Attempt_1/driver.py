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
import math  
import pickle
from copy import copy


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
    def h(self, current,goal):
        global vertices
        currentXYTup = vertices[current]
        goalXYTup = vertices[goal]
        x1 = currentXYTup[0]
        y1 = currentXYTup[1]


        x2 = goalXYTup[0]
        y2 = goalXYTup[1]

        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        return dist
    

    
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
                if n == None or g [v] + self.h(v,stop_node) < g[n] + self.h(n,stop_node):
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
                #print('Path found: {}'.format(reconst_path))
                return reconst_path



        
            #now we have the current node with the lowest value of f()
            #have to add in the current neighbors

            for(m, weight) in self.get_neighbors(n):
            #if the current node isnt in open list and closes
            # we have to add it to the open list and not n as its parent
            #weight stacks it seems
                 if m not in open_list and m not in closed_list:
                     
                    print("if both", m)
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

            
                     #see if its wuicik to first visit n them m
                #  else:
                #      print("else", m)
                #      if g[m] > g[n] + weight:
                #       g[m] = g[n] + weight
                #       parents[m] = n

                #      if m in closed_list:
                #         closed_list.remove(m)
                #         open_list.add(m)



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


def getMean(table, threshold):

    ##create a new organize list 
    crimeList = []
    count = 0
    while(count < len(table)):
        tup = table[count]
        total = tup[0]
        crimeList.append(total)
        count += 1

    index = count*threshold
    index = count - index
    index = int(index)
    crimeList.sort(reverse = True)
    print(crimeList)
    median = crimeList[index] 
    print(median)
    return median
    


def thresholdGraph(blockSize,threshold,table):
    
    global globalPolygons
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


            #adds a vertice into the dict
         coord = (xBot,yBot) 
         vertices[verticeCount] = coord
         verticeCount += 1

        #  coord = (xTop,yBot) 
        #  vertices[verticeCount] = coord
        #  verticeCount += 1

         polygon = Polygon([(xBot, yBot),(xBot,yTop),(xTop,yTop),(xTop,yBot)])
         if(crime < threshold):
             patch = PolygonPatch(polygon, fc= 'red')
         else:
             patch = PolygonPatch(polygon, fc= 'blue')
         new_patch = copy(patch)
         globalPolygons.append(new_patch)
         ax.add_patch(patch)
         count += 1
         xCount += 1
         print("x,y,count" ,xCount,yCount,count)
        xCount = 0
        yCount += 1
    axes = plt.gca()
    axes.set_xlim([-73.59,-73.55])
    axes.set_ylim([45.49,45.53])
    ax.set_xticks(np.arange(-73.59,-73.55,blockSize));
    ax.set_yticks(np.arange(45.49,45.53,blockSize));
    plt.xticks(rotation=45) 
    plt.show()
    return ax


def createAdjacency(size,mean,table,width):
    global vertices
    graph = dict()

    count = 0


    #changing this to exlude the out nodes and calculating just from bottom right perspetive
    while(count< len(table)): 

        #find the bottom right vertice
        tuple = table[count]
        x = tuple[1]
        y = tuple[3]

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
        try:
            quadrent1Crime =  table[count-1][0]
        except KeyError:
            quadrent1Crime = 1000
        
        try:
            quadrent2Crime =  table[count][0]
        except KeyError:
            quadrent2Crime = 1000

        try:
            quadrent3Crime = table[count - width][0]
        except KeyError:
            quadrent3Crime = 1000
        
        try:
            quadrent4Crime = table[count-width-1][0]
        except KeyError:
            quadrent4Crime = 1000
        
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



##used to find the node from the vertice count
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


def estimateNode(x ,y):
    # -73.59 x origin
    # 45.49 y origin
    #just using the global block size varible
    global blockSize
    xDiff = x-(-73.59)
    yDiff = y-(45.49)

    xDiv = xDiff/blockSize
    xDiv = math.floor(xDiv)

    yDiv = yDiff/blockSize
    yDiv = math.floor(xDiv)

    xMult = xDiv*blockSize
    yMult = yDiv*blockSize

    outputX = -73.59 + xMult
    outputY = 45.49 +yMult

    node = findVertice(outputX,outputY)
    return node





##driver calls
shpPath = 'Shape/crime_dt.shp'
#creating global matrix with size of the grid
shape = shapefile.Reader(shpPath, encoding='ISO-8859-1')
shapeRecords = shape.shapeRecords()
vertices = dict()


blockSize = input("enter the size of the blocks (0.003 or 0.002 or 0.001")
blockSize = float(blockSize)

width = 0.04/blockSize
width = int(width)
print(width)



table = getTable(blockSize)

inputThreshold = input("enter the threshold percentage")
inputThreshold = float(inputThreshold)
mean = getMean(table, inputThreshold)
print("the mean is " + str(mean))



#need a global list of vertices
#and an ajacency list
#vertices will be added as a list from the bottom of the blocks
#with the bottom being zero



globalPolygons = []

globalPolygonsCopy = []
colorplotax = thresholdGraph(blockSize,mean,table)



adjaencyGraph = createAdjacency(blockSize,mean,table,width)


graph1 = Graph(adjaencyGraph)

endcheck = 0
while(endcheck == 0):
    globalPolygonsCopy.clear()

    polycount = 0
    while(polycount < len(globalPolygons)):
        new_patch = copy(globalPolygons[polycount])
        globalPolygonsCopy.append(new_patch)
        polycount += 1

    fig = plt.figure(None, dpi=90)
    ax = fig.add_subplot(111)

    polycount = 0
    while(polycount < len(globalPolygons)):
        ax.add_patch(globalPolygonsCopy[polycount])
        polycount += 1

    axes = plt.gca()
    axes.set_xlim([-73.59,-73.55])
    axes.set_ylim([45.49,45.53])
    ax.set_xticks(np.arange(-73.59,-73.55,blockSize));
    ax.set_yticks(np.arange(45.49,45.53,blockSize));
    plt.xticks(rotation=45) 

    startX = input("enter the x Coord of Starting Node")
    startX = float(startX)
    startY = input("enter the y coord of starting Node")
    startY = float(startY)
    startNode = estimateNode(startX,startY)
    startInt = int(startNode)
    endNode = input("enter the end node")
    endInt = int(endNode)
    path = graph1.a_star_algo(startInt,endInt)
    if(path != None):
        print(path)
        x = []
        y = []

        finalloop = 0
        while(finalloop < len(path)):
            tup = vertices[path[finalloop]]
            x.append(tup[0])
            y.append(tup[1])
            finalloop += 1

        print("VERTLEN", len(vertices))

        print('polygons', len(globalPolygons))

        plt.plot(x,y)
        plt.show()

    askforStop = input("enter 0 to try another path")
    endcheck = int(askforStop)




    


    
    






  


