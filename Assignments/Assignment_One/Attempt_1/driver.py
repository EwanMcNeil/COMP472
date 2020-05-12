##first attempt at Assignment one 
##Read in crime_dt.sph
## it is a shape fi
import numpy as np
import pandas as pd
import geopandas as gpd
import shapefile
import matplotlib.pyplot as plt
import matplotlib.image as mpimg



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

    # plt.figure()
    # plt.xlim(-73.59,-73.55)
    # plt.ylim(45.490,45.530)
    # axes = plt.gca()


    xLength = int((-73.55-(-73.59))/0.01)
    yLength = int((45.530-45.490)/0.01)

    matrix = np.zeros((xLength,yLength))

    count = 0
    y=0
    while( y < yLength):
        x=0
        while(x < xLength):
            tup = table[count]
            crime = tup[0]

            matrix[x,y] = crime

            count += 1
            x += 1
        y +=1

    print(matrix)
    imgplot = plt.imshow(matrix)
    plt.show()
    #fig, (ax0, ax1) = plt.subplots(2, 1)

    
    
    

    # plt.pcolor(matrix, edgecolors='k', linewidths=4)
    # #ax1.set_title('thick edges')

    # #fig.tight_layout()
    # plt.show()


    # #need to create matrix from table 
    # #will be set to the same value
    # dx, dy = 0.01, 0.01

    # ##theres a better way to do this
    # data = np.random.rand(10, 10) * 20
    # cmap = colors.ListedColormap(['red', 'blue'])
    # bounds = [0,10,20]
    # norm = colors.BoundaryNorm(bounds, cmap.N)  



    # fig, ax = plt.subplots()
    # ax.imshow(data, cmap=cmap, norm=norm)

    # # draw gridlines
    # ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    # ax.set_xticks(np.arange(-.5,-73.59,-73.55 ));
    # ax.set_yticks(np.arange(-.5, 45.490,45.530));

    # plt.show()

    # while(count < len(table)):
        
    #     ##first need to get coords out for block
    #     tup = table[count]
    #     crime = tup[0]
    #     xBot = tup[1]
    #     xTop = tup[2]
    #     yBot = tup[3]
    #     yTop = tup[4]

    #     if(crime >= threshold):
    #         print("high")
    #         axes.add_patch(Polygon([(xBot, yBot), (xBot, yTop), (xTop, yBot), (xTop, yTop)],
    #                    closed=True, facecolor='red'))
        
    #     if(crime <= threshold):
    #         print("low")
    #         axes.add_patch(Polygon([(xBot, yBot), (xBot, yTop), (xTop, yBot), (xTop, yTop)],
    #                    closed=True, facecolor='green'))
    #     count += 1
    # plt.show()

    




        
       

##driver calls

table = graphCreation(0.01)

outputTup = table.get(0)
mean = getMean(table)
print("the mean is " + str(outputTup[0]))


thresholdGraph(mean,table)


    


    
    






  


