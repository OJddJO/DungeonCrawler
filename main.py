import random
import os
import keyboard
from time import sleep
from maze import Maze

class Player:
    def __init__(self, weapon = None, armor = None):
        self.health = 100
        self.mana = 100
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
    def __init__(self, difficulty, nextRoom, width = 30, height = 10):
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


class Game:
    separator = "─" * 61
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
        adjList = self.getElementAroundPlayer()
        for element in adjList:
            if type(element) == Portal:
                if type(self.currentRoom) == Lobby:
                    self.currentRoom = self.currentRoom.dungeon.rooms[0]
                else:
                    if self.currentRoom.portal.room2 == None: #if there is no next room -> last room of the dungeon, go back to lobby
                        #go to lobby
                        self.currentRoom = self.lobby
                        self.player.health = 100 #reset player health
                        #regenerate dungeon that is initialized in the lobby
                        self.lobby.dungeon.makeDungeon()
                        self.lobby.placePortal() #replace portal in lobby to link to the new dungeon
                    else: #if there is a next room -> go to next room
                        self.currentRoom = self.currentRoom.portal.room2
                        self.lobby.dungeon.floor += 1
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
                    print("\033[3mInfo:\033[0m Press \033[1m˽\033[0m to start a \033[1;35mdungeon\033[0m")
                else:
                    if self.currentRoom.portal.room2 == None:
                        print("\033[3mInfo:\033[0m Press \033[1m˽\033[0m to go back to the \033[32mlobby\033[0m")
                    else:
                        print("\033[3mInfo:\033[0m Press \033[1m˽\033[0m to go to the next \033[1;35mroom\033[0m")
                print(self.separator)

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

    def bar(self, current, maximum, length = 20): #print a bar with current/max
        bar = "■" * (current // (maximum // length))
        bar += " " * (length - current // (maximum // length))
        bar = f'[{bar}]'
        return bar

    def printRoom(self): #print the room and all infos -> called after every player action
        os.system('cls')
        print(self.separator)
        #print current room name
        print("\033[1mCurrent room:\033[0m ", end="")
        if type(self.currentRoom) == Lobby:
            print("\033[32mLobby\033[0m")
        else:
            print("\033[1;35mDungeon: Floor", self.lobby.dungeon.floor, "of", len(self.lobby.dungeon.rooms) - 1, "\033[0m")
        print(self.separator)
        if self.currentRoom == self.lobby:
            mist = False
        else:
            mist = True
        self.currentRoom.render = self.currentRoom.colorMap(mist=mist)

        print(self.currentRoom)

        print(self.separator)
        #print player info
        healthText = f'Health: {self.player.health}/100'
        manaText = f'Mana: {self.player.mana}/100'
        whiteSpace = " " * (61 - len(healthText) - len(manaText))
        print(f'\033[31m{healthText}\033[0m{whiteSpace}\033[36m{manaText}\033[0m')
        healthBar = self.bar(self.player.health, 100)
        manaBar = self.bar(self.player.mana, 100)
        whiteSpace = " " * (61 - len(healthBar) - len(manaBar))
        print(f'\033[31m{healthBar}\033[0m{whiteSpace}\033[36m{manaBar}\033[0m')
        print(self.separator)

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
            if keyboard.is_pressed('down'):
                self.playerMove('down')
            if keyboard.is_pressed('left'):
                self.playerMove('left')
            if keyboard.is_pressed('right'):
                self.playerMove('right')
            if keyboard.is_pressed('space'):
                self.playerInteraction()


class Menu:
    separator = "─" * 61
    def __init__(self):
        self.title = open("ascii/title.txt", "r").read()
        self.option = ["New Game", "Continue", "Quit"]
        self.select = 0

    def printMenu(self):
        os.system('cls')
        print('\033[1m' + self.title + '\033[0m')
        print(self.separator)
        #selected option will in green
        for i, option in enumerate(self.option):
            if i == self.select:
                print(f"\033[1;32m> {option}\033[0m")
            else:
                print(option)

    def selectOption(self):
        getInput = True
        key = None
        while getInput:
            if keyboard.is_pressed('up'):
                key = 'up'
                self.select -= 1
                if self.select < 0:
                    self.select = len(self.option) - 1
            elif keyboard.is_pressed('down'):
                key = 'down'
                self.select += 1
                if self.select > len(self.option) - 1:
                    self.select = 0
            elif keyboard.is_pressed('space'):
                key = 'space'
                match self.select:
                    case 0:
                        game = Game()
                        game.run()
                    case 1:
                        pass
                    case 2:
                        exit()
            if key != None:
                while keyboard.is_pressed(key): pass
                getInput = False

    def run(self):
        run = True
        while run:
            self.printMenu()
            self.selectOption()


if __name__ == "__main__":
    mainMenu = Menu()
    mainMenu.run()