import random
from classes.Maze import Maze
from classes.Player import Player
from classes.Enemy import Enemy
from classes.Item import Treasure

class Dungeon:
    """Dungeon class, contains a list of rooms and the player"""
    def __init__(self, player):
        """Constructor for the Dungeon class, takes in a player"""
        self.rooms = []
        self.player = player
        self.floor = 0 #index of the current room

    def addRoom(self, room):
        """Adds a room to the dungeon"""
        self.rooms.append(room)

    def makeDungeon(self, difficulty):
        """Makes a dungeon depending on the difficulty"""
        nbRoom = random.randint(1, 3) * difficulty
        self.addRoom(Room(player=self.player, difficulty=difficulty, nextRoom=None))
        for i in range(nbRoom-1):
            self.addRoom(Room(player=self.player, difficulty=difficulty, nextRoom=self.rooms[-1]))
        self.rooms.reverse() # first room is the last room of the list


class Room(Maze):
    """Room class for the dungeon"""
    def __init__(self, player, difficulty, nextRoom, width = 60, height = 20):
        """Constructor for the Room class, takes in a player, a difficulty, the next room and the width and height of the room"""
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

    def colorMap(self, mist = True):
        """Returns a matrix of a colored map of the room"""
        # mist = False #testing
        colorDict = { # (char to print, color pair for curses)
            '#': (" ", 1),
            '.': (" ", 7),
            'C': ("C", 2),
            'G': ("G", 3),
            'S': ("S", 2),
            Player: ("@", 5),
            Portal: ("O", 6),
            Enemy: ("M", 4),
            Treasure: ("$", 2)
        }
        render = []
        for i, row in enumerate(self.map):
            render.append([])
            for j, element in enumerate(row):
                if mist:
                    render[i].append((" ", 8))
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

    def getPlayerCoord(self): 
        """Returns the coord of the player in the map"""
        for i, row in enumerate(self.map):
            for j, element in enumerate(row):
                if type(element) == Player:
                    return (i, j)
                
    def get3Walls(self):
        """Returns a list of all the paths that is surrounded by 3 walls"""
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
        """Places a portal in the room"""
        possiblePath = self.get3Walls()
        coord = random.choice(possiblePath)
        self.portal = Portal(self, room)
        self.map[coord[0]][coord[1]] = self.portal
        self.portalCoord = coord

    def placePlayer(self):
        """Places the player in the room"""
        possiblePath = self.get3Walls()
        coord = random.choice(possiblePath)
        self.map[coord[0]][coord[1]] = self.player

    def placeTreasure(self):
        """Places treasures in the room"""
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
        """Places enemies in the room"""
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
        """Returns a string representation of the room"""
        map = [] #map is not self.map because we don't want to modify the original map
        for row in self.render:
            map.append(''.join(row))
        return '\n'.join(map)


class Lobby(Room):
    """Lobby class, the first room of the dungeon"""
    def __init__(self, player):
        """Constructor for the Lobby class, takes in a player"""
        self.map = []
        self.player = player
        self.createRoom()
        self.placePlayer()
        self.dungeon = Dungeon(self.player) #init dungeon in lobby for changing rooms
        self.dungeon.makeDungeon(self.player.level) # dungeon will be reset when the player goes back to the lobby
        self.placePortal()
        self.placeChest()
        self.placeGrimoire()
        self.placeShop()
        self.render = self.colorMap(mist = False) # all the lobby is always visible

    def createRoom(self):
        """Creates the lobby"""
        self.map.append(["#" for i in range(121)])
        for i in range(39):
            self.map.append(["#"] + ["." for i in range(119)] + ["#"])
        self.map.append(["#" for i in range(121)])

    def placePlayer(self):
        """Places the player in the lobby"""
        self.map[21][61] = self.player

    def placePortal(self):
        """Places the portal in the lobby"""
        self.map[16][61] = Portal(self, self.dungeon.rooms[0])

    def placeChest(self):
        """Places the chest in the lobby"""
        self.map[26][61] = "C"

    def placeGrimoire(self):
        """Places the grimoire in the lobby"""
        self.map[21][51] = "G"

    def placeShop(self):
        """Places the shop in the lobby"""
        self.map[21][71] = "S"


class Portal:
    """Portal class, the portal that connects the rooms"""
    def __init__(self, room1, room2):
        """Constructor for the Portal class, takes in the two rooms that the portal connects"""
        self.room1 = room1
        self.room2 = room2