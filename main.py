import random
from maze2 import Maze

class bc:
    gray = '\033[30m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    end = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'


def color(string, color):
    return f'{color}{string}{bc.end}'

class Player:
    def __init__(self):
        self.health = 100
        self.weapon = None
        self.armor = None
        self.inventory = []

    def __str__(self):
        return '@'


class Item:
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value


class Weapon(Item):
    def __init__(self, name, description, value, damage):
        super().__init__(name, description, value)
        self.damage = damage


class Dungeon:
    def __init__(self):
        self.rooms = []



class Room(Maze):
    def __init__(self):
        super().__init__(20, 10)
        self.make_maze()
        self.maze = self.create_matrix()
        self.placePlayer()
        self.colorMaze()

    def colorMaze(self):
        colorDict = {
            '#': '\033[47m \033[0m',
            '@': '\033[32m@\033[0m',
            '.': ' ',
        }
        for i, row in enumerate(self.maze):
            for j, element in enumerate(row):
                self.maze[i][j] = colorDict[element]

    def placePlayer(self):
        #list all the path that is surrounded by 3 walls
        possiblePath = []
        for i, row in enumerate(self.maze):
            for j, element in enumerate(row):
                if element == ".":
                    walls = 0
                    direction = ((1, 0), (-1, 0), (0, 1), (0, -1))
                    for dir in direction:
                        if self.maze[i + dir[0]][j + dir[1]] == "#":
                            walls += 1
                    if walls == 3:
                        possiblePath.append((i, j))

        coord = random.choice(possiblePath)
        self.maze[coord[0]][coord[1]] = "@"

    def __str__(self):
        maze = []
        for row in self.maze:
            maze.append(''.join(row))
        return '\n'.join(maze)

room = Room()
print(room)
