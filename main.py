import random
import os
import keyboard
from time import sleep
from maze import Maze

class Player:
    def __init__(self, weapon = None, armor = None):
        self.health = 100
        self.weapon = weapon
        self.armor = armor
        self.inventory = []

    def __str__(self):
        return '@'
    

class Enemy:
    def __init__(self, name, health, damage, armor = None):
        self.name = name
        self.health = health
        self.damage = damage
        self.armor = armor

    def __str__(self):
        return 'E'


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


class Portal:
    def __init__(self, room1, room2):
        self.room1 = room1
        self.room2 = room2

    def __str__(self):
        return 'O'


class Room(Maze):
    def __init__(self, difficulty, nextRoom, width = 20, height = 10):
        super().__init__(width, height)
        self.difficulty = difficulty
        self.make_maze()
        self.map = self.create_matrix()
        self.placePlayer()
        self.placePortal(nextRoom)
        self.render = self.colorMap()

    def colorMap(self, mist = True): #color the map for printing
        colorDict = {
            '#': '\033[47m \033[0m',
            '.': '\033[30m.\033[0m',
            Player: '\033[32m@\033[0m',
            Portal: '\033[31mO\033[0m',
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
        self.map[coord[0]][coord[1]] = Player()

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
        self.map.append(["#" for i in range(41)])
        for i in range(19):
            self.map.append(["#"] + ["." for i in range(39)] + ["#"])
        self.map.append(["#" for i in range(41)])

    def placePlayer(self):
        #place player in the middle of the lobby
        self.map[10][20] = Player()

    def placePortal(self):
        #place portal on the top middle of the lobby
        self.map[1][20] = Portal(self, self.dungeon.rooms[0])


class Game:
    def __init__(self):
        self.player = Player()
        self.lobby = Lobby()
        self.currentRoom = self.lobby #base room is the lobby

    def getElementAroundPlayer(self): #get all interactable element around the player
        #get element adjacent to the player
        coord = self.currentRoom.getPlayerCoord()
        direction = ((1, 0), (-1, 0), (0, 1), (0, -1))
        adjList = []
        for dir in direction:
            adjList.append(self.currentRoom.map[coord[0] + dir[0]][coord[1] + dir[1]])
        return adjList

    def playerInteraction(self): #player interaction handler
        #if there is a portal go to next room
        coord = self.currentRoom.getPlayerCoord()
        adjList = self.getElementAroundPlayer()
        for element in adjList:
            if type(element) == Portal:
                if type(self.currentRoom) == Lobby:
                    self.currentRoom = self.currentRoom.dungeon.rooms[0]
                else:
                    if self.currentRoom.portal.room2 == None:
                        #go to lobby
                        self.currentRoom = self.lobby
                        #regenerate dungeon
                        self.lobby.dungeon.makeDungeon()
                        self.lobby.placePortal()
                    else:
                        self.currentRoom = self.currentRoom.portal.room2
                        self.lobby.dungeon.floor += 1
            #if there is an item add it to the inventory
            elif type(element) == Item:
                self.player.inventory.append(element[Item])
                self.currentRoom.map[coord[0]][coord[1]] = '.' #remove the item from the map
            #if there is an enemy fight it
            # elif type(element) == Enemy:
            #     self.fight(element)

        while keyboard.is_pressed('space'): #wait for the key to be released
            pass
        self.printRoom()

    def interactionInfo(self): #print info about the interaction with the element around the player
        adjList = self.getElementAroundPlayer()
        for element in adjList:
            if type(element) == Portal:
                if type(self.currentRoom) == Lobby:
                    print("Info: Press space to start a dungeon")
                else:
                    if self.currentRoom.portal.room2 == None:
                        print("Info: Press space to go back to the lobby")
                    else:
                        print("Info: Press space to go to the next room")

    def playerMove(self, direction): #player movement handler
        coord = self.currentRoom.getPlayerCoord()
        if direction == 'up':
            if self.currentRoom.map[coord[0] - 1][coord[1]] == '.':
                self.currentRoom.map[coord[0]][coord[1]] = '.'
                self.currentRoom.map[coord[0] - 1][coord[1]] = self.player
        elif direction == 'down':
            if self.currentRoom.map[coord[0] + 1][coord[1]] == '.':
                self.currentRoom.map[coord[0]][coord[1]] = '.'
                self.currentRoom.map[coord[0] + 1][coord[1]] = self.player
        elif direction == 'left':
            if self.currentRoom.map[coord[0]][coord[1] - 1] == '.':
                self.currentRoom.map[coord[0]][coord[1]] = '.'
                self.currentRoom.map[coord[0]][coord[1] - 1] = self.player
        elif direction == 'right':
            if self.currentRoom.map[coord[0]][coord[1] + 1] == '.':
                self.currentRoom.map[coord[0]][coord[1]] = '.'
                self.currentRoom.map[coord[0]][coord[1] + 1] = self.player

        # while keyboard.is_pressed(direction): #wait for the key to be released
        #     pass

        sleep(0.1) #delay to avoid multiple key press
        self.printRoom()

    def printRoom(self): #print the room and all infos -> called after every player action
        os.system('cls')
        #print current room name
        print("Current room: ", end="")
        if type(self.currentRoom) == Lobby:
            print("Lobby")
        else:
            print("Dungeon: Floor", self.lobby.dungeon.floor, "of", len(self.lobby.dungeon.rooms) - 1)
        if self.currentRoom == self.lobby:
            mist = False
        else:
            mist = True
        self.currentRoom.render = self.currentRoom.colorMap(mist=mist)
        print(self.currentRoom)
        self.interactionInfo()

    def run(self):
        run = True
        self.printRoom()
        while run:
            #get input from the player and manage it
            #all modification of the map are done in the playerMove function and the playerInteraction function
            #the room is also printed in those functions
            if keyboard.is_pressed('up'):
                self.playerMove('up')
            elif keyboard.is_pressed('down'):
                self.playerMove('down')
            elif keyboard.is_pressed('left'):
                self.playerMove('left')
            elif keyboard.is_pressed('right'):
                self.playerMove('right')
            elif keyboard.is_pressed('space'):
                self.playerInteraction()


if __name__ == "__main__":
    game = Game()
    game.run()