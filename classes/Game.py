import keyboard
import os
import json
import random
from sys import exit
from datetime import datetime
from time import sleep
from classes.Map import Lobby, Portal
from classes.Player import Player
from classes.Enemy import Enemy
from classes.Item import Treasure, Weapon, Armor, HealItem, BuffItem
from classes.Spell import DamageSpell, HealSpell, BuffSpell, DebuffSpell, Tree
from cursesInit import *

# keyboard.press("f11")
refreshAll()

#load keybind from save file
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

def bar(current, maximum, reversed = False, length = 20):
    """return a bar with current/max"""
    bar = "■" * (current // (maximum // length))
    bar += " " * (length - current // (maximum // length))
    if reversed:
        bar = bar[::-1]
    bar = f'[{bar}]'
    return bar

def spaceToContinue():
    """wait for the spacebar to be pressed and released"""
    printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to continue", 9, None)])
    wait = True
    while wait:
        if keyPress('space'):
            wait = False

separator = "─" * 61
color = { #color for rarity
    1: "\033[1;37mCommon",
    2: "\033[1;36mUncommon",
    3: "\033[1;34mRare",
    4: "\033[1;35mEpic",
    5: "\033[1;33mLegendary",
    6: "\033[1;31mMythic"
}

class Menu:
    """Menu class, used to create menus"""
    def __init__(self, title, option, onSpace, addInfos=lambda:None):
        """Constructor for the Menu class, takes in title, option, onSpace, and addInfos by default a function that does nothing"""
        self.title = title
        self.option = option
        self.select = 0
        self.onSpace = onSpace
        self.addInfos = addInfos
        self.runVar = True

    def printMenu(self):
        """Prints the menu"""
        clearAll()
        for i, element in enumerate(self.title):
            printText(mainWin, i, [(element, 9, "bold")])
        self.addInfos()
        printText(mainWin, 5, [(separator, 9, None)])
        #selected option will be in green
        for i, option in enumerate(self.option):
            if i == self.select:
                printText(mainWin, i+6, [(">", 5, "bold"), (option, 5, "bold")])
            else:
                printText(mainWin, i+6, [(option, 9, None)])
        refreshAll()

    def selectOption(self):
        """Selects the option"""
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
        """Runs the menu"""
        while self.runVar:
            self.printMenu()
            self.selectOption()

class MainMenu(Menu):
    """MainMenu class, used to create the main menu"""
    def __init__(self):
        """Constructor for the MainMenu class"""
        clearAll()
        title = open("ascii/title", "r").readlines()
        options = ("New Game", "Continue", "Options", "How to play", "Exit")
        super().__init__(title, options, self.onSpace)

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                if os.path.exists("save/stats.json"):
                    clearMain()
                    printText(mainWin, 0, [("WARNING", 1, "bold"), (": You will overwrite your save file", 9, None)])
                    printText(mainWin, 1, [("Are you sure you want to start a new game ?", 9, "bold")])
                    printText(mainWin, 2, [("1. Yes    2. No", 9, None)])
                    getInput = True
                    while getInput:
                        if keyPress('1'):
                            getInput = False
                            RoleMenu().run()
                        elif keyPress('2'):
                            getInput = False
                else:
                    RoleMenu().run()
            case 1:
                try:
                    if os.path.exists("save/stats.json"):
                        Game(new=False).run()
                    else:
                        clearMain()
                        printText(mainWin, 0, [("No save file found", 9, None)])
                        spaceToContinue()
                except Exception as e:
                    printText(mainWin, 0, [("An error occurred while loading the save file", 1, None)])
                    printText(mainWin, 1, [(str(e), 1, None)])
                    spaceToContinue()
            case 2:
                OptionMenu().run()
            case 3:
                HelpMenu().run()
            case 4:
                exit()


class RoleMenu(Menu):
    """RoleMenu class, used to create the role menu"""
    def __init__(self):
        """Constructor for the RoleMenu class"""
        title = open("ascii/role", "r").readlines()
        options = ("Warrior", "Mage", "Archer", "Random", "Back")
        super().__init__(title, options, self.onSpace)

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                self.runVar = False
                Game(new = True, role="warrior").run()
            case 1:
                self.runVar = False
                Game(new = True, role="mage").run()
            case 2:
                self.runVar = False
                Game(new = True, role="archer").run()
            case 3:
                self.select = random.randint(0, 2)
            case 4:
                self.runVar = False


class HelpMenu(Menu):
    """HelpMenu class, used to create the help menu"""
    def __init__(self):
        """Constructor for the HelpMenu class"""
        clearAll()
        options = ("How to play", "Map", "Save", "Back")
        title = open("ascii/help", "r").readlines()
        super().__init__(title, options, self.onSpace)

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                text = """The goal of the game is to go through the dungeon and defeat enemies in the dungeon to get stronger.
You can move using the arrows or the keys you defined.
You can interact with the elements around you using the spacebar.
You can open the menu using the ESC key.
When your health reaches 0 or below, you die and you will be teleported back to the lobby. You will have a death penalty.
You can use skills using your mana which regenerate every action you do during a fight."""
                self.renderText(text)
            case 1:
                text = """There are different object on the map:
-   @ : This is you. You can move using the arrows or the keys you defined.
-     : This is a path. The player can move on the path.
-   O : This is a portal. If the player is around it, he can interact with it to teleport.
-   C : This is a chest. If the player is around it, he can interact with it to see what's in his inventory.  
-   G : This is a grimoire. If the player is around it, he can interact with it to see his spells.
-   S : This is a shop. If the player is around it, he can interact with it to buy items in the shop.
-   M : This is an enemy. If the player is around him, he can fight with him.
-   $ : This is a treasure. If the player is around it, he can pick it up."""
                self.renderText(text)
            case 2:
                text = """To save the game, just press ESC and there is an option to save your progression.
You can exit the game using the menu that appears when you press the ESC key."""
                self.renderText(text)
            case 3:
                self.runVar = False

    def renderText(self, text):
        """Renders the text"""
        clearMain()
        lines = text.split("\n")
        for i, line in enumerate(lines):
            printText(mainWin, i, [(line, 9, None)])
        spaceToContinue()


class OptionMenu(Menu):
    """OptionMenu class, used to create the option menu"""
    def __init__(self):
        clearAll()
        title = open("ascii/options", "r").readlines()
        options = ("Keybind", "Back")
        super().__init__(title, options, self.onSpace)

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                KeybindMenu().run()
            case 1:
                self.runVar = False


class KeybindMenu(Menu):
    """KeybindMenu class, used to create the keybind menu"""
    def __init__(self):
        clearAll()
        title = open("ascii/keybind", "r").readlines()
        options = [f"Up: [{keybind['up']}]", f"Down: [{keybind['down']}]", f"Left: [{keybind['left']}]", f"Right: [{keybind['right']}]", "Back"]
        super().__init__(title, options, self.onSpace)

    def redifineOptionsName(self):
        """Redefines the options name"""
        global keybind
        self.option[0] = f"Up: [{keybind['up']}]"
        self.option[1] = f"Down: [{keybind['down']}]"
        self.option[2] = f"Left: [{keybind['left']}]"
        self.option[3] = f"Right: [{keybind['right']}]"

    def replaceKey(self, key):
        """Replaces the key with the input key"""
        clear()
        printText(mainWin, 0, [("Press the key you want to replace", 9, None), (f" {key} ", 5, "bold"), ("with", 9, None)])
        printText(mainWin, 1, [("Press \033[1m˽\033[0m to cancel", 9, None)])
        inputKey = keyboard.read_key()
        while keyboard.is_pressed(inputKey): pass
        if inputKey == 'space':
            return key
        else:
            return inputKey

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
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
    """PauseMenu class, used to create the pause menu"""
    def __init__(self, game):
        """Constructor for the PauseMenu class, takes in game"""
        clearAll()
        title = open("ascii/pause", "r").readlines()
        options = ("Resume", "Save", "Options", "Exit")
        super().__init__(title, options, self.onSpace)
        self.game = game
    
    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                self.runVar = False
            case 1:
                self.game.save()
                printText(mainWin, 0, [("Game saved", 9, None)])
                spaceToContinue()
            case 2:
                OptionMenu().run()
            case 3:
                clearMain()
                printText(mainWin, 0, [("WARNING", 1, "bold"), (": You will lose your progression", 9, None)])
                printText(mainWin, 1, [("Are you sure you want to exit ?", 9, "bold")])
                printText(mainWin, 2, [("1. Yes    2. No", 9, None)])
                getInput = True
                while getInput:
                    if keyPress('1'):
                        getInput = False
                        exit()
                    elif keyPress('2'):
                        getInput = False

#SHOP
class Shop(Menu):
    """Shop class, used to create the shop"""
    def __init__(self, player):
        """Constructor for the Shop class, takes in player"""
        clearAll()
        self.player = player
        title = open("ascii/shop", "r").readlines()
        self.createOptions()
        super().__init__(title, self.options, self.onSpace)

    def createOptions(self):
        """Creates the options"""
        self.options = []
        items = json.load(open("data/items.json", "r"))
        for key in items:
            self.options.append(items[key]["name"])
        self.options.append("Back")

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        if select == len(self.options) - 1:
            self.runVar = False
        else:
            item = json.load(open("data/items.json", "r"))[self.options[select]]
            ItemShop(item, self.player).run()


class ItemShop(Menu):
    """ItemShop class, used to create the item shop"""
    def __init__(self, data, player):
        """Constructor for the ItemShop class, takes in data and player"""
        clearAll()
        self.player = player
        self.data = data
        if self.data['type'] == "heal":
            self.item = HealItem(self.data['name'], self.data['description'], self.data['health'], self.data['mana'], self.data['rarity'], self.data['value'])
        elif self.data['type'] == "buff":
            self.item = BuffItem(self.data['name'], self.data['description'], self.data['health'], self.data['mana'], self.data['buff'], self.data['duration'], self.data['rarity'], self.data['value'])
        title = open("ascii/shop", "r").readlines()
        option = ["Information", "Buy", "Back"]
        super().__init__(title, option, self.onSpace)

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                printText(mainWin, 0, [(self.item, 9, None)])
                spaceToContinue()
            case 1:
                if self.player.gold >= self.item.value:
                    self.player.gold -= self.item.value
                    self.player.inventory.addItem(self.item)
                    printText(mainWin, 0, [("You bought ", 9, None), (f" {self.item.name} ", 9, "bold")])
                    i = self.player.inventory.getExistingItems().index(self.item.name)
                    qty = self.player.inventory.items[i][1]
                    printText(mainWin, 1, [("You now have ", 9, None), (f" {qty} ", 9, "bold"), ("x ", 9, None), (f" {self.item.name} ", 9, "bold")])
                    printText(mainWin, 2, [("You have ", 9, None), (f" {self.player.gold} ", 9, "bold"), ("gold left", 9, None)])
                    spaceToContinue()
                else:
                    printText(mainWin, 0, [("You don't have enough gold", 1, None)])
                    printText(mainWin, 1, [("You need ", 9, None), (f" {self.item.value - self.player.gold} ", 9, "bold"), ("more gold", 9, None)])
                    spaceToContinue()
            case 2:
                self.runVar = False

#INVENTORY
class InventoryUI(Menu): 
    """InventoryUI class, used to create the inventory UI"""
    def __init__(self, inventory, player):
        """Constructor for the InventoryUI class, takes in inventory and player"""
        clearAll()
        self.inventory = inventory
        self.player = player
        title = open('ascii/inventory', 'r').readlines()
        options = ["Items", "Gear", "Back"]
        super().__init__(title, options, self.onSpace)

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                ItemInventoryUI(self.inventory, self.player).run()
            case 1:
                GearInventoryUI(self.inventory, self.player).run()
            case 2:
                self.runVar = False


class ItemInventoryUI(Menu):
    """ItemInventoryUI class, used to create the item inventory UI"""
    def __init__(self, inventory, player, inFight = False):
        """Constructor for the ItemInventoryUI class, takes in inventory, player, and inFight"""
        clearAll()
        self.inventory = inventory
        self.player = player
        self.inFight = inFight
        if self.inFight: self.used = False
        title = open('ascii/inventory', 'r').readlines()
        self.rewriteOptions()
        super().__init__(title, self.option, self.onSpace)

    def rewriteOptions(self):
        """Rewrites the options"""
        self.option = []
        for item in self.inventory.items:
            if item[0] != None:
                self.option.append(f"{item[0].name} x{item[1]}")
            else:
                self.option.append("Empty")
        self.option.append("Back")

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        if select == len(self.option) - 1:
            self.runVar = False
        elif self.inventory.items[select][0] != None:
            item = self.inventory.items[select]
            ui = ItemUI(self.inventory, item, self.player, self.inFight)
            ui.run()
            if self.inFight:
                self.used = ui.used
                if self.used:
                    self.runVar = False
            else:
                self.rewriteOptions()


class ItemUI(Menu):
    """ItemUI class, used to create the item UI"""
    def __init__(self, inventory, item, player, inFight = False):
        """Constructor for the ItemUI class, takes in inventory, item, player, and inFight"""
        clearAll()
        self.inventory = inventory
        self.item = item[0]
        self.quantity = item[1]
        self.player = player
        self.inFight = inFight
        if self.inFight:
            self.used = False
        title = open('ascii/inventory', 'r').readlines()
        options = ["Information", "Use", "Throw One", "Throw All", "Back"]
        super().__init__(title, options, self.onSpace)

    def addInfos(self):
        text = f"{self.item.name} x{self.quantity}"
        printText(mainWin, 5, [(text, 9, "bold")])

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                printText(mainWin, 0, [(self.item, 9, None)])
                spaceToContinue()
            case 1:
                use = True
                if not self.inFight and type(self.item) == BuffItem:
                    printInfo([("Can't use this item outside of a fight", 1, None)])
                    print("Can't use this item outside of a fight")
                    use = False
                if use:
                    self.item.onUse(self.player)
                    self.inventory.removeItem(self.item)
                    printInfo([("You used ", 9, None), (f" {self.item.name} ", 9, "bold")])
                    printInfo([("You now have ", 9, None), (f" {self.quantity} ", 9, "bold"), ("x ", 9, None), (f" {self.item.name} ", 9, "bold")])
                    printInfo([("You have ", 9, None), (f" {self.player.gold} ", 9, "bold"), ("gold left", 9, None)])
                if not self.inFight:
                    spaceToContinue()
                else:
                    self.used = True
                self.runVar = False
            case 2:
                self.inventory.removeItem(self.item)
            case 3:
                self.inventory.removeItem(self.item, self.quantity)
            case 4:
                self.runVar = False


class GearInventoryUI(Menu):
    """GearInventoryUI class, used to create the gear inventory UI"""
    def __init__(self, inventory, player):
        """Constructor for the GearInventoryUI class, takes in inventory and player"""
        clearAll()
        self.inventory = inventory
        self.player = player
        title = open('ascii/inventory', 'r').readlines()
        self.rewriteOptions()
        super().__init__(title, self.option, self.onSpace)

    def rewriteOptions(self):
        """Rewrites the options"""
        self.option = []
        for gear in self.inventory.gear:
            if gear != None:
                self.option.append(f"{color[gear.rarity]} {gear.name}\033[0m")
            else:
                self.option.append("\033[90mEmpty\033[0m")
        self.option.append("Back")

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        if select == len(self.option) - 1:
            self.runVar = False
        elif self.inventory.gear[select] != None:
            gear = self.inventory.gear[select]
            GearUI(self.inventory, gear, self.player).run()
            self.rewriteOptions()


class GearUI(Menu):
    """GearUI class, used to create the gear UI"""
    def __init__(self, inventory, gear, player):
        """Constructor for the GearUI class, takes in inventory, gear, and player"""
        clearAll()
        self.inventory = inventory
        self.gear = gear
        self.player = player
        title = open('ascii/inventory', 'r').readlines()
        options = ["Equip", "Throw", "Back"]
        super().__init__(title, options, self.onSpace, self.addInfos)

    def addInfos(self):
        """Function to add more infos on the menu"""
        text = self.gear.name
        printText(mainWin, 5, [(text, 9, "bold")])

    def printMenu(self):
        """Prints the menu with the information about the gear"""
        def diffColor(diff):
            if diff < 0:
                return f"\033[31m{diff}\033[0m"
            else:
                return f"\033[32m+{diff}\033[0m"
        clear()
        printText(mainWin, 0, [(self.title, 9, "bold")])
        part = type(self.gear)
        if part == Weapon:
            equiped = self.player.weapon
            damageDiff = diffColor(self.gear.baseDamage - equiped.baseDamage)
        elif part == Armor:
            equiped = self.player.armor
            armorDiff = diffColor(self.gear.baseArmor - equiped.baseArmor)
        levelDiff = diffColor(self.gear.level - equiped.level)
        rarityDiff = diffColor(self.gear.rarity - equiped.rarity)
        manaDiff = diffColor(self.gear.mana - equiped.mana)

        printText(mainWin, 1, [("Description: ", 9, None), (self.gear.description, 9, "bold")]) # current gear
        printText(mainWin, 2, [("Level: ", 9, None), (f"{self.gear.level} {levelDiff}", 9, "bold")])
        printText(mainWin, 3, [(f"Rarity: {color[self.gear.rarity]}", 9, None), (f" {rarityDiff}", 9, "bold")])
        if part == Weapon:
            printText(mainWin, 4, [("Damage: ", 9, None), (f"{self.gear.baseDamage} {damageDiff}", 9, "bold")])
        elif part == Armor:
            printText(mainWin, 4, [("Armor: ", 9, None), (f"{self.gear.baseArmor} {armorDiff}", 9, "bold")])
        printText(mainWin, 5, [("Mana: ", 9, None), (f"{self.gear.mana} {manaDiff}", 9, "bold")])

        printText(mainWin, 7, [("Equiped: ", 9, None), (f"{color[equiped.rarity]} {equiped.name}", 9, "bold")]) # equiped gear
        printText(mainWin, 8, [("Level: ", 9, None), (f"{equiped.level}", 9, "bold")])
        printText(mainWin, 9, [(f"Rarity: {color[equiped.rarity]}", 9, None)])
        if part == Weapon:
            printText(mainWin, 10, [("Damage: ", 9, None), (f"{equiped.baseDamage}", 9, "bold")])
        elif part == Armor:
            printText(mainWin, 10, [("Armor: ", 9, None), (f"{equiped.baseArmor}", 9, "bold")])
        printText(mainWin, 11, [("Mana: ", 9, None), (f"{equiped.mana}", 9, "bold")])

        #selected option will be in green
        for i, option in enumerate(self.option):
            if i == self.select:
                printText(mainWin, i+13, [(">", 5, "bold"), (option, 5, "bold")])
            else:
                printText(mainWin, i+13, [(option, 9, None)])

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                playerWeapon = self.player.weapon
                playerArmor = self.player.armor
                if type(self.gear) == Weapon:
                    self.player.weapon = self.gear
                    self.inventory.removeGear(self.gear)
                    self.inventory.addGear(playerWeapon)
                elif type(self.gear) == Armor:
                    self.player.armor = self.gear
                    self.inventory.removeGear(self.gear)
                    self.inventory.addGear(playerArmor)
                #change player mana
                self.player.maxMana = 100 + self.player.armor.mana + self.player.weapon.mana
                printInfo([("Gear equipped", 9, None)])
                spaceToContinue()
                self.runVar = False
            case 1:
                self.inventory.removeGear(self.gear)
                self.runVar = False
            case 2:
                self.runVar = False


#SPELL
class SpellTree:
    """SpellTree class, used to create the spell tree"""
    def __init__(self, role, player, inFight = False, enemy = None):
        """Constructor for the SpellTree class, takes in role, player, inFight, and enemy"""
        clearAll()
        self.title = open("ascii/spell", "r").read()
        self.player = player
        self.current = self.initTree(role)
        self.selected = 0
        self.path = [self.current]
        self.spells = [self.current.spell] + [branch.spell for branch in self.current.branches]
        self.inFight = inFight
        self.casted = False
        self.enemy = enemy

    def changeTree(self, tree):
        """Changes the tree"""
        self.path.append(tree)
        self.current = tree
        self.spells = [self.current.spell] + [branch.spell for branch in self.current.branches]
        self.selected = 0
        self.render()

    def goBack(self):
        """Goes back in the tree"""
        self.path.pop()
        self.current = self.path[-1]
        self.spells = [self.current.spell] + [branch.spell for branch in self.current.branches]
        self.selected = 0
        self.render()

    def navigate(self):
        """Navigate in the tree"""
        getInput = True
        while getInput:
            if keyPress("left"):
                self.selected -= 1
                if self.selected < 0:
                    self.selected = len(self.spells)-1
                getInput = False
            elif keyPress("right"):
                self.selected += 1
                if self.selected > len(self.spells)-1:
                    self.selected = 0
                getInput = False
            elif keyPress("space"):
                if self.inFight:
                    choiceUI = CastSpellUI(self, self.player, self.enemy, self.spells[self.selected])
                    choiceUI.run()
                    if choiceUI.casted:
                        self.casted = True
                        self.runVar = False
                else:
                    SpellUI(self.player, self.spells[self.selected], self).run()
                getInput = False
            elif keyPress("escape"):
                if len(self.path) == 1:
                    self.runVar = False
                else:
                    self.goBack()
                getInput = False

    def render(self):
        """Renders the tree"""
        clearAll()
        print(self.title)
        print(separator)
        def offset(x): return ' ' * x
        def sliceSpell(branch, selected = False):
            symbol = branch.spell.symbol
            line1 = "╔═╩═╗"
            if selected:
                line2 = f"║{symbol} ║"
            else:
                line2 = f"║{symbol} ║"
            if len(branch.branches) == 0:
                line3 = "╚═══╝"
                line4 = "     "
            else:
                line3 = "╚═╦═╝"
                line4 = "  ║  "
            return line1, line2, line3, line4

        selectedList = [False] * (len(self.current.branches)+1)  # +1 for the current spell
        selectedList[self.selected] = True # to set the selected spell in the tree

        printText(mainWin, 0, [(offset(30), 9, None), ("║", 9, None)])
        spellSlice = sliceSpell(self.current, selectedList[0])
        for i in range(4):
            printText(mainWin, i+1, [(offset(28), 9, None), (spellSlice[i], 9, None)])
        if len(self.current.branches) == 1:
            printText(mainWin, 5, [(offset(30), 9, None), ("║", 9, None)])
            spell1 = sliceSpell(self.current.branches[0], selectedList[1])
            for i in range(4):
                printText(mainWin, i+6, [(offset(28), 9, None), (spell1[i], 9, None)])
        elif len(self.current.branches) == 2:
            printText(mainWin, 5, [(offset(15), 9, None), ("╔══════════════╩══════════════╗", 9, None)])
            spell1 = sliceSpell(self.current.branches[0], selectedList[1])
            spell2 = sliceSpell(self.current.branches[1], selectedList[2])
            for i in range(4):
                printText(mainWin, i+6, [(offset(13), 9, None), (spell1[i], 9, None), (offset(25), 9, None), (spell2[i], 9, None)])
                print(offset(13) + spell1[i] + offset(25) + spell2[i])
        elif len(self.current.branches) == 3:
            printText(mainWin, 5, [(offset(10), 9, None), ("╔═══════════════════╬═══════════════════╗", 9, None)])
            spell1 = sliceSpell(self.current.branches[0], selectedList[1])
            spell2 = sliceSpell(self.current.branches[1], selectedList[2])
            spell3 = sliceSpell(self.current.branches[2], selectedList[3])
            for i in range(4):
                printText(mainWin, i+6, [(offset(8), 9, None), (spell1[i], 9, None), (offset(15), 9, None), (spell2[i], 9, None), (offset(15), 9, None), (spell3[i], 9, None)])
        elif len(self.current.branches) == 4:
            printText(mainWin, 5, [(offset(14), 9, None), ("╔═══════╦═══════╩═══════╦═══════╗", 9, None)])
            spell1 = sliceSpell(self.current.branches[0], selectedList[1])
            spell2 = sliceSpell(self.current.branches[1], selectedList[2])
            spell3 = sliceSpell(self.current.branches[2], selectedList[3])
            spell4 = sliceSpell(self.current.branches[3], selectedList[4])
            for i in range(4):
                printText(mainWin, i+6, [(offset(12), 9, None), (spell1[i], 9, None), (offset(3), 9, None), (spell2[i], 9, None), (offset(11), 9, None), (spell3[i], 9, None), (offset(3), 9, None), (spell4[i], 9, None)])
        printInfo([("Navigate with ", 9, None), ("◄ ►", 9, "bold"), (" and press ", 9, None), ("˽", 9, "bold"), (" to select. ESC to go back", 9, None)])


    def initTree(self, role):
        """Initializes the tree depending on the role of the player recursively"""
        if role == "mage":
            data = json.load(open("data/spells/mage.json", "r", encoding="utf-8"))
        elif role == "warrior":
            data = json.load(open("data/spells/warrior.json", "r", encoding="utf-8"))
        elif role == "archer":
            data = json.load(open("data/spells/archer.json", "r", encoding="utf-8"))
        firstKey = list(data.keys())[0]

        def createTree(key, data):
            """Creates part of the tree"""
            spellData = data[key]
            if spellData['type'] == "damage":
                spell = DamageSpell(spellData['name'], spellData['symbol'], spellData['cost'], spellData['damage'], spellData['scale'], spellData['description'], spellData['unlock'])
            elif spellData['type'] == "heal":
                spell = HealSpell(spellData['name'], spellData['symbol'], spellData['cost'], spellData['heal'], spellData['scale'], spellData['description'], spellData['unlock'])
            elif spellData['type'] == "buff":
                spell = BuffSpell(spellData['name'], spellData['symbol'], spellData['cost'], spellData['heal'], spellData['scale'], spellData['buff'], spellData['duration'], spellData['description'], spellData['unlock'])
            elif spellData['type'] == "debuff":
                spell = DebuffSpell(spellData['name'], spellData['symbol'], spellData['cost'], spellData['damage'], spellData['scale'], spellData['debuff'], spellData['duration'], spellData['description'], spellData['unlock'])
            branches = []
            for nextKey in data[key]['next']:
                branches.append(createTree(nextKey, data[key]['next']))
            return Tree(spell, branches)

        return createTree(firstKey, data)

    def run(self):
        """Runs the tree"""
        self.runVar = True
        while self.runVar:
            self.render()
            self.navigate()


class SpellUI(Menu):
    """SpellUI class, used to create the spell UI"""
    def __init__(self, player, spell, tree):
        """Constructor for the SpellUI class, takes in player, spell, and tree"""
        clearAll()
        title = open("ascii/spell", "r").read()
        options = ("Information", "Unlock", "Go to this spell", "Back")
        super().__init__(title, options, self.onSpace)
        self.player = player
        self.spell = spell
        self.spellTree = tree

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                printText(mainWin, 0, [(self.spell.symbol), (self.spell.name, 9, None)])
                printText(mainWin, 1, [(self.spell.description, 9, None)])
                if self.spell.name in self.player.spells:
                    printText(mainWin, 2, [("This spell is unlocked", 7, None)])
                elif self.spell.unlock["level"] <= self.player.level:
                    printText(mainWin, 2, [("This spell can be unlocked", 5, None)])
                    printText(mainWin, 3, [("Level required: ", 9, None), (f"{self.spell.unlock['level']}", 9, "bold")])
                    printText(mainWin, 4, [("Cost: ", 9, None), (f"{self.spell.unlock['cost']}", 9, "bold")])
                else:
                    printText(mainWin, 2, [("\033[3;31mThis spell can't be unlocked yet\033[0m", 4, None)])
                    printText(mainWin, 3, [("Level required: ", 9, None), (f"{self.spell.unlock['level']}", 9, "bold")])
                printText(mainWin, 5, [("Mana Cost: ", 9, None), (f"{self.spell.cost}", 9, "bold")])
                if type(self.spell) == DamageSpell:
                    printText(mainWin, 6, [("Damage: ", 9, None), (f"{int(self.spell.damage+(self.spell.scale*self.player.mana))}", 9, "bold")])
                elif type(self.spell) == HealSpell:
                    printText(mainWin, 6, [("Heal: ", 9, None), (f"{int(self.spell.heal+(self.spell.scale*self.player.mana))}", 9, "bold")])
                elif type(self.spell) == BuffSpell:
                    printText(mainWin, 6, [("Heal: ", 9, None), (f"{int(self.spell.heal+(self.spell.scale*self.player.mana))}", 9, "bold")])
                    printText(mainWin, 7, [("Buff: ", 9, None), (f"{self.spell.buff}", 9, "bold")])
                    printText(mainWin, 8, [("Duration: ", 9, None), (f"{self.spell.duration}", 9, "bold")])
                elif type(self.spell) == DebuffSpell:
                    printText(mainWin, 6, [("Damage: ", 9, None), (f"{int(self.spell.damage+(self.spell.scale*self.player.mana))}", 9, "bold")])
                    printText(mainWin, 7, [("Debuff: ", 9, None), (f"{self.spell.debuff}", 9, "bold")])
                    printText(mainWin, 8, [("Duration: ", 9, None), (f"{self.spell.duration}", 9, "bold")])
                spaceToContinue()
            case 1:
                if self.spell.name in self.player.spells:
                    printInfo([("This spell is already unlocked", 7, None)])
                    spaceToContinue()
                elif self.spell.unlock["level"] <= self.player.level:
                    if self.player.gold >= self.spell.unlock["cost"]:
                        self.player.gold -= self.spell.unlock["cost"]
                        self.player.spells.append(self.spell.name)
                        printInfo([("You unlocked ", 9, None), (f"{self.spell.name}", 9, "bold")])
                        spaceToContinue()
                    else:
                        printInfo([("You don't have enough gold", 1, None)])
                        spaceToContinue()
                else:
                    printInfo([("Your level is to low to unlock this spell", 1, None)])
                    spaceToContinue()
            case 2:
                if self.spellTree.selected == 0:
                    printInfo(mainWin, 0, [("You are already on this spell", 1, None)])
                    spaceToContinue()
                elif len(self.spellTree.current.branches[self.spellTree.selected-1].branches) == 0:
                    printInfo([("This spell doesn't unlock any other spell", 1, None)])
                    spaceToContinue()
                else:
                    if self.spell.name not in self.player.spells:
                        printInfo([("You didn't unlock this spell yet", 1, None)])
                        spaceToContinue()
                    else:
                        self.spellTree.changeTree(self.spellTree.current.branches[self.spellTree.selected-1])
                        self.runVar = False
            case 3:
                self.runVar = False


class CastSpellUI(Menu):
    """CastSpellUI class, used to create the cast spell UI"""
    def __init__(self, spellTree, player, enemy, spell):
        """Constructor for the CastSpellUI class, takes in spellTree, player, enemy, and spell"""
        title = open("ascii/spell", "r").read()
        options = ("Cast", "Go to this spell", "Back")
        super().__init__(title, options, self.onSpace)
        self.spellTree = spellTree
        self.player = player
        self.enemy = enemy
        self.spell = spell
        self.casted = False

    def printMenu(self):
        """Prints the menu with the information about the spell"""
        clearMain()
        printText(mainWin, 0, [(self.title, 9, "bold")])
        printText(mainWin, 1, [("Mana: ", 9, None), (f"{self.player.mana}/{self.player.maxMana}", 9, "bold")])
        printText(mainWin, 2, [(self.spell.symbol, 9, None), (self.spell.name, 9, None)])
        printText(mainWin, 3, [(self.spell.description, 9, None)])
        if self.spell.name in self.player.spells:
            printText(mainWin, 4, [("This spell is unlocked", 7, None)])
        elif self.spell.unlock["level"] <= self.player.level:
            printText(mainWin, 4, [("This spell can be unlocked", 5, None)])
            printText(mainWin, 5, [("Level required: ", 9, None), (f"{self.spell.unlock['level']}", 9, "bold")])
            printText(mainWin, 6, [("Cost: ", 9, None), (f"{self.spell.unlock['cost']}", 9, "bold")])
        else:
            printText(mainWin, 4, [("\033[3;31mThis spell can't be unlocked yet\033[0m", 4, None)])
            printText(mainWin, 5, [("Level required: ", 9, None), (f"{self.spell.unlock['level']}", 9, "bold")])
        printText(mainWin, 7, [("Mana Cost: ", 9, None), (f"{self.spell.cost}", 9, "bold")])
        if type(self.spell) == DamageSpell:
            printText(mainWin, 8, [("Damage: ", 9, None), (f"{int(self.spell.damage+(self.spell.scale*self.player.mana))}", 9, "bold")])
        elif type(self.spell) == HealSpell:
            printText(mainWin, 8, [("Heal: ", 9, None), (f"{int(self.spell.heal+(self.spell.scale*self.player.mana))}", 9, "bold")])
        elif type(self.spell) == BuffSpell:
            printText(mainWin, 8, [("Heal: ", 9, None), (f"{int(self.spell.heal+(self.spell.scale*self.player.mana))}", 9, "bold")])
            printText(mainWin, 9, [("Buff: ", 9, None), (f"{self.spell.buff}", 9, "bold")])
            printText(mainWin, 10, [("Duration: ", 9, None), (f"{self.spell.duration}", 9, "bold")])
        elif type(self.spell) == DebuffSpell:
            printText(mainWin, 8, [("Damage: ", 9, None), (f"{int(self.spell.damage+(self.spell.scale*self.player.mana))}", 9, "bold")])
            printText(mainWin, 9, [("Debuff: ", 9, None), (f"{self.spell.debuff}", 9, "bold")])
            printText(mainWin, 10, [("Duration: ", 9, None), (f"{self.spell.duration}", 9, "bold")])
        #selected option will be in green
        for i, option in enumerate(self.option):
            if i == self.select:
                printText(mainWin, i+12, [(">", 5, "bold"), (option, 5, "bold")])
            else:
                printText(mainWin, i+12, [(option, 9, None)])

    def getTarget(self):
        """Gets the target of the spell"""
        if type(self.spell) == DamageSpell:
            return self.enemy
        elif type(self.spell) == HealSpell:
            return self.player
        elif type(self.spell) == BuffSpell:
            return self.player
        elif type(self.spell) == DebuffSpell:
            return self.enemy

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                pactRequired = ["Infernal Blade", "Infernal Shield", "Abyssal Regeneration"]
                demonizedRequired = ["Demonic Blade", "Demon's Mark"]
                if self.spell.name not in self.player.spells:
                    printText(mainWin, 0, [("This spell is not unlocked", 1, None)])
                    spaceToContinue()
                elif self.spell.cost > self.player.mana:
                    printText(mainWin, 0, [("You don't have enough mana", 1, None)])
                    spaceToContinue()
                elif self.spell.unlock["level"] > self.player.level:
                    printText(mainWin, 0, [("Your level is to low to use this spell", 1, None)])
                    spaceToContinue()
                elif self.spell.name in pactRequired and not Fight.haveBuff("pact", self.player):
                    printText(mainWin, 0, [("You need to make a pact with a demon to use  this spell", 1, None)])
                    spaceToContinue()
                elif self.spell.name in demonizedRequired and not Fight.haveBuff("demonized", self.player):
                    printText(mainWin, 0, [("You need in your demon form to use this spell", 1, None)])
                    spaceToContinue()
                elif self.spell.name in self.player.spells:
                    text = self.spell.onUse(self.player, self.getTarget())
                    printText(mainWin, 0, [(text, 9, None)])
                    self.casted = True
                self.runVar = False
            case 1:
                if self.spellTree.selected == 0:
                    printText(mainWin, 0, [("You are already on this spell", 1, None)])
                    spaceToContinue()
                elif len(self.spellTree.current.branches[self.spellTree.selected-1].branches) == 0:
                    printText(mainWin, 0, [("This spell doesn't unlock any other spell", 1, None)])
                    spaceToContinue()
                else:
                    if self.spell.name not in self.player.spells:
                        printText(mainWin, 0, [("You didn't unlock this spell yet", 1, None)])
                        spaceToContinue()
                    else:
                        self.spellTree.changeTree(self.spellTree.current.branches[self.spellTree.selected-1])
                        self.runVar = False
            case 2:
                self.runVar = False


class Game:
    """Game class, main class of the game that contains the player and the current room"""
    separator = "─" * 61
    def __init__(self, new = True, role = None):
        """Constructor for the Game class, takes in new and role"""
        if new: #new = True if the player start a new game
            clearAll()
            self.player = Player(role)
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
            self.player.maxMana = 100 + self.player.armor.mana + self.player.weapon.mana
        self.lobby = Lobby(self.player)
        self.currentRoom = self.lobby #base room is the lobby

    def getElementAroundPlayer(self):
        """Gets all interactable element around the player"""
        #get element adjacent to the player
        coord = self.currentRoom.getPlayerCoord()
        direction = ((1, 0), (-1, 0), (0, 1), (0, -1))
        adjList = []
        for dir in direction:
            adjList.append(self.currentRoom.map[coord[0] + dir[0]][coord[1] + dir[1]])
        return adjList

    def playerInteraction(self):
        """Player Interaction Handler. Interact with the element around the player"""
        clearInfo()
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
                self.player.gold += money
                printInfo([(f"You found {color[item.rarity]} {item.name} and {money} gold in the treasure", 9, None)])
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
                    printInfo([("You flee the fight", 9, None)])
                elif win == "skip":
                    self.currentRoom.map[element.coord[0]][element.coord[1]] = '.'
                    printInfo([("You skip the fight", 9, None)])
                elif win == "floorSkip":
                    printInfo([("You skip the fight and the floor", 9, None)])
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
                elif win == True:
                    self.currentRoom.map[element.coord[0]][element.coord[1]] = '.'
                    printInfo([("You win the fight", 9, None)])
                    printInfo([(f"You gain {element.exp} exp and {element.gold} gold", 9, None)])
                    self.player.exp += element.exp
                    self.player.gold += element.gold
                    if self.player.exp >= (self.player.level*5)**2:
                        self.player.exp = 0
                        if self.player.level < 50:
                            self.player.level += 1
                            printInfo([("You level up", 9, None)])
                            printInfo([(f"You are now level {self.player.level}", 9, None)])
                        elif self.player.level == 50:
                            printInfo([("You are level max, you can't level up anymore", 9, None)])
                else:
                    self.currentRoom = self.lobby
                    self.player.health = 100
                    self.lobby.dungeon.makeDungeon(self.player.level)
                    self.lobby.placePortal()
                    printInfo([("You died, you will be teleported back to the ", 9, None), ("lobby", 3, "bold")])
                    printInfo([("You lose all your gold", 9, None)])
                    self.player.exp = 0
                    self.player.level = 1
                self.save()
                spaceToContinue()
            elif element == "C": #if there is a chest open it
                InventoryUI(self.player.inventory, self.player).run()
                self.save()
            elif element == "G": #if there is a grimoire use it to see the spell tree
                SpellTree(self.player.role, self.player).run()
                self.save()
            elif element == "S":
                Shop(self.player).run()
                self.save()
        self.printRoom()

    def interactionInfo(self):
        clearInfo()
        """Prints info about the interaction with the element around the player"""
        adjList = self.getElementAroundPlayer()
        for element in adjList:
            if type(element) == Portal:
                if type(self.currentRoom) == Lobby:
                    printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to start a ", 9, None), ("dungeon", 4, "bold")])
                else:
                    if self.currentRoom.portal.room2 == None:
                        printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to go back to the ", 9, None), ("lobby", 3, "bold")])
                    else:
                        printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to go to the next ", 9, None), ("floor", 4, "bold")])
            elif type(element) == Enemy:
                printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to start the ", 9, None), ("fight", 1, "bold")])
            elif type(element) == Treasure:
                printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to open the ", 9, None), ("treasure", 2, "bold")])
            elif element == "C":
                printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to open your ", 9, None), ("inventory", 3, "bold")])
            elif element == "G":
                printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to see your ", 9, None), ("spell tree", 4, "bold")])
            elif element == "S":
                printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to open the ", 9, None), ("shop", 3, "bold")])

    def playerMove(self, direction):
        """Player Movement Handler. Move the player in the room depending on the direction"""
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

    def printRoom(self):
        """Prints the room and all infos -> called after every player action"""
        clearMain()
        #print current room name
        if type(self.currentRoom) == Lobby:
            text = "Lobby"
        else:
            text = f"Dungeon: Floor {self.lobby.dungeon.floor + 1} of {len(self.lobby.dungeon.rooms)}"
        printText(statsWin, 0, [("Current Room: ", 9, None), (text, 9, "bold")])
        printText(statsWin, 1, [(f"Gold: {self.player.gold}", 2, None)])
        if self.currentRoom == self.lobby:
            mist = False
        else:
            mist = True
        self.currentRoom.render = self.currentRoom.colorMap(mist=mist)
        printMap(self.currentRoom.render)

        #print player info
        healthText = f'Health: {self.player.health}/100'
        healthBar = bar(self.player.health, 100)
        printText(statsWin, 2, [(healthText, 9, None)])
        printText(statsWin, 3, [(healthBar, 9, None)])
        manaText = f'Mana: {self.player.mana}/{self.player.maxMana}'
        manaBar = bar(self.player.mana, self.player.maxMana)
        printText(statsWin, 4, [(manaText, 9, None)])
        printText(statsWin, 5, [(manaBar, 9, None)])
        expText = f'Exp: {self.player.exp}/{(self.player.level*5)**2}'
        levelText = f'Level: {self.player.level}'
        whiteSpace = " " * (59 - len(expText) - len(levelText))
        expBar = bar(self.player.exp, (self.player.level*10)**2, length=57)
        printText(statsWin, 6, [(expText, 9, None), (whiteSpace, 9, None), (levelText, 9, None)])
        printText(statsWin, 7, [(expBar, 9, None)])
        self.interactionInfo()

    def save(self):
        """Saves the player and the inventory data in the save folder"""
        self.player.save()
        self.player.inventory.save()

    def run(self):
        """Runs the game"""
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
    """Fight class, used to create a fight between the player and an enemy"""
    def __init__(self, player, enemy):
        """Constructor for the Fight class, takes in player and enemy"""
        self.player = player
        self.enemy = enemy
        self.resetBuffDebuff()
        self.enemySpellData = json.load(open("data/spells/enemy.json", "r", encoding="utf-8"))
        self.flee = False
        self.skip = False
        self.floorSkip = False

    @staticmethod
    def haveBuff(buff, target):
        """Returns True if the target has the buff else returns False"""
        buffsList = [element[0] for element in target.buff]
        if buff in buffsList:
            return True
        return False

    @staticmethod
    def haveDebuff(debuff, target):
        """Returns True if the target has the debuff else returns False"""
        debuffsList = [element[0] for element in target.debuff]
        if debuff in debuffsList:
            return True
        return False

    def removeBuffDebuff(self, target):
        """Removes 1 turn to all buff and debuff of the target"""
        for i, element in enumerate(target.buff):
            if element[0] == "purify":
                target.buff.pop(i)
            else:
                target.buff[i][1] -= 1
                if element[1] <= 0:
                    target.buff.pop(i)
                    i -= 1
        for i, element in enumerate(target.debuff):
            target.debuff[i][1] -= 1
            if element[1] <= 0:
                target.debuff.pop(i)
                i -= 1

    def resetBuffDebuff(self):
        """Resets all buff and debuff of the player and the enemy"""
        self.player.buff = []
        self.player.debuff = []
        self.enemy.buff = []
        self.enemy.debuff = []

    def turn(self):
        """Turn Handler. Manages the turn of the player and the enemy"""
        #player turn
        if self.player.health > 0:
            self.playerTurn()
        #purify effect (player only)
        if self.haveBuff("purify", self.player):
            self.player.debuff = []
            print(f"\033[3;92m{self.player.name}\033[0m are purified ! All debuffs are removed")
            spaceToContinue()
        #skip potion
        if self.haveBuff("skip", self.player):
            for i, element in enumerate(self.player.buff):
                if element[0] == "skip":
                    self.player.buff.pop(i)
            self.skip = True
            return True
        #floorSkip potion
        if self.haveBuff("floorSkip", self.player):
            for i, element in enumerate(self.player.buff):
                if element[0] == "floorSkip":
                    self.player.buff.pop(i)
            self.floorSkip = True
            return True

        #enemy turn
        if self.enemy.health > 0:
            self.enemyTurn()
        if self.flee:
            return True
        
        #poison effect
        p = False
        if self.haveDebuff("poison", self.player):
            self.player.health -= 5
            print(f"\033[3;31m{self.player.name}\033[0m are poisoned and lose \033[1;31m5 health\033[0m")
            p = True
        if self.haveDebuff("poison", self.enemy):
            self.enemy.health -= 5
            print(f"\033[3;31m{self.enemy.name}\033[0m is poisoned and loses \033[1;31m5 health\033[0m")
            p = True
        if p:
            spaceToContinue()

        #burn effect
        b = False
        if self.haveDebuff("burn", self.player):
            self.player.health -= 5
            print(f"\033[3;31m{self.player.name}\033[0m are burning and lose \033[1;31m5 health\033[0m")
            b = True
        if self.haveDebuff("burn", self.enemy):
            self.enemy.health -= 5
            print(f"\033[3;31m{self.enemy.name}\033[0m is burning and loses \033[1;31m5 health\033[0m")
            b = True
        if b:
            spaceToContinue()
        
        # revive buff (player only)
        if self.haveBuff("revive", self.player) and self.player.health <= 0:
            self.player.health = 100
            self.player.debuff = []
            for i, element in enumerate(self.player.buff):
                if element[0] == "revive":
                    self.player.buff.pop(i)
            print(f"\033[3;92m{self.player.name}\033[0m is revived !")
            spaceToContinue()

        self.removeBuffDebuff(self.player)
        self.removeBuffDebuff(self.enemy)
        return self.endFight()
    
    def enemySpell(self):
        """Enemy Spell Handler. Manages the enemy spell"""
        def evalSpell(spell):
            """Evaluates the spell and returns the spell object"""
            if self.enemySpellData[spell]["type"] == "damage":
                return DamageSpell(self.enemySpellData[spell]["name"], self.enemySpellData[spell]["symbol"], self.enemySpellData[spell]["cost"], self.enemySpellData[spell]["damage"], self.enemySpellData[spell]["scale"], self.enemySpellData[spell]["description"], self.enemySpellData[spell]["unlock"])
            elif self.enemySpellData[spell]["type"] == "heal":
                return HealSpell(self.enemySpellData[spell]["name"], self.enemySpellData[spell]["symbol"], self.enemySpellData[spell]["cost"], self.enemySpellData[spell]["heal"], self.enemySpellData[spell]["scale"], self.enemySpellData[spell]["description"], self.enemySpellData[spell]["unlock"])
            elif self.enemySpellData[spell]["type"] == "buff":
                return BuffSpell(self.enemySpellData[spell]["name"], self.enemySpellData[spell]["symbol"], self.enemySpellData[spell]["cost"], self.enemySpellData[spell]["heal"], self.enemySpellData[spell]["scale"], self.enemySpellData[spell]["buff"], self.enemySpellData[spell]["duration"], self.enemySpellData[spell]["description"], self.enemySpellData[spell]["unlock"])
            elif self.enemySpellData[spell]["type"] == "debuff":
                return DebuffSpell(self.enemySpellData[spell]["name"], self.enemySpellData[spell]["symbol"], self.enemySpellData[spell]["cost"], self.enemySpellData[spell]["damage"], self.enemySpellData[spell]["scale"], self.enemySpellData[spell]["debuff"], self.enemySpellData[spell]["duration"], self.enemySpellData[spell]["description"], self.enemySpellData[spell]["unlock"])
        #randomly choose a spell of the enemy level
        spellList = [evalSpell(element) for element in self.enemy.spells if self.enemySpellData[element]["unlock"]["level"] <= self.enemy.level]
        spell = random.choice(spellList)
        #cast the spell
        if spell.cost <= self.enemy.mana:
            if type(spell) == DamageSpell:
                text = spell.onUse(self.enemy, self.player)
            elif type(spell) == HealSpell:
                text = spell.onUse(self.enemy, self.enemy)
            elif type(spell) == BuffSpell:
                text = spell.onUse(self.enemy, self.enemy)
            elif type(spell) == DebuffSpell:
                text = spell.onUse(self.enemy, self.player)
            print(text)
        else:
            print(f"\033[31m{self.enemy.name}\033[0m has exhausted all his mana and can't cast any spell")

    def enemyTurn(self):
        """Enemy Turn Handler. Manages the enemy turn"""
        if self.haveDebuff("stun", self.enemy):
            print(f"\033[31m{self.enemy.name}\033[0m is stunned and can't do anything")
        else:
            print(f"\033[1;31m{self.enemy.name}'s turn\033[0m")
            randomAction = random.randint(1, 2)
            match randomAction:
                case 1:
                    self.evalDamage(self.enemy, self.player)
                case 2:
                    print(f"\033[31m{self.enemy.name}\033[0m uses a spell")
                    if self.haveBuff("invulnerable", self.player):
                        print("\033[32mYou\033[0m are invulnerable !")
                        print(f"\033[31m{self.enemy.name}\033[0m's spell has no effect on \033[32mYou\033[0m")
                    else:
                        self.enemySpell()
        spaceToContinue()

    def playerTurn(self):
        """Player Turn Handler. Manages the player turn"""
        if self.haveDebuff("stun", self.player):
            print("\033[32mYou\033[0m are stunned and can't do anything")
        else:
            #player choose an action
            print("Choose an action:")
            print("1. Attack    2. Spell    3. Item    4. Run")
            getInput = True
            while getInput:
                if keyPress('1'): #attack
                    self.evalDamage(self.player, self.enemy)
                    getInput = False
                elif keyPress('2'): #skill
                    if len(self.player.spells) == 0:
                        print("\033[32mYou\033[0m don't have any spell")
                        spaceToContinue()
                        self.print()
                        self.playerTurn()
                    else:
                        if self.haveBuff("invulnerable", self.enemy):
                            print(f"\033[31m{self.enemy.name}\033[0m is invulnerable !")
                            print("\033[32mYou\033[0mr spell has no effect on him")
                        else:
                            spell = SpellTree(self.player.role, self.player, inFight=True, enemy=self.enemy)
                            spell.run()
                            if not spell.casted:
                                self.print()
                                self.playerTurn()
                    getInput = False
                elif keyPress('3'): #item
                    invItems = self.player.inventory.getExistingItems()
                    empty = True
                    for item in invItems:
                        if item != None:
                            empty = False
                            break
                    if empty:
                        print("\033[32mYou\033[0m don't have any item")
                        spaceToContinue()
                        self.print()
                        self.playerTurn()
                    else:
                        item = ItemInventoryUI(self.player.inventory, self.player, inFight=True)
                        item.run()
                        if not item.used:
                            self.print()
                            self.playerTurn()
                    getInput = False
                elif keyPress('4'): #run
                    print("\033[32mYou\033[0m try to flee")
                    flee = random.randint(1, 2)
                    if flee == 1:
                        print("\033[32mYou\033[0m successfully flee")
                        self.flee = True
                    else:
                        print("\033[32mYou\033[0m failed to flee")
                    getInput = False
        if self.player.mana < self.player.maxMana:
            self.player.mana += self.player.maxMana // 20
            if self.player.mana > self.player.maxMana:
                self.player.mana = self.player.maxMana
        if self.haveBuff("purify", self.player):
            self.player.debuff = []

    def evalDamage(self, user, target):
        """Evaluates the damage dealt by the user to the target and applies it"""
        if self.haveBuff("invulnerable", target):
            if user == self.player:
                print(f"\033[31m{target.name}\033[0m is invulnerable !")
                print("Your attack has no effect on him")
            else:
                print("\033[32mYou\033[0m are invulnerable !")
                print(f"\033[31m{user.name}\033[0m's attack has no effect on \033[32mYou\033[0m")
        else:
            baseAtk = user.weapon.onUse()
            atk = baseAtk + random.randint(-1//(baseAtk // 5), 1//(baseAtk // 5))
            if self.haveBuff("strength", user):
                atk += atk // 2 #atk * 1.5
            if self.haveBuff("shield", target):
                atk -= atk // 2
            if self.haveDebuff("break", target):
                atk -= target.armor.onUse() // 2
            else:
                atk -= target.armor.onUse()
            if atk < 0: atk = 0
            target.health -= atk

            if user == self.player:
                print(f"\033[32mYou\033[0m deal {atk} damage to \033[31m{target.name}\033[0m")

                if self.haveBuff("vampirism", user):
                    user.health += atk // 4
                    if user.health > 100:
                        user.health = 100
                    print(f"\033[32mYou\033[0m gain \033[1;31m{atk // 4} health\033[0m from \033[31m{target.name}\033[0m's blood")
            else:
                print(f"\033[31m{user.name}\033[0m attacks \033[32mYou\033[0m !")
                print(f"\033[31m{user.name}\033[0m deals {atk} damage to \033[32mYou\033[0m")

    def endFight(self):
        """Test if the fight is over"""
        if self.enemy.health <= 0 or self.player.health <= 0:
            return True
        else:
            return False

    def endMessage(self):
        """Returns the state of the fight"""
        win = False
        if self.player.health > 0:
            win = True
        if self.flee:
            win = "flee"
        elif self.skip:
            win = "skip"
        elif self.floorSkip:
            win = "floorSkip"
        return win

    def print(self):
        """Prints the fight screen with all infos"""
        clearMain()
        #print enemy info
        print(f"\033[1;31m{self.enemy.name} - {self.enemy.type}:\033[0m")
        healthText = f'Health: {self.enemy.health}/100'
        print(f'\033[31m{healthText}\033[0m')
        healthBar = bar(self.enemy.health, 100)
        print(f'\033[31m{healthBar}\033[0m')
        # buffList = [element[0] for element in self.enemy.buff]
        print(f"\033[32mBuff:\033[0m {self.enemy.buff}")
        # debuffList = [element[0] for element in self.enemy.debuff]
        print(f"\033[31mDebuff:\033[0m {self.enemy.debuff}")
        self.enemy.render()
        #print player info
        print("\033[1;32mYou\033[0m:")
        healthText = f'Health: {self.player.health}/100'
        manaText = f'Mana: {self.player.mana}/{self.player.maxMana}'
        whiteSpace = " " * (61 - len(healthText) - len(manaText))
        print(f'\033[31m{healthText}\033[0m{whiteSpace}\033[36m{manaText}\033[0m')
        healthBar = bar(self.player.health, 100)
        manaBar = bar(self.player.mana, self.player.maxMana, reversed=True)
        whiteSpace = " " * (61 - len(healthBar) - len(manaBar))
        print(f'\033[31m{healthBar}\033[0m{whiteSpace}\033[36m{manaBar}\033[0m')
        # buffList = [element[0] for element in self.player.buff]
        print(f"\033[32mBuff:\033[0m {self.player.buff}")
        # debuffList = [element[0] for element in self.player.debuff]
        print(f"\033[31mDebuff:\033[0m {self.player.debuff}")
        print(separator)
