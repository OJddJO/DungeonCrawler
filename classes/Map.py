import random
from classes.Maze import Maze
from classes.Player import Player
from classes.Enemy import Enemy
from classes.Item import Treasure

class Dungeon:
    def __init__(self, player):
        self.rooms = []
        self.player = player
        self.floor = 0 #index of the current room

    def addRoom(self, room):
        self.rooms.append(room)

    def makeDungeon(self, difficulty, nbRoom = random.randint(2, 5)):
        nbRoom *= difficulty
        self.addRoom(Room(player=self.player, difficulty=difficulty, nextRoom=None))
        for i in range(nbRoom-1):
            self.addRoom(Room(player=self.player, difficulty=difficulty, nextRoom=self.rooms[-1]))
        self.rooms.reverse() # first room is the last room of the list


class Room(Maze):
    def __init__(self, player, difficulty, nextRoom, width = 30, height = 10):
        super().__init__(width, height)
        self.player = player
        self.difficulty = difficulty
        self.make_maze()
        self.map = self.create_matrix()
        self.placePlayer()
        self.placePortal(nextRoom)
        self.placeTreasure()
        self.placeEnemies()
        self.render = self.colorMap()

    def colorMap(self, mist = True): #color the map for printing
        mist = False #testing
        colorDict = {
            '#': '\033[47m \033[0m',
            '.': '\033[30m.\033[0m',
            Player: '\033[1;32m@\033[0m',
            Portal: '\033[1;33mO\033[0m',
            Enemy: '\033[1;31mM\033[0m',
            Treasure: '\033[1;34m$\033[0m'
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
        self.map[coord[0]][coord[1]] = self.portal
        self.portalCoord = coord

    def placePlayer(self):
        possiblePath = self.get3Walls()
        coord = random.choice(possiblePath)
        self.map[coord[0]][coord[1]] = self.player

    def placeTreasure(self):
        self.treasurePos = []
        allowedPath = self.get3Walls()
        random.shuffle(allowedPath)
        nbTreasure = int(random.randint(5, 10) * self.difficulty / 2)
        if nbTreasure > len(allowedPath):
            nbTreasure = len(allowedPath)
        for i in range(nbTreasure):
            pos = random.choice(allowedPath)
            self.map[pos[0]][pos[1]] = Treasure(self.player.role, self.difficulty, pos)
            self.treasurePos.append(pos)

    def placeEnemies(self):
        allowedPath = self.get3Walls()
        enemyType = ["bat", "demon", "ghost", "imp", "mushroom", "spider"]
        random.shuffle(allowedPath)
        nbEnemies = random.randint(5, 10) * self.difficulty
        if nbEnemies < len(self.treasurePos):
            nbEnemies = len(self.treasurePos)
        if nbEnemies > len(allowedPath):
            nbEnemies = len(allowedPath)
        # place an enemy around portal
        direction = ((1, 0), (-1, 0), (0, 1), (0, -1))
        for dir in direction:
            if self.map[self.portalCoord[0] + dir[0]][self.portalCoord[1] + dir[1]] == ".":
                self.map[self.portalCoord[0] + dir[0]][self.portalCoord[1] + dir[1]] = Enemy("Portal Guardian", random.choice(enemyType), self.difficulty, (self.portalCoord[0] + dir[0], self.portalCoord[1] + dir[1]))
        for pos in self.treasurePos:
            direction = ((1, 0), (-1, 0), (0, 1), (0, -1))
            for dir in direction:
                if self.map[pos[0] + dir[0]][pos[1] + dir[1]] == ".":
                    self.map[pos[0] + dir[0]][pos[1] + dir[1]] = Enemy("Treasure Guardian", random.choice(enemyType), self.difficulty, (pos[0] + dir[0], pos[1] + dir[1]))
        for i in range(nbEnemies-1):
            direction = ((1, 0), (-1, 0), (0, 1), (0, -1))
            pos = random.choice(allowedPath)
            enemyPlaced = False
            for dir in direction:
                if self.map[pos[0] + dir[0]][pos[1] + dir[1]] == ".":
                    self.map[pos[0] + dir[0]][pos[1] + dir[1]] = Enemy("Enemy", random.choice(enemyType), self.difficulty, (pos[0] + dir[0], pos[1] + dir[1]))
                    enemyPlaced = True
            if not enemyPlaced:
                i -= 1

    def __str__(self):
        map = []
        for row in self.render:
            map.append(''.join(row))
        return '\n'.join(map)


class Lobby(Room):
    def __init__(self, player):
        self.map = []
        self.player = player
        self.createRoom()
        self.placePlayer()
        self.dungeon = Dungeon(self.player) #init dungeon in lobby for changing rooms
        self.dungeon.makeDungeon(self.player.level) # dungeon will be reset when the player goes back to the lobby
        self.placePortal()
        self.render = self.colorMap(mist = False) # all the lobby is always visible

    def createRoom(self):
        self.map.append(["#" for i in range(61)])
        for i in range(19):
            self.map.append(["#"] + ["." for i in range(59)] + ["#"])
        self.map.append(["#" for i in range(61)])

    def placePlayer(self):
        #place player in the middle of the lobby
        self.map[10][30] = self.player

    def placePortal(self):
        #place portal on the top middle of the lobby
        self.map[1][30] = Portal(self, self.dungeon.rooms[0])

class Portal:
    def __init__(self, room1, room2):
        self.room1 = room1
        self.room2 = room2