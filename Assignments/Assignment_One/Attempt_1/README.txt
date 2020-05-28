# -------------------------------------------------------
# Assignment One
# Written by Ewan McNeil 40021787
# For COMP 472 Section JX – Summer 2020
# --------------------------------------------------------



--------------------------------------
Libraries needed (all imports can be founnd in helperfunctions.py)
----------------------------------

numpy 
(for array manipulation)

shapefile from pyshp 
(reading in shapefiles)

matplotlib colors and pyplot 
(plotting)

shapely.geometry.polygon 
(plotting)

descartes PolygonPatch
(plotting)

math
(finding diagional and floating point)

copy
(saving the graph and moving it)

time 
(for calcualting run time)


----------------------------------
Running the Program
----------------------------------
This assignment was created with anaconda with the libraies above, to run the program
run the command "python driver.py" in the local directory and the program will begin

1. First a prompt comes up for the size of the blocks in the grid, the lowest the program
can handle is 0.001 due to rounding specified 

2. After the shapefile has been loaded in (may take a few seconds) another prompt will
appear asking for the threshold level, enter a decimal value between 0 and 1, for example 0.75

3. The program will then generate the adjacency matrix and other setup which may take a few
seconds as well

4. The prompt will then ask for the coordinates of the start and end locations enter them in x y 
format with a space between 

5. The Astar algo will then run with the inputs and then display a graph and the time when completed

6. After the program will prompt asking for another path for the previous grid or to create another grid
 with differnt blocksize and threshold 




----------------------------------
Notes
----------------------------------

-driver file contains first the main class for the implementation of the A* algorithm, and taking in all the inputs in the program

- setupfunctions deal with creating the graph dealing with the data

-helper functions deal with checks and calcuations