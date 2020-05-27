import numpy as np
import pandas as pd
import geopandas as gpd
import shapefile
from matplotlib import colors
import numpy as np
from matplotlib import pyplot as plt
from shapely.geometry.polygon import Polygon
from descartes import PolygonPatch
import math  
from copy import copy




##main class for the algoithm
##used after first the visual has been created with the thresholds 
##and an adjacency list has been made to be passed to it
class Graph:
    def __init__(self,adjacencyList):
        self.adjacencyList = adjacencyList
    def getNeighbors(self, v):
        return self.adjacencyList[v]


    #heuristic is bulit upon finding the diagonal length to the end point
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
    

    
    def Astar(self,startNode,stopNode):
      
        openList = set([startNode])
        closedList = set()
        g = {}
        g[startNode] = 0

        #parents contain an adjacency map of all nodes
        parents = {}
        parents[startNode] = startNode

        while len(openList) > 0:
            n = None
            for v in openList:
                if n == None or g[v] + self.h(v,stopNode) < g[n] + self.h(n,stopNode):
                    n = v



            #if there are no more in the open list the algo is done
            if n == None:
                print('Path does not exist!')
                return None
            #or if its found the end stop
            if n ==stopNode:
                path = []

                while parents[n] != n:
                    path.append(n)
                    n = parents[n]
                
                path.append(startNode)
                path.reverse()
                return path



            #main search part
            #goes through neighbors of current node
            for(m, weight) in self.getNeighbors(n):
            
                    #if its an unseen node add to open, and calculate the g[n]
                    #by adding g[n] to parents g[n]
                 if m not in openList and m not in closedList:
                    openList.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                    #if it has been seen before check if its a shorter path
                    #if so add it
                 elif m in closedList:
                     if g[m] > g[n] + weight:
                      g[m] = g[n] + weight
                      parents[m] = n
                      closedList.remove(m)
                      openList.add(m)

            openList.remove(n)
            closedList.add(n)

        print('No path found, please try other nodes')
        return None




#Sums up all the crimes within a block
def crimesWithinBounds(xBot,xTop,yBot,yTop,shapeList):
    count = 0
    for i in range(len(shapeList)):
        x = shapeList[i][0]
        y = shapeList[i][1]

        if xBot <= x <= xTop:
           if yBot <= y <= yTop:
                count += 1
    return count







#get table converts the shapefile into array data
#and effiecieny 
def getTable(size):
    table = dict()

    ##driver calls
    shpPath = 'Shape/crime_dt.shp'
#creating global matrix with size of the grid
    shape = shapefile.Reader(shpPath, encoding='ISO-8859-1')
    shapeRecords = shape.shapeRecords()

    shapeList = []

    for i in range(len(shapeRecords)):
        x = shapeRecords[i].shape.__geo_interface__["coordinates"][0]
        y = shapeRecords[i].shape.__geo_interface__["coordinates"][1]
        shapeTuple = (x,y) 
        shapeList.append(shapeTuple)

    xBot = -73.59
    xTop = -73.59+size
    yBot = 45.49
    yTop = 45.49 +size

  
    count = 0
    yCount  =0
    while(yTop <= 45.53):
        while(xTop <= -73.55):
         xBot = truncate(xBot, 3)
         xTop = truncate(xTop, 3)
         yBot = truncate(yBot, 3)
         yTop = truncate(yTop, 3)
         crime = crimesWithinBounds(xBot,xTop,yBot,yTop,shapeList)
         info = (crime,xBot, xTop, yBot, yTop)
         table[count] = info
         count += 1
         xBot += size
         xTop += size
         xBot = round(xBot, 3)
         xTop = round(xTop, 3)
        xBot = -73.59
        xTop = -73.59+size
        yBot += size
        yTop += size
        xTop = round(xTop, 3)
        yBot = round(yBot, 3)
        yTop = round(yTop, 3)
        yCount += 1
    return table


#finds the threshold value that the assignment asks for 
#creates an array of all the crime values and sorts by size
#then takes the value at that percentage
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
    median = crimeList[index] 
    return median
    

#plots out the threshold graph to start
#uses polygons to fill in the blocks
#with data created by table
#a second graph is created for the path
def thresholdGraph(blockSize,threshold,table):
    
    global globalPolygons
    global vertices
    fig = plt.figure(None, dpi=90)
    ax = fig.add_subplot(111)
  
    count = 0
    xCount = 0
    yCount = 0
    xylength = int(0.04/blockSize)

    halfBlock = blockSize/2

    midX = []
    midY = []
    midCrimes = []


    while(yCount < xylength):
        while(xCount < xylength):
         tup = table[count]
         crime = tup[0]
         xBot=tup[1]
         xTop=tup[2]
         yBot=tup[3]
         yTop=tup[4]

         midValueX = xBot +halfBlock
         midValuey = yBot + halfBlock
         midX.append(midValueX)
         midY.append(midValuey)
         midCrimes.append(crime)


            #adds a vertice into the dict
         coord = (xBot,yBot) 
         vertices[count] = coord

         polygon = Polygon([(xBot, yBot),(xBot,yTop),(xTop,yTop),(xTop,yBot)])
         if(crime < threshold):
             patch = PolygonPatch(polygon, fc= 'purple')
         else:
             patch = PolygonPatch(polygon, fc= 'yellow')
         new_patch = copy(patch)
         globalPolygons.append(new_patch)
         ax.add_patch(patch)
         count += 1
         xCount += 1
        xCount = 0
        yCount += 1

    title = str(blockSize) + " Graph with " + str(threshold) + " as its Threshold"
    axes = plt.gca()
    axes.set_xlim([-73.59,-73.55])
    axes.set_ylim([45.49,45.53])
    ax.set_xticks(np.arange(-73.59,-73.55,blockSize));
    ax.set_yticks(np.arange(45.49,45.53,blockSize));

    midCrimesCount = 0
    for a,b in zip(midX, midY): 
        plt.text(a, b, midCrimes[midCrimesCount])
        midCrimesCount += 1

    plt.title(title)
    plt.xticks(rotation=45) 
    plt.show(block = False)
    return ax



#the adjacney matrix is created by taking the bottom left node of all the blocks
#and calcuatining if the eight paths near it are viable paths
#if they are those edges are appended to that current node
def createAdjacency(size,mean,table,width):
    global vertices
    graph = dict()

    count = 0
   
    while(count< len(table)): 

        #find the bottom left vertice
        outTuple = table[count]
        x = outTuple[1]
        y = outTuple[3]

        x = truncateThree(x)
        y = truncateThree(y)
       
        graph[count] = []

        #the one point for quadrents and points is top left
        #goes clockwise
        point1 = findVertice(x-size,y+size)
        point2 = findVertice(x,y+size)
        point3 = findVertice(x+size,y+size)
        point4 = findVertice(x+size,y)
        point5 = findVertice(x+size,y-size)
        point6 = findVertice(x,y-size)
        point7 = findVertice(x-size,y-size)
        point8 = findVertice(x-size,y)

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
        
        #true is less (purple)
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
        #if its a legal move append to the graph
        #diagonals
        if(oneBool):
            if(point1 != None):
                newtuple = (point1,1.5)
                graph[count].append(newtuple)

        if(twoBool):
            if(point3 != None):
                newtuple = (point3,1.5)
                graph[count].append(newtuple)
        
        if(threeBool):
            if(point5 != None):
                newtuple = (point5,1.5)
                graph[count].append(newtuple)

        if(fourBool):
            if(point7 != None):
                newtuple = (point7,1.5)
                graph[count].append(newtuple)

        #Straight ones
        if((oneBool) or (twoBool)):
            if(point2 != None):
                if((oneBool) and (twoBool)):
                    newtuple = (point2,1.3)
                    graph[count].append(newtuple)
                else:
                    newtuple = (point2,1)
                    graph[count].append(newtuple)
        

        if((twoBool) or (threeBool)):
            if(point4 != None):
                if((twoBool) and  (threeBool)):
                    newtuple = (point4,1.3)
                    graph[count].append(newtuple)
                else:
                    newtuple = (point4,1)
                    graph[count].append(newtuple)

        if((threeBool) or (fourBool)):
            if(point6 != None):
                if((threeBool) and (fourBool)):
                 newtuple= (point6,1.3)
                 graph[count].append(newtuple)
                else:
                    newtuple = (point6,1)
                    graph[count].append(newtuple)

        if((fourBool) or (oneBool)):
            if(point8 != None):
                if((oneBool) and (twoBool)):
                    newtuple = (point8,1.3)
                    graph[count].append(newtuple)
                else:
                    newtuple = (point8,1)
                    graph[count].append(newtuple)

      
        count += 1
   
    return graph



def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier




#used to check the adjacencies
#not needed in the demo
#just to ensure paths are being properly generated
def graphAdjaceny(graph):
    global vertices
    fig = plt.figure(None, dpi=90)
    ax = fig.add_subplot(111)
    axes = plt.gca()
    axes.set_xlim([-73.59,-73.55])
    axes.set_ylim([45.49,45.53])
    ax.set_xticks(np.arange(-73.59,-73.55,blockSize));
    ax.set_yticks(np.arange(45.49,45.53,blockSize));
    plt.xticks(rotation=45) 

    count = 0
    while(count < len(graph)):
        start = vertices[count]
        associated = graph[count]
        innerCount = 0
        while(innerCount < len(associated)):
            endNode = associated[innerCount]
            endNode = endNode[0]
            end = vertices[endNode]
            xvalues = [start[0], end[0]]
            yvalues= [start[1], end[1]]
            plt.plot(xvalues,yvalues)
            innerCount += 1
        count += 1
    plt.show(block = False)



##used to find the node from the vertice count
def findVertice(x, y):
    global vertices
    global blockSize
    count = 0
    x = round(x , 3)
    y = round(y, 3)
    x = truncateThree(x)
    y= truncateThree(y)


    posrange = blockSize/2
    negRange = -1*blockSize
  
    while(count <len(vertices)):
        outTuple = vertices[count]
        xSearch = outTuple[0]
        ySearch = outTuple[1]
        xdiff = x - xSearch
        ydiff = y - ySearch
        

        if(xdiff >= negRange and xdiff <= posrange) and (ydiff >= negRange and ydiff <= posrange):
            return count
        count += 1
    return None


##these do the same thing take out one
def truncateThree(n, decimals=3):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier



##function used to find the bottom left point that corresponding to 
##a starting or ending point in the input 
def estimateNode(x ,y):
 
    global blockSize

    xcount = 0
    xstart = -73.59
    while(xstart < x):
        xcount += 1
        xstart += blockSize
    
    xcount -= 1
    
    ycount = 0
    ystart = 45.49
    while(ystart < y):
        ycount += 1
        ystart += blockSize

    ycount -= 1

   
    xMult = xcount*blockSize
    yMult = ycount*blockSize

    outputX = -73.59 + xMult
    outputY = 45.49 +yMult

    outputX = truncate(outputX, 3)
    outputY = truncate(outputY,3)


    node = findVertice(outputX,outputY)
    return node




##driver code runs two loops one for setting up the graph 
##one for putting in the coordiants

newGraph = 0
while newGraph == 0:
    

    vertices = dict()
    blockSize = input("enter the size of the blocks ")
    blockSize = float(blockSize)

    width = 0.04/blockSize
    width = int(width)


    table = getTable(blockSize)

    inputThreshold = input("enter the threshold percentage")
    inputThreshold = float(inputThreshold)
    mean = getMean(table, inputThreshold)

    print("the Threshold Value is " + str(mean))





    globalPolygons = []
    globalPolygonsCopy = []

    
    colorplotax = thresholdGraph(blockSize,mean,table)



    adjaencyGraph = createAdjacency(blockSize,mean,table,width)


    #used for testing
    #graphAdjaceny(adjaencyGraph)

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

    
        startX, startY = map(float, input("Please enter start location xcoord ycoord seperated by space ").split());

        plt.plot(startX, startY, marker='o', markersize=3, color="black")
        startNode = estimateNode(startX,startY)
        startInt = int(startNode)

      

        endX, endY = map(float, input("Please enter end location xcoord ycoord seperated by space ").split());
        plt.plot(endX, endY, marker='o', markersize=3, color="black")

        endNode = estimateNode(endX,endY)
        endInt = int(endNode)

        path = graph1.Astar(startInt,endInt)
        title = "Path from: (" + str(startX) + "," + str(startY) + "," +")" + " to " + "(" + str(endX) + "," + str(endY) + "," +")" 
        plt.title(title)

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
            plt.plot(x,y)


        plt.show(block = False)

        askforStop = input("enter 0 to try another path or 1 to make a new graph")
        endcheck = int(askforStop)




    


    
    






  


