

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


def validCoordCheck(x , y):
    outputBool = False
    xBool = False
    yBool = False

    if((x >= -73.59) and (x <= -73.55)):
        xBool = True

    if((y >= 45.49) and (y <= 45.53)):
        yBool =True
    
    if xBool and yBool:
        outputBool = True
    
    return outputBool
