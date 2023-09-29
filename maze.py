import random

class Maze:
    def __init__(self, width, height):
        self.maze, self.width, self.height = self.init_maze(width, height)
        self.generate_maze()

    def init_maze(self, width, height):
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
    
    def generate_maze(self, next=None):
        unvisited = []
        for i, list in enumerate(self.maze):
            for j, value in enumerate(list):
                if value == "u":
                    unvisited.append([i, j])
        if len(unvisited) == 0:
            return
        if next == None:
            current = random.choice(unvisited)
        else:
            current = next
        self.maze[current[0]][current[1]] = "."
        direction = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        #remove the direction if it is out of bound
        for dir in direction:
            if current[0] + dir[0] <= 0 or current[0] + dir[0] >= self.height-1:
                direction.remove(dir)
            elif current[1] + dir[1] <= 0 or current[1] + dir[1] >= self.width-1:
                direction.remove(dir)
        #remove the direction if there is no wall to break or if next is path
        for dir in direction:
            if self.maze[int(current[0] + dir[0]/2)][int(current[0] + dir[0]/2)] == "." or self.maze[current[0] + dir[0]][current[1] + dir[1]] == ".":
                direction.remove(dir)
        random.shuffle(direction)
        randomDirection = random.choice(direction)
        direction.remove(randomDirection)
        self.maze[current[0] + randomDirection[0] // 2][current[1] + randomDirection[1] // 2] = "."
        self.print_maze()
        print('')
        self.generate_maze(next=[current[0] + randomDirection[0], current[1] + randomDirection[1]])

    def print_maze(self):
        for i in range(self.height+1):
            for j in range(self.width+1):
                print(self.maze[i][j], end="")
            print()


if __name__ == "__main__":
    maze = Maze(20, 10)
    maze.print_maze()
    
