
##########################################################
# maze solving program using the Left Hand Rule algorithm
# DavisMT 07.01.2018
##########################################################
from collections import defaultdict
import turtle                    # import turtle library
import time
import sys

wn = turtle.Screen()               # define the turtle screen
wn.bgcolor("black")                # set the background colour
# setup the dimensions of the working window
wn.setup(1300, 700)


# class for the Maze turtle (white square)
class Maze(turtle.Turtle):               # define a Maze class
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")            # the turtle shape
        self.color("white")             # colour of the turtle
        self.penup()                    # lift up the pen so it do not leave a trail
        # sets the speed that the maze is written to the screen
        self.speed(0)

# class for the End marker turtle (green square)


class End(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("green")
        self.penup()
        self.speed(0)

# class for the sprite turtle (red turtle)


class sprite(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("turtle")
        self.color("red")
        # point turtle to point down angle has been predefined
        self.setheading(270)
        self.penup()
        self.speed(0)

    def spriteDown(self):
        if (self.heading() == 270):                   # check to see if the sprite is pointing down
            x_walls = round(sprite.xcor(), 0)          # sprite x coordinates =
            y_walls = round(sprite.ycor(), 0)
            if (x_walls, y_walls) in finish:          # if the sprite is on tha
                print("lefthand rule count: " + str(LHRcount))
                print("Finished")
                endProgram()
            if (x_walls + 24, y_walls) in walls:          # check to see if they are walls on the left
                if(x_walls, y_walls - 24) not in walls:   # check to see if path ahead is clear
                    self.forward(24)
                else:
                    self.right(90)
            else:
                self.left(90)
                self.forward(24)

    def spriteleft(self):
        if (self.heading() == 0):
            x_walls = round(sprite.xcor(), 0)
            y_walls = round(sprite.ycor(), 0)
            if (x_walls, y_walls) in finish:   # check turtle coordinates are at the finish line
                print("lefthand rule count: " + str(LHRcount))
                print("Finished")
                endProgram()
            if (x_walls, y_walls + 24) in walls:       # check to see if they are walls on the left
                if(x_walls + 24, y_walls) not in walls:
                    self.forward(24)
                else:
                    self.right(90)
            else:
                self.left(90)
                self.forward(24)

    def spriteUp(self):
        if (self.heading() == 90):
            x_walls = round(sprite.xcor(), 0)
            y_walls = round(sprite.ycor(), 0)
            if (x_walls, y_walls) in finish:   # check turtle coordinates are at the finish line
                print("lefthand rule count: " + str(LHRcount))
                print("Finished")
                endProgram()
            if (x_walls - 24, y_walls) in walls:  # check to see if they are walls on the left
                if (x_walls, y_walls + 24) not in walls:
                    self.forward(24)
                else:
                    self.right(90)
            else:
                self.left(90)
                self.forward(24)

    def spriteRight(self):
        if (self.heading() == 180):

            x_walls = round(sprite.xcor(), 0)
            y_walls = round(sprite.ycor(), 0)
            if (x_walls, y_walls) in finish:   # check turtle coordinates are at the finish line
                print("lefthand rule count: " + str(LHRcount))
                print("Finished")
                endProgram()
            if (x_walls, y_walls - 24) in walls:  # check to see if they are walls on the left
                if (x_walls - 24, y_walls) not in walls:
                    self.forward(24)
                else:
                    self.right(90)
            else:
                self.left(90)
                self.forward(24)


class Node:
    def __init__(self, key, x, y):
        self.u = key
        self.x = x
        self.y = y

    def setDistance(self, distance):
         self.distance = distance


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
    def addcoordtoNode(self, u, x, y):
        coord = ("coord", x, y)
        self.graph[u].append(coord)

    # function to make a breadth first seach of the graph

    def bfs_shortest_path(self, start, goal):
   
        explored = []
        queue = [[start]]

        print("start", start)
        print("goal", goal)

        if start == goal:
            return "That was easy! Start = goal"
 
   
        while queue:
 
            path = queue.pop(0)
            node = path[-1]
            print("path", path)
            print("node", node)

            # how im creating the graph isnt right
            if node not in explored:
                neighbours = self.graph[node]
       
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)
                    # return path if neighbour is goal
                    if neighbour == goal:
                        global BFSqueue
                        BFSqueue = new_path
                        return new_path
            explored.append(node)
 
    # in case there's no path between the 2 nodes
        return "So sorry, but a connecting path doesn't exist :"
    # in case there's no path between the 2 nodes





def endProgram():
    wn.exitonclick()
    sys.exit()


grid = [
"++++++++++++++++++++++++++++++++++++++++++++++",
"+ s             +                            +",
"+  ++++++++++  +++++++++++++  +++++++  ++++  +",
"+           +                 +        +     +",
"+  +++++++  +++++++++++++  +++++++++++++++++++",
"+  +     +  +           +  +                 +",
"+  +  +  +  +  +  ++++  +  +  +++++++++++++  +",
"+  +  +  +  +  +  +     +  +  +  +        +  +",
"+  +  ++++  +  ++++++++++  +  +  ++++  +  +  +",
"+  +     +  +              +           +  +  +",
"+  ++++  +  ++++++++++++++++  +++++++++++++  +",
"+     +  +                    +              +",
"++++  +  ++++++++++++++++++++++  ++++++++++  +",
"+  +  +                    +     +     +  +  +",
"+  +  ++++  +++++++++++++  +  ++++  +  +  +  +",
"+  +  +     +     +     +  +  +     +     +  e",
"+  +  +  +++++++  ++++  +  +  +  ++++++++++  +",
"+                       +  +  +              +",
"++++  +  +  ++++++++++  +  +  +  +++++++++++++",
"+++++++++++++++++++++++++++++++++++++++++++++",
]



def setupMaze(grid):




    for y in range(len(grid)):                       # select each line in the grid
        for x in range(len(grid[y])):                # identify each character in the line

                                                    


            character = grid[y][x]                   # assign the grid reference to the variable character
            screen_x = -588 + (x * 24)               # assign screen_x to screen starting position for x ie -588
            screen_y = 288 - (y * 24)                # assign screen_y to screen starting position for y ie  288

            if character == "+":                     # if grid character contains an +
                maze.goto(screen_x, screen_y)        # move turtle to the x and y location and
                maze.stamp()                         # stamp a copy of the turtle (white square) on the screen
                walls.append((screen_x, screen_y))   # add coordinate to walls list

            if character == "e":                     # if grid character contains an e
                end.goto(screen_x, screen_y)         # move turtle to the x and y location and
                end.stamp()                          # stamp a copy of the turtle (green square) on the screen
                finish.append((screen_x, screen_y))  # add coordinate to finish list

            if character == "s":                     # if the grid character contains an s
                sprite.goto(screen_x, screen_y)      # move turtle to the x and y location
                spriteBFS.goto(screen_x,screen_y)


def gridToGraph(grid,g):

    gridCount = 1


    for y in range(len(grid)):                       # select each line in the grid
        for x in range(len(grid[y])): 

           
            gridCount += 1

            character = grid[y][x]                   # assign the grid reference to the variable character
            screen_x = -588 + (x * 24)               # assign screen_x to screen starting position for x ie -588
            screen_y = 288 - (y * 24)
            node = gridCount

            global Coordmap
            Coordmap[gridCount] = [screen_x,screen_y]

            if character == "s":
                 global startNode
                 startNode = gridCount
                 if (screen_x - 24,screen_y) not in walls:
                    g.addEdge(gridCount,gridCount-1)
                 if (screen_x + 24, screen_y) not in walls:
                    g.addEdge(gridCount,gridCount+1)
                 if (screen_x, screen_y-24) not in walls:
                    g.addEdge(gridCount,gridCount + 46)
                 if (screen_x, screen_y+24) not in walls:
                    g.addEdge(gridCount, gridCount -46)  

            if character == " ":
                 if (screen_x - 24,screen_y) not in walls:
                    g.addEdge(gridCount,gridCount-1)
                 if (screen_x + 24, screen_y) not in walls:
                    g.addEdge(gridCount,gridCount+1)
                 if (screen_x, screen_y-24) not in walls:
                    g.addEdge(gridCount,gridCount + 46)
                 if (screen_x, screen_y+24) not in walls:
                    g.addEdge(gridCount, gridCount -46)  
            if character == "e":
                global endNode
                endNode = gridCount




class spriteBFS(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("turtle")
        self.color("green")
        self.setheading(270)  # point turtle to point down angle has been predefined
        self.penup()
        self.speed(0)
    
    def nextMove(self,nodeNumber):

        screen_x = Coordmap[nodeNumber][0]               # assign screen_x to screen starting position for x ie -588
        screen_y = Coordmap[nodeNumber][1]

        print("moved" + str(screen_x) + str(screen_y))
        self.goto(screen_x,screen_y)










# ############ main program starts here  ######################
g = Graph()
maze = Maze()                # enable the maze class
sprite = sprite()            # enable the sprite  class
spriteBFS = spriteBFS()
end = End()                  # enable End position class
walls =[]                    # create walls coordinate list
finish = []                  # enable the finish array

Coordmap = dict()

BFSqueue = []

LHRcount = 0
startNode = 0
endNode = 0


setupMaze(grid)              # call the setup maze function
gridToGraph(grid,g)




print(g.bfs_shortest_path(startNode,endNode))






while True:
    sprite.spriteRight()
    sprite.spriteDown()
    sprite.spriteleft()
    sprite.spriteUp()
    LHRcount += 1

    nextmove = BFSqueue.pop(0)
    print(nextmove)

    spriteBFS.nextMove(nextmove)

    time.sleep(0.5)
