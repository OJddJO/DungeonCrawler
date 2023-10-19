import keyboard
import os
import random
from time import sleep
from classes.Map import Lobby, Portal
from classes.Player import Player

def clear():
    # for windows
    if os.name == 'nt':
        os.system('cls')
    # for mac and ²
    else:
        os.system('clear')


def keyPress(key):
    """return True if the key is pressed and wait for the key to be released"""
    if keyboard.is_pressed(key):
        while keyboard.is_pressed(key): pass
        return True
    return False


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
        clear()
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
        clear()
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


class Fight:
    def __init__(self, player, enemy, maxTurn):
        self.player = player
        self.enemy = enemy
        self.maxTurn = maxTurn

    def turn(self):
        #player turn
        if self.player.health > 0:
            self.playerTurn()
        else:
            pass
        #enemy turn
        if self.enemy.health > 0:
            pass
        else:
            pass

    def playerTurn(self):
        #player choose an action
        #attack skill item
        print("Choose an action:")
        print("1. Attack    2. Skill    3. Item")
        getInput = True
        while getInput:
            if keyPress('1'):
                key = '1'
                getInput = False
            elif keyPress('2'):
                key = '2'
                getInput = False
            elif keyPress('3'):
                key = '3'
                getInput = False
        #attack
        if key == '1':
            baseAtk = self.player.weapon.baseDamage
            atk = baseAtk + random.randint(-baseAtk // 5, baseAtk // 5)
            self.enemy.health -= atk
            print("You deal", atk, "damage")
        #skill
        elif key == '2':
            pass
        #item
        elif key == '3':
            pass
        #press any key to continue
        print("Press \033[1m˽\033[0m to continue")
        wait = True
        while wait:
            if keyPress('space'):
                wait = False

    def endFight(self):
        if self.enemy.health <= 0 or self.player.health <= 0:
            return True
        else:
            return False

    def endMessage(self):
        if self.player.health > 0:
            print("You win")
            print("You gain", self.enemy.exp, "exp")
        else:
            print("You lose")

    def run(self):
        turn = 0
        while turn < self.maxTurn:
            self.turn()
            turn += 1