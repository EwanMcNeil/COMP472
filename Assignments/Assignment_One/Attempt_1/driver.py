##first attempt at Assignment one 
##Read in crime_dt.sph
## it is a shape fi
import numpy as np
import pandas as pd
import geopandas as gpd
import shapefile
import matplotlib.pyplot as plt
import seaborn as sns




shpPath = 'Shape/crime_dt.shp'
data = gpd.read_file(shpPath)



# iterating the columns 
for col in data.columns: 
    print(col) 

data.plot()

plt.show()
print(type(data))


print(data.head(9))




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
    graph = Graph()

    xBot = -73.59
    xTop = -73.59+size
    yBot = 45.49
    yTop = 45.49 +size

    #count gives an index for each box
    count = 1

    while(True):
        crime = crimesWithinBounds(xBot,xTop,yBot,yTop)
        graph.addinfo(count,xBot, xTop, yBot, yTop, crime)
        xBot += size
        xTop += size
        yBot += size
        yTop += size
        count += 1
        if(xTop >= -73.55):
            return graph



print(graphCreation(0.002).getLength)


    
    






  


