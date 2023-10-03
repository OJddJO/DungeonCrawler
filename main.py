import random
from maze import Maze

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
        self.baseDamage = damage


class Dungeon:
    def __init__(self):
        self.rooms = []
        self.floor = 0 #index of the current room

    def addRoom(self, room):
        self.rooms.append(room)

    def makeDungeon(self, nbRoom = random.randint(5, 10)):
        for i in range(nbRoom):
            self.addRoom(Room())


class Room(Maze):
    def __init__(self, width = 20, height = 10):
        super().__init__(width, height)
        self.make_maze()
        self.map = self.create_matrix()
        self.placePlayer()
        self.render = self.colorMaze()

    def colorMaze(self):
        colorDict = {
            '#': '\033[47m \033[0m',
            Player: '\033[32m@\033[0m',
            '.': ' ',
        }
        render = self.map.copy()
        for i, row in enumerate(render):
            for j, element in enumerate(row):
                self.map[i][j] = colorDict[element]
        return render

    def placePlayer(self):
        #list all the path that is surrounded by 3 walls
        possiblePath = []
        for i, row in enumerate(self.map):
            for j, element in enumerate(row):
                if element == ".":
                    walls = 0
                    direction = ((1, 0), (-1, 0), (0, 1), (0, -1))
                    for dir in direction:
                        if self.map[i + dir[0]][j + dir[1]] == "#":
                            walls += 1
                    if walls == 3:
                        possiblePath.append((i, j))

        coord = random.choice(possiblePath)
        self.map[coord[0]][coord[1]] = Player

    def __str__(self):
        map = []
        for row in self.render:
            map.append(''.join(row))
        return '\n'.join(map)


class Lobby(Room):
    def __init__(self):
        self.map = []
        self.createRoom()
        self.placePlayer()
        self.render = self.colorMaze()

    def createRoom(self):
        self.map.append(["#" for i in range(41)])
        for i in range(19):
            self.map.append(["#"] + ["." for i in range(39)] + ["#"])
        self.map.append(["#" for i in range(41)])
    
    def placePlayer(self):
        #place player in the middle of the lobby
        self.map[10][20] = "@"


maze = Room()
print(maze)