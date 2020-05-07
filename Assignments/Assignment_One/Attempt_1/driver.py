##first attempt at Assignment one 
##Read in crime_dt.sph
## it is a shape file
import shapefile
import geopandas


sf = shapefile.Reader("Shape/crime_dt.shp")

shapes = sf.shapes()


print(len(shapes))


print(dir(shapes[3]))