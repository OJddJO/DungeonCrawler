import random

class Maze:
    def __init__(self, width, height):
        self.maze, self.width, self.height = self.initMaze(width, height)
        self.generateMaze()

    def initMaze(self, width, height):
        if width % 2 != 0:
            width += 1
        if height % 2 != 0:
            height += 1
        maze = []
        for i in range(height):
            maze.append([])
            for j in range(width):
                if i == 0 or i == height or j == 0 or j == width:
                    maze[i].append("#")
                elif i % 2 == 0 or j % 2 == 0:
                    maze[i].append("#")
                else:
                    maze[i].append("u")
            maze[i].append("#")
        maze.append(["#" for i in range(width + 1)])
        return maze, width, height
    
    def generateMaze(self):
        #list unvisited cells
        unvisited = []
        for i in range(self.height): #row
            for j in range(self.width): #column
                if self.maze[i][j] == "u":
                    unvisited.append((i, j))

        #randomly choose a starting point
        start = random.choice(unvisited)
        self.maze[start[0]][start[1]] = "."

        def walk(self, current, last = None):
            direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            #remove the direction if it is out of bound
            for dir in direction:
                if current[0] + dir[0] < 1 or current[0] + dir[0] >= self.height-1:
                    direction.remove(dir)
                elif current[1] + dir[1] < 1 or current[1] + dir[1] >= self.width-1:
                    direction.remove(dir)
            #remove the direction if next is path
            for dir in direction:
                if self.maze[current[0] + dir[0]*2][current[1] + dir[1]*2] != ".":
                    direction.remove(dir)
            #if there is no direction, return
            if len(direction) == 0:
                return 0 #dead end return to last direction
            elif len(direction) == 1 and self.maze[current[0] + dir[0]*2][current[1] + dir[1]*2] == ".":
                return 0 #return to last direction

            print(direction)
            #randomly choose a direction
            next = random.choice(direction)
            #last defines the last position if the direction is unchanged
            if last == None:
                last = (current, next)
            elif last[1] != next:
                last = (current, next)
            #break the wall
            self.maze[current[0] + next[0]][current[1] + next[1]] = "."
            self.maze[current[0] + next[0]*2][current[1] + next[1]*2] = "."
            #remove current from unvisited
            if current in unvisited:
                unvisited.remove(current)
            self.printMaze()
            #walk to next
            value = walk(self, (current[0] + next[0]*2, current[1] + next[1]*2), last)
            if value == 0 and len(unvisited) != 0:
                walk(self, current, last)
            return
        
        walk(self, start)

    def printMaze(self):
        for i in range(self.height+1):
            for j in range(self.width+1):
                print(self.maze[i][j], end="")
            print()

maze = Maze(20, 10)
maze.printMaze()