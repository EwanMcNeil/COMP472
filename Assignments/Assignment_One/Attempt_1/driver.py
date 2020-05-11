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









  


