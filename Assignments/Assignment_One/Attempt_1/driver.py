##first attempt at Assignment one 
##Read in crime_dt.sph
## it is a shape fi
import numpy as np
import pandas as pd
import geopandas as gpd
import shapefile
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import seaborn as sns




shpPath = 'Shape/crime_dt.shp'
data = gpd.read_file(shpPath)



# iterating the columns 
for col in data.columns: 
    print(col) 

# data.plot()

# plt.show()
# print(type(data))


# print(data.head(9))




#need to go through all of it and find
#within the thresholds how many occured



def crimesWithinBounds(xBot,xTop,yBot,yTop):
    shape = shapefile.Reader(shpPath, encoding='ISO-8859-1')
    shapeRecords = shape.shapeRecords()
    count = 0
    for i in range(len(shapeRecords)):
        x = shapeRecords[i].shape.__geo_interface__["coordinates"][0]
        y = shapeRecords[i].shape.__geo_interface__["coordinates"][1]

        if xBot <= x <= xTop:
           if yBot <= y <= yTop:
                count += 1
    return count


output = crimesWithinBounds(-73.552,-73.551,45.490,45.492)

print("the number of crimes within bounds is: " + str(output))



#trying to build the graph to both display the blocks
#but also be the basis for the A*



##need to use this for the modes later
##but for now have a lookup table for the grids and 
##their values
class Graph:

    def __init__(self):
        # default dictonaily to store the graph
        self.graph = dict()

    # edges are appended right to it and added if not existing
    def addEdge(self, u, v):
        if u not in self.graph:
            print(True)
            self.graph[u] = [v]
        else:
            print(False)
            self.graph[u].append(v)
        if v not in self.graph:
            print(True)
            self.graph[v] = [u]
        else:
            print(False)
            self.graph[v].append(u)

    # coords are appended after
    def addinfo(self,count,xBot, xTop, yBot, yTop, crimeNumber):
        self.graph[count] = [crimeNumber]
        coords = (xBot, xTop, yBot, yTop)
        self.graph[count].append(coords)

    def getLength(self):
        return len(self.graph)





#size is the multipler so I think as you go along you 
#add a bit each time
def graphCreation(size):
    table = dict()

    xBot = -73.59
    xTop = -73.59+size
    yBot = 45.49
    yTop = 45.49 +size

    #count gives an index for each box
    #we start at bottom left here
    count = 0
    ## this needs to be a two loop with max bounds

    
    while(yTop <= 45.53):
       
        while(xTop <= -73.55):
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


def thresholdGraph(threshold,table):

    plt.figure()
    axes = plt.gca()
    count = 0
    while(count < len(table)):
        
        ##first need to get coords out for block
        tup = table[count]
        crime = tup[0]
        xBot = tup[1]
        xTop = tup[2]
        yBot = tup[3]
        yTop = tup[4]

        if(crime >= threshold):
            print("high")
            axes.add_patch(Polygon([(xBot, yBot), (xBot, yTop), (xTop, yBot), (xTop, yTop)],
                       closed=True, facecolor='red'))
        
        if(crime <= threshold):
            print("low")
            axes.add_patch(Polygon([(xBot, yBot), (xBot, yTop), (xTop, yBot), (xTop, yTop)],
                       closed=True, facecolor='green'))
        count += 1

    




        
       

##driver calls

table = graphCreation(0.01)

outputTup = table.get(0)
mean = getMean(table)
print("the mean is " + str(outputTup[0]))


thresholdGraph(mean,table)


    


    
    






  


