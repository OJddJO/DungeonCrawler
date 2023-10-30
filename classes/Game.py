import keyboard
import os
import json
import random
from datetime import datetime
from time import sleep
from classes.Map import Lobby, Portal
from classes.Player import Player
from classes.Enemy import Enemy
from classes.Item import Treasure, Weapon, Armor

os.makedirs("save", exist_ok=True)
if os.path.exists("save/keybind.json"):
    with open("save/keybind.json", "r") as f:
        keybind = json.load(f)
else:
    keybind = {
        "up": "up",
        "down": "down",
        "left": "left",
        "right": "right"
    }
    with open("save/keybind.json", "w") as f:
        json.dump(keybind, f)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def keyPress(key):
    """return True if the key is pressed and wait for the key to be released"""
    if keyboard.is_pressed(key):
        while keyboard.is_pressed(key): pass
        return True
    return False

def bar(current, maximum, reversed = False, length = 20): #print a bar with current/max
    bar = "■" * (current // (maximum // length))
    bar += " " * (length - current // (maximum // length))
    if reversed:
        bar = bar[::-1]
    bar = f'[{bar}]'
    return bar

def spaceToContinue():
    print("Press \033[1m˽\033[0m to continue")
    wait = True
    while wait:
        if keyPress('space'):
            wait = False

separator = "─" * 61

class Menu:
    def __init__(self, title, option, onSpace):
        self.title = title
        self.option = option
        self.select = 0
        self.onSpace = onSpace
        self.runVar = True

    def printMenu(self):
        clear()
        print('\033[1m' + self.title + '\033[0m')
        print(separator)
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
            if keyPress(keybind['up']):
                key = keybind['up']
                self.select -= 1
                if self.select < 0:
                    self.select = len(self.option) - 1
            elif keyPress(keybind['down']):
                key = keybind['down']
                self.select += 1
                if self.select > len(self.option) - 1:
                    self.select = 0
            elif keyPress('space'):
                key = 'space'
                getInput = False
                self.onSpace(self.select)
            if key != None:
                getInput = False

    def run(self):
        while self.runVar:
            self.printMenu()
            self.selectOption()

class MainMenu(Menu):
    def __init__(self):
        title = open("ascii/title", "r").read()
        options = ("Play", "Continue", "Options", "How to play", "Exit")
        super().__init__(title, options, self.onSpace)

    def onSpace(self, select):
        match select:
            case 0:
                if os.path.exists("save/stats.json"):
                    print(separator)
                    print("\033[1;31mWARNING\033[0m: You will overwrite your save file")
                    print("\033[1mAre you sure you want to start a new game ?\033[0m")
                    print("1. Yes    2. No")
                    getInput = True
                    while getInput:
                        if keyPress('1'):
                            getInput = False
                            Game().run()
                        elif keyPress('2'):
                            getInput = False
                else:
                    Game().run()
            case 1:
                try:
                    if os.path.exists("save"):
                        Game(new=False).run()
                    else:
                        print(separator)
                        print("No save file found")
                        spaceToContinue()
                except Exception as e:
                    print(separator)
                    print("An error occurred while loading the save file")
                    print(e)
                    spaceToContinue()
            case 2:
                OptionMenu().run()
            case 3:
                HelpMenu().run()
            case 4:
                exit()


class HelpMenu(Menu):
    def __init__(self):
        title = open("ascii/help", "r").read()
        options = ("Map", "Save", "Back")
        super().__init__(title, options, self.onSpace)

    def onSpace(self, select):
        match select:
            case 0:
                text = """There are different object on the map:
-   \033[1;32m@\033[0m : This is you. You can move using the arrows or the keys you defined.
-   \033[30m.\033[0m : This is a path. The player can move on the path.
-   \033[47m \033[0m : This is a wall. The player can't move on the wall.
-   \033[1;33mO\033[0m : This is a portal. If the player is around it, he can interact with it.
-   \033[1;31mM\033[0m : This is an enemy. If the player is around him, he can fight with him.
-   \033[1;34m$\033[0m : This is a treasure. If the player is around it, he can pick it up."""
                self.renderText(text)
            case 1:
                text = """To save in the game, just exit the game and it will save automatically.
You can exit the game using the menu that appears when you press the ESC key."""
                self.renderText(text)
            case 2:
                self.runVar = False

    def renderText(self, text):
        print(separator)
        lines = text.split("\n")
        for line in lines:
            if len(line) > 61:
                print(line[:61])
                print(line[61:])
            else:
                print(line)
        print(separator)
        spaceToContinue()


class OptionMenu(Menu):
    def __init__(self):
        title = open("ascii/options", "r").read()
        options = ("Keybind", "Back")
        super().__init__(title, options, self.onSpace)

    def onSpace(self, select):
        match select:
            case 0:
                KeybindMenu().run()
            case 1:
                self.runVar = False


class KeybindMenu(Menu):
    def __init__(self):
        title = open("ascii/keybind", "r").read()
        options = [f"Up: [{keybind['up']}]", f"Down: [{keybind['down']}]", f"Left: [{keybind['left']}]", f"Right: [{keybind['right']}]", "Back"]
        super().__init__(title, options, self.onSpace)

    def redifineOptionsName(self):
        global keybind
        self.option[0] = f"Up: [{keybind['up']}]"
        self.option[1] = f"Down: [{keybind['down']}]"
        self.option[2] = f"Left: [{keybind['left']}]"
        self.option[3] = f"Right: [{keybind['right']}]"

    def replaceKey(self, key):
        clear()
        print("Press the key you want to replace", key, "with")
        print("Press \033[1m˽\033[0m to cancel")
        inputKey = keyboard.read_key()
        while keyboard.is_pressed(inputKey): pass
        if inputKey == 'space':
            return key
        else:
            return inputKey

    def onSpace(self, select):
        global keybind
        match select:
            case 0:
                keybind['up'] = self.replaceKey(keybind['up'])
            case 1:
                keybind['down'] = self.replaceKey(keybind['down'])
            case 2:
                keybind['left'] = self.replaceKey(keybind['left'])
            case 3:
                keybind['right'] = self.replaceKey(keybind['right'])
            case 4:
                with open("save/keybind.json", "w") as f:
                    json.dump(keybind, f)
                self.runVar = False
        self.redifineOptionsName()


class PauseMenu(Menu):
    def __init__(self, game):
        title = open("ascii/pause", "r").read()
        options = ("Resume", "Save", "Options", "Main Menu", "Exit")
        super().__init__(title, options, self.onSpace)
        self.game = game
    
    def onSpace(self, select):
        match select:
            case 0:
                self.runVar = False
            case 1:
                self.game.save()
                print(separator)
                print("Game saved")
                spaceToContinue()
                self.runVar = False
            case 2:
                OptionMenu().run()
            case 3:
                self.game.save()
                MainMenu().run()
            case 4:
                print(separator)
                print("\033[1;31mWARNING\033[0m: Be sure to save your game before exiting")
                print("\033[1mAre you sure you want to exit ?\033[0m")
                print("1. Yes    2. No")
                getInput = True
                while getInput:
                    if keyPress('1'):
                        getInput = False
                        exit()
                    elif keyPress('2'):
                        getInput = False


class Game:
    separator = "─" * 61
    def __init__(self, new = True): #new = True if the player start a new game
        if new:
            self.player = Player()
            self.save()
        else:
            self.player = Player()
            self.player.loadData()
            #time verification
            statsFileTime = datetime.fromtimestamp(os.path.getmtime("save/stats.json"))
            inventoryFileTime = datetime.fromtimestamp(os.path.getmtime("save/inventory.json"))
            savedTime = json.load(open("save/stats.json", "r"))["date"]
            if statsFileTime.strftime("%d/%m/%Y-%H:%M:%S") != savedTime or inventoryFileTime.strftime("%d/%m/%Y-%H:%M:%S") != savedTime:
                raise Exception("Save file corrupted/modified")
            self.player.inventory.loadData()
        self.lobby = Lobby(self.player)
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
        adjList = self.getElementAroundPlayer()
        for element in adjList:
            if type(element) == Portal: #if there is a portal go to next room
                if type(self.currentRoom) == Lobby:
                    self.currentRoom = self.currentRoom.dungeon.rooms[0]
                else:
                    if self.currentRoom.portal.room2 == None: #if there is no next room -> last room of the dungeon, go back to lobby
                        #go to lobby
                        self.currentRoom = self.lobby
                        self.player.health = 100 #reset player health
                        #regenerate dungeon that is initialized in the lobby
                        self.lobby.dungeon.makeDungeon(self.player.level)
                        self.lobby.placePortal() #replace portal in lobby to link to the new dungeon
                    else: #if there is a next room -> go to next room
                        self.currentRoom = self.currentRoom.portal.room2
                        self.lobby.dungeon.floor += 1
            elif type(element) == Treasure: #if there is a treasure open it
                item = element.randomLoot()
                money = element.gold
                if type(item) in (Weapon, Armor):
                    self.player.inventory.addGear(item)
                else:
                    self.player.inventory.addItem(item)
                self.player.inventory.addGold(money)
                color = {
                    1: "\033[1;37mCommon",
                    2: "\033[1;36mUncommon",
                    3: "\033[1;34mRare",
                    4: "\033[1;35mEpic",
                    5: "\033[1;33mLegendary",
                    6: "\033[1;31mMythic"
                }
                print(f"You found '{color[item.rarity]} {item.name}\033[0m' and \033[33m{money} gold\033[0m in the treasure")
                self.currentRoom.map[element.coord[0]][element.coord[1]] = '.'
                self.save()
                spaceToContinue()
            elif type(element) == Enemy: #if there is an enemy fight it
                fight = Fight(self.player, element)
                runFight = True
                fight.print()
                while runFight:
                    runFight = not fight.turn() #if the fight is not over, runFight = True -> see Fight.turn() -> Fight.endFight()
                    fight.print()
                win = fight.endMessage()
                if win == "flee":
                    print("\033[3mInfo:\033[0m You flee the fight")
                elif win == True:
                    self.currentRoom.map[element.coord[0]][element.coord[1]] = '.'
                    print("\033[3mInfo:\033[0m You win the fight")
                    print(f"      You gain {element.exp} exp")
                    self.player.exp += element.exp
                    if self.player.exp >= 5**(self.player.level*2)*10:
                        self.player.exp = 0
                        self.player.level += 1
                        print("      You level up")
                        print("      You are now level", self.player.level)
                else:
                    self.currentRoom = self.lobby
                    self.player.health = 100
                    self.lobby.dungeon.makeDungeon(self.player.level)
                    self.lobby.placePortal()
                    print("\033[3mInfo:\033[0m You died, you will be teleported back to the \033[32mlobby\033[0m")
                    print("      You lose all your exp and level")
                    self.player.exp = 0
                    self.player.level = 1
                self.save()
                print(separator)
                spaceToContinue()
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
                print(separator)
            elif type(element) == Enemy:
                print(f"\033[3mInfo:\033[0m You encounter \033[3;31m{element.name}\033[0m.\n      Press \033[1m˽\033[0m to start the \033[31mfight\033[0m")
                print(separator)
            elif type(element) == Treasure:
                print("\033[3mInfo:\033[0m Press \033[1m˽\033[0m to open the \033[33mtreasure\033[0m")
                print(separator)

    def playerMove(self, direction): #player movement handler
        coord = self.currentRoom.getPlayerCoord()
        match direction:
            case'up':
                if self.currentRoom.map[coord[0] - 1][coord[1]] == '.':
                    self.currentRoom.map[coord[0]][coord[1]] = '.'
                    self.currentRoom.map[coord[0] - 1][coord[1]] = self.player
            case 'down':
                if self.currentRoom.map[coord[0] + 1][coord[1]] == '.':
                    self.currentRoom.map[coord[0]][coord[1]] = '.'
                    self.currentRoom.map[coord[0] + 1][coord[1]] = self.player
            case 'left':
                if self.currentRoom.map[coord[0]][coord[1] - 1] == '.':
                    self.currentRoom.map[coord[0]][coord[1]] = '.'
                    self.currentRoom.map[coord[0]][coord[1] - 1] = self.player
            case 'right':
                if self.currentRoom.map[coord[0]][coord[1] + 1] == '.':
                    self.currentRoom.map[coord[0]][coord[1]] = '.'
                    self.currentRoom.map[coord[0]][coord[1] + 1] = self.player

        # while keyboard.is_pressed(direction): #wait for the key to be released
        #     pass

        sleep(0.1) #delay to avoid multiple key press
        self.printRoom()

    def printRoom(self): #print the room and all infos -> called after every player action
        clear()
        print(separator)
        #print current room name
        print("\033[1mCurrent room:\033[0m ", end="")
        if type(self.currentRoom) == Lobby:
            print("\033[32mLobby\033[0m")
        else:
            print("\033[1;35mDungeon: Floor", self.lobby.dungeon.floor, "of", len(self.lobby.dungeon.rooms) - 1, "\033[0m")
        print(separator)
        if self.currentRoom == self.lobby:
            mist = False
        else:
            mist = True
        self.currentRoom.render = self.currentRoom.colorMap(mist=mist)

        print(self.currentRoom)

        print(separator)
        #print player info
        healthText = f'Health: {self.player.health}/100'
        manaText = f'Mana: {self.player.mana}/100'
        whiteSpace = " " * (61 - len(healthText) - len(manaText))
        print(f'\033[31m{healthText}\033[0m{whiteSpace}\033[36m{manaText}\033[0m')
        healthBar = bar(self.player.health, 100)
        manaBar = bar(self.player.mana, 100, reversed=True)
        whiteSpace = " " * (61 - len(healthBar) - len(manaBar))
        print(f'\033[31m{healthBar}\033[0m{whiteSpace}\033[36m{manaBar}\033[0m')
        expText = f'Exp: {self.player.exp}/{(self.player.level*10)**2}'
        levelText = f'Level: {self.player.level}'
        whiteSpace = " " * (61 - len(expText) - len(levelText))
        print(f'\033[33m{expText}\033[0m{whiteSpace}\033[33m{levelText}\033[0m')
        expBar = bar(self.player.exp, (self.player.level*10)**2, length=59)
        print(f'\033[33m{expBar}\033[0m')
        print(separator)

        self.interactionInfo()

    def save(self):
        with open("save/stats.json", "w") as f:
            json.dump({
                "health": self.player.health,
                "mana": self.player.mana,
                "exp": self.player.exp,
                "level": self.player.level,
                "role": self.player.role,
                "weapon": self.player.weapon.__dict__(),
                "armor": self.player.armor.__dict__(),
                "date": datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
            }, f)
        self.player.inventory.save()

    def run(self):
        run = True
        self.printRoom()
        while run:
            #get input from the player and manage it
            #all modification of the map are done in the playerMove function and the playerInteraction function
            #the room is also printed in those functions
            if keyboard.is_pressed(keybind['up']):
                self.playerMove('up')
            if keyboard.is_pressed(keybind['down']):
                self.playerMove('down')
            if keyboard.is_pressed(keybind['left']):
                self.playerMove('left')
            if keyboard.is_pressed(keybind['right']):
                self.playerMove('right')
            if keyPress('space'):
                self.playerInteraction()
            if keyPress('esc'):
                PauseMenu(self).run()


class Fight:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.flee = False

    def turn(self):
        #player turn
        if self.player.health > 0:
            self.playerTurn()
        #enemy turn
        if self.enemy.health > 0:
            self.enemyTurn()
        if self.flee:
            return True
        return self.endFight()

    def enemyTurn(self):
        print(f"{self.enemy.name}'s turn")
        randomAction = random.randint(1, 2)
        if randomAction == 1:
            print(f"{self.enemy.name} attacks you !")
            baseAtk = self.enemy.weapon.onUse()
            atk = baseAtk + random.randint(-baseAtk // 5, baseAtk // 5) - self.player.armor.onUse()
            self.player.health -= atk
            print("He deals", atk, "damage")
        elif randomAction == 2:
            print(f"{self.enemy.name} uses a skill")
            pass
        # elif randomAction == 3:
        #     print(f"{self.enemy.name} uses an item")
        #     pass
        spaceToContinue()

    def playerTurn(self):
        #player choose an action
        #attack skill item
        print("Choose an action:")
        print("1. Attack    2. Skill    3. Item    4. Run")
        getInput = True
        while getInput:
            if keyPress('1'): #attack
                baseAtk = self.player.weapon.onUse()
                atk = baseAtk + random.randint(-baseAtk // 5, baseAtk // 5) - self.enemy.armor.onUse()
                self.enemy.health -= atk
                print("You deal", atk, "damage")
                getInput = False
            elif keyPress('2'): #skill
                getInput = False
            elif keyPress('3'): #item
                getInput = False
            elif keyPress('4'): #run
                print("You try to flee")
                flee = random.randint(1, 2)
                if flee == 1:
                    print("You successfully flee")
                    self.flee = True
                else:
                    print("You failed to flee")
                getInput = False

    def endFight(self):
        if self.enemy.health <= 0 or self.player.health <= 0:
            return True
        else:
            return False

    def endMessage(self): #return True if the player win else False
        win = False
        if self.player.health > 0:
            win = True
        if self.flee:
            win = "flee"
        return win
    
    def print(self):
        clear()
        #print enemy info
        print(f"\033[1m{self.enemy.name} - {self.enemy.type}:\033[0m")
        healthText = f'Health: {self.enemy.health}/100'
        print(f'\033[31m{healthText}\033[0m')
        healthBar = bar(self.enemy.health, 100)
        print(f'\033[31m{healthBar}\033[0m')
        self.enemy.render()
        #print player info
        print("\033[1mYou:\033[0m")
        healthText = f'Health: {self.player.health}/100'
        manaText = f'Mana: {self.player.mana}/100'
        whiteSpace = " " * (61 - len(healthText) - len(manaText))
        print(f'\033[31m{healthText}\033[0m{whiteSpace}\033[36m{manaText}\033[0m')
        healthBar = bar(self.player.health, 100)
        manaBar = bar(self.player.mana, 100, reversed=True)
        whiteSpace = " " * (61 - len(healthBar) - len(manaBar))
        print(f'\033[31m{healthBar}\033[0m{whiteSpace}\033[36m{manaBar}\033[0m')
        print(separator)
