# -------------------------------------------------------
# Assignment One
# Written by Ewan McNeil 40021787
# For COMP 472 Section JX – Summer 2020
# --------------------------------------------------------

from setupFunctions import *
from helperFunctions import *
import globalVar


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
        currentXYTup = globalVar.vertices[current]
        goalXYTup = globalVar.vertices[goal]
        x1 = currentXYTup[0]
        y1 = currentXYTup[1]
        x2 = goalXYTup[0]
        y2 = goalXYTup[1]
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        return dist
    

    
    def Astar(self,startNode,stopNode):

        print("Starting A* search Algorithm ")
        startTime = time.time()
        openList = set([startNode])
        closedList = set()
        g = {}
        g[startNode] = 0

        #parents contain an adjacency map of all nodes
        parents = {}
        parents[startNode] = startNode


        #finds the next best path in the open list by adding the g[n] and the h[n]
        while len(openList) > 0:
            n = None
            for v in openList:
                if n == None or g[v] + self.h(v,stopNode) < g[n] + self.h(n,stopNode):
                    n = v



            #if there are no more in the open list the algo is done
            if n == None:
                print('Path does not exist!', '\n')
                return None
            #or if its found the end stop
            if n ==stopNode:
                endTime = time.time() - startTime;
                print("Path found, time taken is: "+ str(endTime), '\n')
                path = []

                while parents[n] != n:
                    path.append(n)
                    n = parents[n]
                
                path.append(startNode)
                path.reverse()
                return path



            
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

            #its been visited to swap it to the closed list
            openList.remove(n)
            closedList.add(n)

        print('No path found, please try other nodes', '\n')
    
        return None




##driver code runs two loops one for setting up the graph 
##one for putting in the coordiants
globalVar.init()
newGraph = 0
while newGraph == 0:
    

    ##taking in the block size and the threshold percentage
    sizeCheck = False
    blockSize = 0
    while not sizeCheck:
        blockSize = input("Enter the size of the blocks: ")
        blockSize = float(blockSize)
        print('\n')
        if(blockSize <= 0.01 and blockSize >= 0.001):
            sizeCheck = True
        else:
            print("Please enter a valid block size between 0.001 and 0.01")

    globalVar.blocksize = blockSize

   

    width = 0.04/blockSize
    width = int(width)


    table = getTable(blockSize)

    thresholdCheck = False
    inputThreshold = 0
    while not thresholdCheck:
        inputThreshold = input("Enter the threshold percentage in decimal format: ")
        inputThreshold = float(inputThreshold)
        print('\n')
        if (inputThreshold < 1 and inputThreshold > 0):
            thresholdCheck = True
        else: 
            print("invalid percentage please reenter")




    #calcuatiing the threhold value from the ordered list of crimes
    mean = getMean(table, inputThreshold)

    print("the Threshold Value is " + str(mean), '\n')


    

    ##setup functions for the adjacency and passing the plot
    globalPolygonsCopy = []
    colorplotax = thresholdGraph(blockSize,mean,table)
    adjaencyGraph = createAdjacency(blockSize,mean,table,width)


    #used for testing
    #graphAdjaceny(adjaencyGraph)


    #creating graph from the graph class for the A* 
    graph1 = Graph(adjaencyGraph)


    #loop for the driver 
    endcheck = 0
    while(endcheck == 0):

        #polygons can only be displayed once so copying them
        globalPolygonsCopy.clear()
        polycount = 0
        while(polycount < len(globalVar.globalPolygons)):
            new_patch = copy(globalVar.globalPolygons[polycount])
            globalPolygonsCopy.append(new_patch)
            polycount += 1

       

        #inputs for the start and end coords with checks 
        startBool = False
        startX = 0
        startY = 0
        while not startBool: 
            startX, startY = map(float, input("Please enter start location xcoord ycoord seperated by space ").split());
            startBool = validCoordCheck(startX,startY)

            if startBool == False:
                print("please enter a valid coords ")
        
        endBool = False
        endX = 0
        endY = 0
        while not endBool: 
            endX, endY = map(float, input("Please enter end location xcoord ycoord seperated by space ").split());
            endBool = validCoordCheck(endX,endY)

            if endBool == False:
                print("please enter a valid coords ")

        

        #replotting the graph to display the path
        plt.close()
        fig = plt.figure(None, dpi=90)
        ax = fig.add_subplot(111)
       
        polycount = 0
        while(polycount < len(globalVar.globalPolygons)):
            ax.add_patch(globalPolygonsCopy[polycount])
            polycount += 1

        axes = plt.gca()
        axes.set_xlim([-73.59,-73.55])
        axes.set_ylim([45.49,45.53])
        ax.set_xticks(np.arange(-73.59,-73.55,blockSize));
        ax.set_yticks(np.arange(45.49,45.53,blockSize));
        plt.xticks(rotation=45) 


        plt.plot(startX, startY, marker='o', markersize=3, color="black")
        startNode = estimateNode(startX,startY)
        startInt = int(startNode)
        
        plt.plot(endX, endY, marker='o', markersize=3, color="black")

        endNode = estimateNode(endX,endY)
        endInt = int(endNode)


        #getting the path by passing the nodes found from the input
        path = graph1.Astar(startInt,endInt)
        title = "Path from: (" + str(startX) + "," + str(startY) +")" + " to " + "(" + str(endX) + "," + str(endY)  +")" 
        plt.title(title)


        #if path has been found plot it
        if(path != None):
            x = []
            y = []

            finalloop = 0
            while(finalloop < len(path)):
                tup = globalVar.vertices[path[finalloop]]
                x.append(tup[0])
                y.append(tup[1])
                finalloop += 1
            plt.plot(x,y)
            


        plt.show(block = False)


        #after path display ask for next step from the user
        stopBool = False
        while not stopBool:
            askforStop = input("enter 0 to try another path or 1 to make a new graph: ")
            endcheck = int(askforStop)
            print('\n')
            if (endcheck == 1) or (endcheck == 0):
                stopBool = True
            else:
                print("please enter a valid input")
           
        



    


    
    






  


