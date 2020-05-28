
from helperFunctions import *
import globalVar

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
    
    globalVar.globalPolygons
    globalVar.vertices
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
         globalVar.vertices[count] = coord

         polygon = Polygon([(xBot, yBot),(xBot,yTop),(xTop,yTop),(xTop,yBot)])
         if(crime < threshold):
             patch = PolygonPatch(polygon, fc= 'purple')
         else:
             patch = PolygonPatch(polygon, fc= 'yellow')
         new_patch = copy(patch)
         globalVar.globalPolygons.append(new_patch)
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
