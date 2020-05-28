# -------------------------------------------------------
# Assignment One
# Written by Ewan McNeil 40021787
# For COMP 472 Section JX – Summer 2020
# --------------------------------------------------------


##these varibles need to be accessed by multiple functions in multiple files so 
# they have been isolated here
def init():
    global vertices
    global globalPolygons
    global blocksize
    blocksize = 0
    globalPolygons = []
    vertices = dict()