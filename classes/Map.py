import random
from classes.Maze import Maze
from classes.Player import Player

class Dungeon:
    def __init__(self, difficulty = 1):
        self.rooms = []
        self.difficulty = difficulty
        self.floor = 0 #index of the current room

    def addRoom(self, room):
        self.rooms.append(room)

    def makeDungeon(self, nbRoom = random.randint(2, 5)):
        nbRoom *= self.difficulty
        self.addRoom(Room(difficulty=self.difficulty, nextRoom=None))
        for i in range(nbRoom-1):
            self.addRoom(Room(difficulty=self.difficulty, nextRoom=self.rooms[-1]))
        self.rooms.reverse()

class Room(Maze):
    def __init__(self, difficulty, nextRoom, width = 30, height = 10):
        super().__init__(width, height)
        self.difficulty = difficulty
        self.make_maze()
        self.map = self.create_matrix()
        self.placePlayer()
        self.placePortal(nextRoom)
        self.render = self.colorMap()

    def colorMap(self, mist = True): #color the map for printing
        # mist = False #testing
        colorDict = {
            '#': '\033[47m \033[0m',
            '.': '\033[30m.\033[0m',
            Player: '\033[1;32m@\033[0m',
            Portal: '\033[1;33mO\033[0m',
        }
        render = []
        for i, row in enumerate(self.map):
            render.append([])
            for j, element in enumerate(row):
                if mist:
                    render[i].append('\033[40m \033[0m')
                else:
                    if type(element) == str:
                        render[i].append(colorDict[element])
                    else:
                        render[i].append(colorDict[type(element)])
        if mist:
            coord = self.getPlayerCoord()
            #arround the player in a square of 5x5 use colorDict
            for i in range(coord[0] - 4, coord[0] + 5):
                for j in range(coord[1] - 4, coord[1] + 5):
                    #test if the coord is in the map
                    if i >= 0 and i < len(self.map) and j >= 0 and j < len(self.map[0]):
                        if type(self.map[i][j]) == str:
                            render[i][j] = colorDict[self.map[i][j]]
                        else:
                            render[i][j] = colorDict[type(self.map[i][j])]
        return render

    def getPlayerCoord(self): #get the coord of the player in the map
        for i, row in enumerate(self.map):
            for j, element in enumerate(row):
                if type(element) == Player:
                    return (i, j)
                
    def get3Walls(self):
        #list all the path that is surrounded by 3 walls
        paths = []
        for i, row in enumerate(self.map):
            for j, element in enumerate(row):
                if element == ".":
                    walls = 0
                    direction = ((1, 0), (-1, 0), (0, 1), (0, -1))
                    for dir in direction:
                        if self.map[i + dir[0]][j + dir[1]] == "#":
                            walls += 1
                    if walls == 3:
                        paths.append((i, j))
        return paths

    def placePortal(self, room):
        possiblePath = self.get3Walls()
        coord = random.choice(possiblePath)
        self.portal = Portal(self, room)
        self.map[coord[0]][coord[1]] = Portal(self, room)

    def placePlayer(self):
        possiblePath = self.get3Walls()
        coord = random.choice(possiblePath)
        self.map[coord[0]][coord[1]] = Player() #place player to render the room, it will be replaced by the game player to get all data about the player

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
        self.dungeon = Dungeon() #init dungeon in lobby for changing rooms
        self.dungeon.makeDungeon() # dungeon will be reset when the player goes back to the lobby
        self.placePortal()
        self.render = self.colorMap(mist = False) # all the lobby is always visible

    def createRoom(self):
        self.map.append(["#" for i in range(61)])
        for i in range(19):
            self.map.append(["#"] + ["." for i in range(59)] + ["#"])
        self.map.append(["#" for i in range(61)])

    def placePlayer(self):
        #place player in the middle of the lobby
        self.map[10][30] = Player() #place player to render the room, it will be replaced by the game player to get all data about the player

    def placePortal(self):
        #place portal on the top middle of the lobby
        self.map[1][30] = Portal(self, self.dungeon.rooms[0])

class Portal:
    def __init__(self, room1, room2):
        self.room1 = room1
        self.room2 = room2