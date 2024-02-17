import keyboard
import os
import json
import random
import zipfile
from sys import exit
from datetime import datetime
from time import sleep
from shutil import rmtree
from cursesInit import *
from classes.Map import Lobby, Portal
from classes.Player import Player
from classes.Enemy import Enemy
from classes.Item import Treasure, Weapon, Armor, HealItem, BuffItem, Item, randomWeapon, randomArmor
from classes.Spell import DamageSpell, HealSpell, BuffSpell, DebuffSpell, Tree

separator = "─" * 200
color = { #color for rarity
    1: 9,
    2: 5,
    3: 7,
    4: 3,
    5: 2,
    6: 4
}

os.system("cls")

clearAll()

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

def keyPress(key):
    """Return True if the key is pressed and released"""
    if keyboard.is_pressed(key):
        while keyboard.is_pressed(key): pass
        return True
    return False

def bar(current, maximum, reversed = False, length = 20):
    """Return a bar with current/max"""
    bar = "■" * (current // (maximum // length))
    bar += " " * (length - current // (maximum // length))
    if reversed:
        bar = bar[::-1]
    bar = f'[{bar}]'
    return bar

def spaceToContinue():
    """Wait for the spacebar to be pressed and released"""
    printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to continue", 9, None)])
    wait = True
    while wait:
        if keyPress('space'):
            wait = False

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
        if type(self.title) == str:
            self.title = self.title.split("\n")
        for i, element in enumerate(self.title):
            printText(mainWin, i, [(element, 9, "bold")])
        addLine = self.addInfos()
        if addLine == None:
            addLine = 0
        printText(mainWin, 5+addLine, [(separator, 9, None)])
        #selected option will be in green
        for i, option in enumerate(self.option):
            if i == self.select:
                printText(mainWin, i+6+addLine, [(">", 5, "bold"), (option, 5, "bold")])
            else:
                printText(mainWin, i+6+addLine, [(option, 9, None)])
        refreshAll()

    def selectOption(self):
        """Selects the option"""
        getInput = True
        while getInput:
            if keyPress(keybind['up']):
                getInput = False
                self.select -= 1
                if self.select < 0:
                    self.select = len(self.option) - 1
            elif keyPress(keybind['down']):
                getInput = False
                self.select += 1
                if self.select > len(self.option) - 1:
                    self.select = 0
            elif keyPress('space'):
                getInput = False
                self.onSpace(self.select)
            elif keyPress('esc'):
                getInput = False
                self.runVar = False

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
        title = open("ascii/title", "r").read()
        options = ("New Game", "Continue", "Options", "How to play", "Exit")
        super().__init__(title, options, self.onSpace)

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                if os.path.exists("save/stats.json"):
                    clearMain()
                    printText(mainWin, 0, [("WARNING", 4, "bold"), (": You will overwrite your save file", 9, None)])
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
                    clearMain()
                    printText(mainWin, 0, [("An error occurred", 4, None)])
                    printText(mainWin, 1, [(str(e), 4, None)])
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
        title = open("ascii/role", "r").read()
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
        title = open("ascii/help", "r").read()
        super().__init__(title, options, self.onSpace)

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                text = open("data/help/play.txt", "r").read()
                self.renderText(text)
            case 1:
                text = open("data/help/map.txt", "r").read()
                self.renderText(text)
            case 2:
                text = open("data/help/save.txt", "r").read()
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
        title = open("ascii/options", "r").read()
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
        title = open("ascii/keybind", "r").read()
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
        clearMain()
        printText(mainWin, 0, [("Press the key you want to replace", 9, None), (f" {key} ", 5, "bold"), ("with", 9, None)])
        printText(mainWin, 1, [("Press ", 9, None), ("˽", 9, "bold"),  (" to cancel", 9, None)])
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
        title = open("ascii/pause", "r").read()
        options = ("Resume", "Save", "Options", "Exit")
        super().__init__(title, options, self.onSpace)
        self.game = game
    
    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                self.runVar = False
            case 1:
                clearMain()
                self.game.save()
                printText(mainWin, 0, [("Game saved", 9, None)])
                spaceToContinue()
            case 2:
                OptionMenu().run()
            case 3:
                clearMain()
                printText(mainWin, 0, [("WARNING", 4, "bold"), (": You will lose your progression", 9, None)])
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
        title = open("ascii/shop", "r").read()
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
        title = open("ascii/shop", "r").read()
        option = ["Information", "Buy", "Back"]
        super().__init__(title, option, self.onSpace, self.addInfos)

    def addInfos(self):
        """Adds infos"""
        l = 0
        printText(statsWin, l, [(self.item.name, color[self.item.rarity], "bold")])
        l += 1
        if len(self.item.description) > 59:
            printText(statsWin, l, [(self.item.description[:59], 9, None)])
            printText(statsWin, l+1, [(self.item.description[59:], 9, None)])
            l += 2
        else:
            printText(statsWin, l, [(self.item.description, 9, None)])
            l += 1
        printText(statsWin, l, [("Rarity: ", 9, None), (str(self.item.rarity), color[self.item.rarity], None)])
        printText(statsWin, l+1, [("Value: ", 9, None), (str(self.item.value), 2, None)])

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                clearMain()
                printText(mainWin, 0, [(self.item.name, 9, None)])
                spaceToContinue()
            case 1:
                if self.player.gold >= self.item.value:
                    self.player.gold -= self.item.value
                    self.player.inventory.addItem(self.item)
                    printInfo([("You bought ", 9, None), (self.item.name, 9, "bold")])
                    i = self.player.inventory.getExistingItems().index(self.item.name)
                    qty = self.player.inventory.items[i][1]
                    printInfo([("You now have ", 9, None), (str(qty), 9, "bold"), (" x ", 9, None), (f" {self.item.name} ", 9, "bold")])
                    printInfo([("You have ", 9, None), (str(self.player.gold), 2, "bold"), (" gold left", 9, None)])
                    spaceToContinue()
                else:
                    printInfo([("You don't have enough gold", 4, None)])
                    printInfo([("You need ", 9, None), (f" {self.item.value - self.player.gold} ", 9, "bold"), ("more gold", 9, None)])
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
        title = open('ascii/inventory', 'r').read()
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
        title = open('ascii/inventory', 'r').read()
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
        title = open('ascii/inventory', 'r').read()
        options = ["Information", "Use", "Throw One", "Throw All", "Back"]
        super().__init__(title, options, self.onSpace, self.addInfos)

    def addInfos(self):
        text = f"{self.item.name} x{self.quantity}"
        l = 0
        printText(statsWin, l, [(text, color[self.item.rarity], "bold")])
        l += 1
        if len(self.item.description) > 59:
            printText(statsWin, l, [(self.item.description[:59], 9, None)])
            printText(statsWin, l+1, [(self.item.description[59:], 9, None)])
            l += 2
        else:
            printText(statsWin, l, [(self.item.description, 9, None)])
            l += 1
        printText(statsWin, l, [("Rarity: ", 9, None), (str(self.item.rarity), color[self.item.rarity], None)])
        printText(statsWin, l+1, [("Value: ", 9, None), (str(self.item.value), 2, None)])

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                clearMain()
                text = f"{self.item.name} x{self.quantity}"
                l = 0
                printText(mainWin, l, [(text, color[self.item.rarity], "bold")])
                l += 1
                if len(self.item.description) > 59:
                    printText(mainWin, l, [(self.item.description[:59], 9, None)])
                    printText(mainWin, l+1, [(self.item.description[59:], 9, None)])
                    l += 2
                else:
                    printText(mainWin, l, [(self.item.description, 9, None)])
                    l += 1
                printText(mainWin, l, [("Rarity: ", 9, None), (str(self.item.rarity), color[self.item.rarity], None)])
                printText(mainWin, l+1, [("Value: ", 9, None), (str(self.item.value), 2, None)])
                spaceToContinue()
                self.runVar = False
            case 1:
                if type(self.item) != Item:
                    use = True
                    if not self.inFight and type(self.item) == BuffItem:
                        printInfo([("Can't use this item outside of a fight", 1, None)])
                        use = False
                    if use:
                        self.item.onUse(self.player)
                        self.inventory.removeItem(self.item)
                        printInfo([("You used ", 9, None), (self.item.name, 9, "bold")])
                        printInfo([("You now have ", 9, None), (str(self.quantity), 9, "bold"), (" x ", 9, None), (self.item.name, 9, "bold")])
                    if not self.inFight:
                        spaceToContinue()
                    else:
                        self.used = True
                self.runVar = False
            case 2:
                self.inventory.removeItem(self.item)
                printInfo([("You threw ", 9, None), (self.item.name, 9, "bold")])
                printInfo([("You now have ", 9, None), (str(self.quantity), 9, "bold"), (" x ", 9, None), (self.item.name, 9, "bold")])
                self.runVar = False
            case 3:
                self.inventory.removeItem(self.item, self.quantity)
                printInfo([("You threw all your ", 9, None), (self.item.name, 9, "bold")])
                self.runVar = False
            case 4:
                self.runVar = False


class GearInventoryUI(Menu):
    """GearInventoryUI class, used to create the gear inventory UI"""
    def __init__(self, inventory, player):
        """Constructor for the GearInventoryUI class, takes in inventory and player"""
        clearAll()
        self.inventory = inventory
        self.player = player
        title = open('ascii/inventory', 'r').read()
        self.rewriteOptions()
        super().__init__(title, self.option, self.onSpace)

    def rewriteOptions(self):
        """Rewrites the options"""
        self.option = []
        for gear in self.inventory.gear:
            if gear != None:
                self.option.append(gear.name)
            else:
                self.option.append("Empty")
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
        title = open('ascii/inventory', 'r').read()
        options = ["Equip", "Throw", "Back"]
        super().__init__(title, options, self.onSpace, self.addInfos)

    def addInfos(self):
        """Function to add more infos on the menu"""
        def diffColor(diff):
            if diff < 0:
                return (str(diff), 4, None)
            else:
                return (f"+{diff}", 5, None)
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

        printText(statsWin, 0, [(self.gear.name, color[self.gear.rarity], "bold")])
        printText(statsWin, 1, [("Description: ", 9, None), (self.gear.description, 9, "bold")]) # current gear
        printText(statsWin, 2, [("Level: ", 9, None), (f"{self.gear.level} ", 9, "bold"), levelDiff])
        printText(statsWin, 3, [(f"Rarity: {self.gear.rarity} ", color[self.gear.rarity], None), rarityDiff])
        if part == Weapon:
            printText(statsWin, 4, [("Damage: ", 9, None), (f"{self.gear.baseDamage} ", 9, "bold"), damageDiff])
        elif part == Armor:
            printText(statsWin, 4, [("Armor: ", 9, None), (f"{self.gear.baseArmor} ", 9, "bold"), armorDiff])
        printText(statsWin, 5, [("Mana: ", 9, None), (f"{self.gear.mana} ", 9, "bold"), manaDiff])
        printText(statsWin, 6, [(separator, 9, None)])
        printText(statsWin, 7, [("Equiped: ", 9, None), (equiped.name, color[equiped.rarity], "bold")]) # equiped gear
        printText(statsWin, 8, [("Level: ", 9, None), (f"{equiped.level}", 9, "bold")])
        printText(statsWin, 9, [(f"Rarity: {equiped.rarity}", color[equiped.rarity], None)])
        if part == Weapon:
            printText(statsWin, 10, [("Damage: ", 9, None), (f"{equiped.baseDamage}", 9, "bold")])
        elif part == Armor:
            printText(statsWin, 10, [("Armor: ", 9, None), (f"{equiped.baseArmor}", 9, "bold")])
        printText(statsWin, 11, [("Mana: ", 9, None), (f"{equiped.mana}", 9, "bold")])
        printText(statsWin, 12, [("Rank: ", 9, None), (f"{equiped.rank}", 9, "bold")])

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
        self.title = self.title.split("\n")
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
            if keyPress(keybind['left']):
                self.selected -= 1
                if self.selected < 0:
                    self.selected = len(self.spells)-1
                getInput = False
            elif keyPress(keybind['right']):
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
        for i, element in enumerate(self.title):
            printText(mainWin, i, [(element, 9, "bold")])
        printText(mainWin, 5, [(separator, 9, None)])
        def offset(x): return ' ' * x
        def sliceSpell(branch, selected = False):
            symbol = branch.spell.symbol
            line1 = [("╔═╩═╗", 9, None)]
            if selected:
                line2 = [("║", 9, None), (fr"{symbol} ", 1, None) , ("║", 9, None)]
            else:
                line2 = [(fr"║{symbol} ║", 9, None)]
            if len(branch.branches) == 0:
                line3 = [("╚═╦═╝", 9, None)]
                line4 = [("     ", 9, None)]
            else:
                line3 = [("╚═╦═╝", 9, None)]
                line4 = [("  ║  ", 9, None)]
            return line1, line2, line3, line4

        selectedList = [False] * (len(self.current.branches)+1)  # +1 for the current spell
        selectedList[self.selected] = True # to set the selected spell in the tree

        n = len(self.current.branches)
        k = (122 - 6*n)//(2*n) # space between squares
        d = 122 - 2*k*n - 6*n # space between the tree and the border
        d1 = d//2 # space before the tree
        d2 = d - d1 # space after the tree

        spell = sliceSpell(self.current, selectedList[0])
        line = 6
        for i in range(len(spell)):
            printText(mainWin, line, [(offset(121//2-2), 9, None)] + spell[i])
            line += 1

        # link between spells
        links = ""
        links += offset(d1+k+2)+"╔"
        for i in range(n-2):
            links += "═"*(2*k+5)
            links += "╦"
        links += "═"*(2*k+5)
        links += "╗"
        links = list(links)
        if n%2 == 0:
            links[121//2] = "╩"
        else:
            links[121//2] = "╬"
        links = "".join(links)
        printText(mainWin, line, [(links, 9, None)])
        line += 1

        # spells
        spells = [sliceSpell(branch, selectedList[i+1]) for i, branch in enumerate(self.current.branches)]
        spellsStr = []

        s = [(offset(d1+k), 9, None)]
        for i in range(4):
            for j in range(n):
                s += spells[j][i]
                s += [(offset(2*k+1), 9, None)]
            s += [(offset(d2+k), 9, None)]
            spellsStr.append(s)
            s = [(offset(d1+k), 9, None)]
        for i in range(len(spellsStr)):
            printText(mainWin, line, spellsStr[i])
            line += 1
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
        super().__init__(title, options, self.onSpace, self.addInfos)
        self.player = player
        self.spell = spell
        self.spellTree = tree

    def addInfos(self):
        clearStats()
        printText(statsWin, 0, [(f"{self.spell.symbol} {self.spell.name}", 9, None)])
        l = 1
        if len(self.spell.description) > 59:
            printText(statsWin, l, [(self.spell.description[:59], 9, None)])
            printText(statsWin, l+1, [(self.spell.description[59:], 9, None)])
            l += 2
        else:
            printText(statsWin, l, [(self.spell.description, 9, None)])
            l += 1
        if self.spell.name in self.player.spells:
            printText(statsWin, l, [("This spell is unlocked", 7, None)])
            l += 1
        elif self.spell.unlock["level"] <= self.player.level:
            printText(statsWin, l, [("This spell can be unlocked", 5, None)])
            printText(statsWin, l+1, [("Level required: ", 9, None), (f"{self.spell.unlock['level']}", 9, "bold")])
            printText(statsWin, l+2, [("Cost: ", 9, None), (f"{self.spell.unlock['cost']}", 2, "bold")])
            l += 3
        else:
            printText(statsWin, l, [("This spell can't be unlocked yet", 4, None)])
            printText(statsWin, l+1, [("Level required: ", 9, None), (f"{self.spell.unlock['level']}", 9, "bold")])
            l += 2
        printText(statsWin, l, [("Mana Cost: ", 9, None), (f"{self.spell.cost}", 6, "bold")])
        l += 1
        if type(self.spell) == DamageSpell:
            printText(statsWin, l, [("Damage: ", 9, None), (f"{int(self.spell.damage+(self.spell.scale*self.player.mana))}", 4, "bold")])
            l += 1
        elif type(self.spell) == HealSpell:
            printText(statsWin, l, [("Heal: ", 9, None), (f"{int(self.spell.heal+(self.spell.scale*self.player.mana))}", 4, "bold")])
            l += 1
        elif type(self.spell) == BuffSpell:
            printText(statsWin, l, [("Heal: ", 9, None), (f"{int(self.spell.heal+(self.spell.scale*self.player.mana))}", 4, "bold")])
            printText(statsWin, l+1, [("Buff: ", 9, None), (f"{self.spell.buff}", 9, "bold")])
            printText(statsWin, l+2, [("Duration: ", 9, None), (f"{self.spell.duration}", 9, "bold")])
            l += 3
        elif type(self.spell) == DebuffSpell:
            printText(statsWin, l, [("Damage: ", 9, None), (f"{int(self.spell.damage+(self.spell.scale*self.player.mana))}", 4, "bold")])
            printText(statsWin, l+1, [("Debuff: ", 9, None), (f"{self.spell.debuff}", 9, "bold")])
            printText(statsWin, l+2, [("Duration: ", 9, None), (f"{self.spell.duration}", 9, "bold")])
            l += 3

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                clearAll()
                printText(mainWin, 0, [(f"{self.spell.symbol} {self.spell.name}", 9, None)])
                l = 1
                if len(self.spell.description) > 59:
                    printText(mainWin, l, [(self.spell.description[:59], 9, None)])
                    printText(mainWin, l+1, [(self.spell.description[59:], 9, None)])
                    l += 2
                else:
                    printText(mainWin, l, [(self.spell.description, 9, None)])
                    l += 1
                if self.spell.name in self.player.spells:
                    printText(mainWin, l, [("This spell is unlocked", 7, None)])
                    l += 1
                elif self.spell.unlock["level"] <= self.player.level:
                    printText(mainWin, l, [("This spell can be unlocked", 5, None)])
                    printText(mainWin, l+1, [("Level required: ", 9, None), (f"{self.spell.unlock['level']}", 9, "bold")])
                    printText(mainWin, l+2, [("Cost: ", 9, None), (f"{self.spell.unlock['cost']}", 2, "bold")])
                    l += 3
                else:
                    printText(mainWin, l, [("This spell can't be unlocked yet", 4, None)])
                    printText(mainWin, l+1, [("Level required: ", 9, None), (f"{self.spell.unlock['level']}", 9, "bold")])
                    l += 2
                printText(mainWin, l, [("Mana Cost: ", 9, None), (f"{self.spell.cost}", 6, "bold")])
                l += 1
                if type(self.spell) == DamageSpell:
                    printText(mainWin, l, [("Damage: ", 9, None), (f"{int(self.spell.damage+(self.spell.scale*self.player.mana))}", 4, "bold")])
                    l += 1
                elif type(self.spell) == HealSpell:
                    printText(mainWin, l, [("Heal: ", 9, None), (f"{int(self.spell.heal+(self.spell.scale*self.player.mana))}", 4, "bold")])
                    l += 1
                elif type(self.spell) == BuffSpell:
                    printText(mainWin, l, [("Heal: ", 9, None), (f"{int(self.spell.heal+(self.spell.scale*self.player.mana))}", 4, "bold")])
                    printText(mainWin, l+1, [("Buff: ", 9, None), (f"{self.spell.buff}", 9, "bold")])
                    printText(mainWin, l+2, [("Duration: ", 9, None), (f"{self.spell.duration}", 9, "bold")])
                    l += 3
                elif type(self.spell) == DebuffSpell:
                    printText(mainWin, l, [("Damage: ", 9, None), (f"{int(self.spell.damage+(self.spell.scale*self.player.mana))}", 4, "bold")])
                    printText(mainWin, l+1, [("Debuff: ", 9, None), (f"{self.spell.debuff}", 9, "bold")])
                    printText(mainWin, l+2, [("Duration: ", 9, None), (f"{self.spell.duration}", 9, "bold")])
                    l += 3
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
                        printInfo([("You don't have enough gold", 9, None)])
                        spaceToContinue()
                else:
                    printInfo([("Your level is to low to unlock this spell", 9, None)])
                    spaceToContinue()
            case 2:
                if self.spellTree.selected == 0:
                    printInfo([("You are already on this spell", 9, None)])
                    spaceToContinue()
                elif len(self.spellTree.current.branches[self.spellTree.selected-1].branches) == 0:
                    printInfo([("This spell doesn't unlock any other spell", 9, None)])
                    spaceToContinue()
                else:
                    if self.spell.name not in self.player.spells:
                        printInfo([("You didn't unlock this spell yet", 9, None)])
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
        super().__init__(title, options, self.onSpace, self.addInfos)
        self.spellTree = spellTree
        self.player = player
        self.enemy = enemy
        self.spell = spell
        self.casted = False

    def addInfos(self):
        clearStats()
        printText(statsWin, 0, [(f"{self.spell.symbol} {self.spell.name}", 9, None)])
        l = 1
        if len(self.spell.description) > 59:
            printText(statsWin, l, [(self.spell.description[:59], 9, None)])
            printText(statsWin, l+1, [(self.spell.description[59:], 9, None)])
            l += 2
        else:
            printText(statsWin, l, [(self.spell.description, 9, None)])
            l += 1
        if self.spell.name in self.player.spells:
            printText(statsWin, l, [("This spell is unlocked", 7, None)])
            l += 1
        elif self.spell.unlock["level"] <= self.player.level:
            printText(statsWin, l, [("This spell can be unlocked", 5, None)])
            printText(statsWin, l+1, [("Level required: ", 9, None), (f"{self.spell.unlock['level']}", 9, "bold")])
            printText(statsWin, l+2, [("Cost: ", 9, None), (f"{self.spell.unlock['cost']}", 2, "bold")])
            l += 3
        else:
            printText(statsWin, l, [("This spell can't be unlocked yet", 4, None)])
            printText(statsWin, l+1, [("Level required: ", 9, None), (f"{self.spell.unlock['level']}", 9, "bold")])
            l += 2
        printText(statsWin, l, [("Mana Cost: ", 9, None), (f"{self.spell.cost}", 6, "bold")])
        l += 1
        if type(self.spell) == DamageSpell:
            printText(statsWin, l, [("Damage: ", 9, None), (f"{int(self.spell.damage+(self.spell.scale*self.player.mana))}", 4, "bold")])
            l += 1
        elif type(self.spell) == HealSpell:
            printText(statsWin, l, [("Heal: ", 9, None), (f"{int(self.spell.heal+(self.spell.scale*self.player.mana))}", 4, "bold")])
            l += 1
        elif type(self.spell) == BuffSpell:
            printText(statsWin, l, [("Heal: ", 9, None), (f"{int(self.spell.heal+(self.spell.scale*self.player.mana))}", 4, "bold")])
            printText(statsWin, l+1, [("Buff: ", 9, None), (f"{self.spell.buff}", 9, "bold")])
            printText(statsWin, l+2, [("Duration: ", 9, None), (f"{self.spell.duration}", 9, "bold")])
            l += 3
        elif type(self.spell) == DebuffSpell:
            printText(statsWin, l, [("Damage: ", 9, None), (f"{int(self.spell.damage+(self.spell.scale*self.player.mana))}", 4, "bold")])
            printText(statsWin, l+1, [("Debuff: ", 9, None), (f"{self.spell.debuff}", 9, "bold")])
            printText(statsWin, l+2, [("Duration: ", 9, None), (f"{self.spell.duration}", 9, "bold")])
            l += 3

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
                    printInfo([("This spell is not unlocked", 4, None)])
                    spaceToContinue()
                elif self.spell.cost > self.player.mana:
                    printInfo([("You don't have enough mana", 7, None)])
                    spaceToContinue()
                elif self.spell.unlock["level"] > self.player.level:
                    printInfo([("Your level is to low to use this spell", 4, None)])
                    spaceToContinue()
                elif self.spell.name in pactRequired and not Fight.haveBuff("pact", self.player):
                    printInfo([("You need to make a pact with a demon to use this spell", 4, None)])
                    spaceToContinue()
                elif self.spell.name in demonizedRequired and not Fight.haveBuff("demonized", self.player):
                    printInfo([("You need in your demon form to use this spell", 4, None)])
                    spaceToContinue()
                elif self.spell.name in self.player.spells:
                    text = self.spell.onUse(self.player, self.getTarget())
                    printMultipleInfo(text)
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

#CRAFT
class ForgeUI(Menu):
    """ForgeUI class, used to create the craft UI"""
    def __init__(self, player, inventory):
        """Constructor for the ForgeUI class, takes in player and inventory"""
        self.player = player
        self.inventory = inventory
        title = open("ascii/craft", "r").read()
        options = ("Weapon", "Armor", "Consumable", "Upgrade", "Back")
        super().__init__(title, options, self.onSpace)

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                SelectItemUI(self.player, self.inventory, "weapon").run()
            case 1:
                SelectItemUI(self.player, self.inventory, "armor").run()
            case 2:
                SelectItemUI(self.player, self.inventory, "item").run()
            case 3:
                UpgradeUI(self.player, self.inventory).run()
            case 4:
                self.runVar = False


class SelectItemUI(Menu):
    """SelectItemUI class, used to create the select item UI"""
    def __init__(self, player, inventory, itemType):
        """Constructor for the SelectItemUI class, takes in player, inventory, and itemType"""
        title = open("ascii/craft", "r").read()
        self.player = player
        self.inventory = inventory
        self.type = itemType
        self.redefineOptions()
        super().__init__(title, self.option, self.onSpace)

    def redefineOptions(self):
        """Redefines the options"""
        self.option = []
        data = json.load(open("data/crafting/recipes.json", "r"))
        for recipe in data[self.type]:
            recipe = data[self.type][recipe]
            if self.type == "weapon":
                if recipe["role"] != self.player.role:
                    continue
            self.option.append(recipe["name"])
        self.option.append("Back")

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        if select == len(self.option) - 1:
            self.runVar = False
        else:
            data = json.load(open("data/crafting/recipes.json", "r"))[self.type][self.option[select]]
            CraftItemUI(self.player, self.inventory, data).run()


class CraftItemUI(Menu):
    """CraftItemUI class, used to create the craft item UI"""
    def __init__(self, player, inventory, item):
        """Constructor for the CraftItemUI class, takes in player, inventory, and item"""
        title = open("ascii/craft", "r").read()
        options = ("Craft", "Back")
        self.player = player
        self.inventory = inventory
        self.item = item #dict of the item to craft
        self.moneyCost = self.player.level * 100
        super().__init__(title, options, self.onSpace, self.addInfos)

    def addInfos(self):
        """Adds the infos of the item to craft"""
        clearStats()
        printText(statsWin, 0, [(f"{self.item['name']}", 9, "bold")])
        printText(statsWin, 1, [("Cost: ", 9, None)])
        for i, element in enumerate(self.item["recipe"]):
            printText(statsWin, 2+i, [(f"- {element}", 9, None)])
        printText(statsWin, 4, [(f"- {self.moneyCost} gold", 2, None)])

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        match select:
            case 0:
                haveItem1 = self.item["recipe"][0] in self.inventory.getExistingItems()
                haveItem2 = self.item["recipe"][1] in self.inventory.getExistingItems()
                if self.player.gold >= self.moneyCost and haveItem1 and haveItem2:
                    for i in range(2):
                        item = Item(self.item["recipe"][i], "", 0, 0) #simulate the item used in the craft
                        self.inventory.removeItem(item)
                    self.player.gold -= self.moneyCost
                    if self.item["type"] == "weapon":
                        example = randomWeapon(self.player.role, self.player.level)
                        item = Weapon(self.item["name"], self.item["description"], example.level, int(example.baseDamage*1.1), example.rarity, int(example.mana*1.1))
                    elif self.item["type"] == "armor":
                        example = randomArmor(self.player.role, self.player.level)
                        item = Armor(self.item["name"], self.item["description"], example.level, int(example.baseArmor*1.1), example.rarity, int(example.mana*1.1))
                    self.inventory.addGear(item)
                    printInfo([("Item crafted", 9, None)])
                    spaceToContinue()
                else:
                    if self.player.gold < self.moneyCost:
                        printInfo([("You don't have enough money", 4, None)])
                    if not haveItem1 or not haveItem2:
                        printInfo([("You don't have the required items", 4, None)])
                    spaceToContinue()
            case 1:
                self.runVar = False


class UpgradeUI(Menu):
    """UpgradeUI class, used to create the upgrade UI"""
    def __init__(self, player, inventory):
        """Constructor for the UpgradeUI class"""
        title = open("ascii/craft", "r").read()
        self.player = player
        self.inventory = inventory
        self.redifineOptions()
        super().__init__(title, self.option, self.onSpace, self.addInfos)

    def redifineOptions(self):
        """Redefines the options"""
        self.option = []
        self.option.append(self.player.weapon.name)
        self.option.append(self.player.armor.name)
        for gear in self.inventory.gear:
            if gear != None:
                self.option.append(gear.name)
            else:
                self.option.append("Empty")
        self.option.append("Back")

    def getGear(self):
        """Gets the selected gear"""
        if self.select == 0:
            return self.player.weapon
        elif self.select == 1:
            return self.player.armor
        elif self.select >= 2 and self.select-2 < len(self.inventory.gear):
            return self.inventory.gear[self.select-2]
        else:
            return None

    def addInfos(self):
        """Adds the infos of the item to upgrade"""
        clearStats()
        printInfo([("Select an item to upgrade", 9, None)])
        selected = self.getGear()
        if selected != None:
            printText(statsWin, 0, [(selected.name, color[selected.rarity], "bold")])
            printText(statsWin, 1, [("Description: ", 9, None), (selected.description, 9, "bold")]) # current gear
            printText(statsWin, 2, [("Level: ", 9, None), (str(selected.level), 9, "bold")])
            printText(statsWin, 3, [(f"Rarity: {selected.rarity}", color[selected.rarity], None)])
            if type(selected) == Weapon:
                printText(statsWin, 4, [("Damage: ", 9, None), (str(selected.baseDamage), 9, "bold")])
            elif type(selected) == Armor:
                printText(statsWin, 4, [("Armor: ", 9, None), (str(selected.baseArmor), 9, "bold")])
            printText(statsWin, 5, [("Mana: ", 9, None), (str(selected.mana), 9, "bold")])
            printText(statsWin, 6, [(f"Rank: {selected.rank}", 9, "bold")])
            cost = selected.rank * selected.level * selected.rarity * 10
            printText(statsWin, 7, [("Upgrade Cost: ", 9, None), (str(cost), 2, "bold")])

    def onSpace(self, select):
        """Function called when the spacebar is pressed"""
        if select == len(self.option) - 1:
            self.runVar = False
        else:
            gear = self.getGear()
            if gear != None:
                cost = gear.rank * gear.level * gear.rarity * 10
                if self.player.gold >= cost:
                    self.player.gold -= cost
                    gear.upgrade()
                    printInfo([("Gear upgraded", 9, None)])
                    printInfo([("You have ", 9, None), (str(self.player.gold), 2, "bold"), (" gold left", 9, None)])
                    spaceToContinue()
                else:
                    printInfo([("You don't have enough gold", 4, None)])
                    printInfo([("You need ", 9, None), (str(cost - self.player.gold), 9, "bold"), (" more gold", 9, None)])
                    spaceToContinue()


class Game:
    """Game class, main class of the game that contains the player and the current room"""
    def __init__(self, new = True, role = None):
        """Constructor for the Game class, takes in new and role"""
        #data recovery
        def recovery():
            """Recovers the data from the zip file"""
            rmtree("data")
            zipf = zipfile.ZipFile(f"recovery.dc", "r", zipfile.ZIP_DEFLATED)
            zipf.extractall()
            zipf.close()
        if not os.path.exists("recovery.dc"):
            raise Exception("Recovery file not found. Please reinstall the game")
        recovery()
        #end of data recovery
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
                clearStats()
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
                    pickedUp = self.player.inventory.addGear(item)
                else:
                    pickedUp = self.player.inventory.addItem(item)
                if not pickedUp:
                    printInfo([("Your inventory is full", 9, None)])
                self.player.gold += money
                printInfo([("You found ", 9, None), (item.name, color[item.rarity], "bold"), (f" and {money} gold in the treasure", 9, None)])
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
                    printInfo([("You loot ", 9, None), (element.loot.name, color[element.loot.rarity], "bold")])
                    self.player.exp += element.exp
                    self.player.gold += element.gold
                    self.player.inventory.addItem(element.loot)
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
                    printInfo([("You lose half of your experience and level", 9, None)])
                    self.player.exp = self.player.exp//2
                    self.player.level = self.player.level//2
                    if self.player.level < 1:
                        self.player.level = 1
                    if self.player.exp < 0:
                        self.player.exp = 0
                clearStats()
                self.save()
                spaceToContinue()
            elif element == "C": #if there is a chest open it
                InventoryUI(self.player.inventory, self.player).run()
                self.save()
            elif element == "G": #if there is a grimoire use it to see the spell tree
                SpellTree(self.player.role, self.player).run()
                self.save()
            elif element == "S": #if there is a shop open it
                Shop(self.player).run()
                self.save()
            elif element == "F":
                ForgeUI(self.player, self.player.inventory).run()
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
                        printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to go back to the ", 9, None), ("Lobby", 7, "bold")])
                    else:
                        printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to go to the next ", 9, None), ("floor", 4, "bold")])
            elif type(element) == Enemy:
                printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to start the ", 9, None), ("fight", 4, "bold")])
            elif type(element) == Treasure:
                printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to open the ", 9, None), ("treasure", 2, "bold")])
            elif element == "C":
                printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to open your ", 9, None), ("inventory", 2, "bold")])
            elif element == "G":
                printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to see your ", 9, None), ("spell tree", 3, "bold")])
            elif element == "S":
                printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to open the ", 9, None), ("shop", 2, "bold")])
            elif element == "F":
                printInfo([("Press ", 9, None), ("˽", 9, "bold"), (" to open the ", 9, None), ("forge", 7, "bold")])

    def playerMove(self, direction):
        """Player Movement Handler. Move the player in the room depending on the direction"""
        coord = self.currentRoom.getPlayerCoord()
        move = False
        match direction:
            case'up':
                if self.currentRoom.map[coord[0] - 1][coord[1]] == '.':
                    self.currentRoom.map[coord[0]][coord[1]] = '.'
                    self.currentRoom.map[coord[0] - 1][coord[1]] = self.player
                    move = True
            case 'down':
                if self.currentRoom.map[coord[0] + 1][coord[1]] == '.':
                    self.currentRoom.map[coord[0]][coord[1]] = '.'
                    self.currentRoom.map[coord[0] + 1][coord[1]] = self.player
                    move = True
            case 'left':
                if self.currentRoom.map[coord[0]][coord[1] - 1] == '.':
                    self.currentRoom.map[coord[0]][coord[1]] = '.'
                    self.currentRoom.map[coord[0]][coord[1] - 1] = self.player
                    move = True
            case 'right':
                if self.currentRoom.map[coord[0]][coord[1] + 1] == '.':
                    self.currentRoom.map[coord[0]][coord[1]] = '.'
                    self.currentRoom.map[coord[0]][coord[1] + 1] = self.player
                    move = True
        # while keyboard.is_pressed(direction): #wait for the key to be released
        #     pass
        sleep(0.1) if move else None #delay to avoid multiple key press
        self.printRoom()

    def printRoom(self):
        """Prints the room and all infos -> called after every player action"""
        #print current room name
        if type(self.currentRoom) == Lobby:
            text = "Lobby"
            printText(statsWin, 0, [("Current Room: ", 9, None), (text, 6, "bold")])
        else:
            text = f"Dungeon: Floor {self.lobby.dungeon.floor + 1} of {len(self.lobby.dungeon.rooms)}"
            printText(statsWin, 0, [("Current Room: ", 9, None), (text, 3, "bold")])
        printText(statsWin, 1, [(separator, 9, None)])
        printText(statsWin, 2, [(f"Gold: {self.player.gold}", 2, None)])
        if self.currentRoom == self.lobby:
            mist = False
        else:
            mist = True
        self.currentRoom.render = self.currentRoom.colorMap(mist=mist)
        printMap(self.currentRoom.render)

        #print player info
        printText(statsWin, 3, [(separator, 9, None)])
        healthText = f'Health: {self.player.health}/100'
        manaText = f'Mana: {self.player.mana}/{self.player.maxMana}'
        textSpace = " " * (59 - len(healthText) - len(manaText))
        healthBar = bar(self.player.health, 100)
        manaBar = bar(self.player.mana, self.player.maxMana, reversed=True)
        barSpace = " " * (59 - len(healthBar) - len(manaBar))
        printText(statsWin, 4, [(healthText, 4, None), (textSpace, 9, None), (manaText, 6, None)])
        printText(statsWin, 5, [(healthBar, 4, None), (barSpace, 9, None), (manaBar, 6, None)])
        printText(statsWin, 6, [(separator, 9, None)])
        expText = f'Exp: {self.player.exp}/{(self.player.level*5)**2}'
        levelText = f'Level: {self.player.level}'
        whiteSpace = " " * (59 - len(expText) - len(levelText))
        expBar = bar(self.player.exp, (self.player.level*10)**2, length=57)
        printText(statsWin, 7, [(expText, 2, None), (whiteSpace, 9, None), (levelText, 2, None)])
        printText(statsWin, 8, [(expBar, 2, None)])
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
                self.printRoom()


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
        clearInfo()
        #player turn
        if self.player.health > 0:
            self.playerTurn()
        #purify effect (player only)
        if self.haveBuff("purify", self.player):
            self.player.debuff = []
            printInfo(["You ", 5, None], ["are purified ! All debuffs are removed", 9, None])
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
            printInfo([("You ", 5, None), ("are poisoned and lose ", 9, None), ("5 health", 4, None)])
            p = True
        if self.haveDebuff("poison", self.enemy):
            self.enemy.health -= 5
            printInfo([(self.enemy.name, 3, None), (" is poisoned and loses ", 9, None), ("5 health", 4, None)])
            p = True
        if p:
            spaceToContinue()

        #burn effect
        b = False
        if self.haveDebuff("burn", self.player):
            self.player.health -= 5
            printInfo([("You ", 5, None), ("are burning and lose ", 9, None), ("5 health", 4, None)])
            b = True
        if self.haveDebuff("burn", self.enemy):
            self.enemy.health -= 5
            printInfo([(self.enemy.name, 3, None), (" is burning and loses ", 9, None), ("5 health", 4, None)])
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
            printInfo([("You ", 5, None), ("are revived !", 9, None)])
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
            printMultipleInfo(text)
        else:
            printInfo([(self.enemy.name, 3, None), (" has exhausted all his mana and can't cast any spell", 9, None)])

    def enemyTurn(self):
        """Enemy Turn Handler. Manages the enemy turn"""
        if self.haveDebuff("stun", self.enemy):
            printInfo([(self.enemy.name, 3, None), (" is stunned and can't do anything", 9, None)])
        else:
            printInfo([(self.enemy.name, 3, "bold"), ("'s turn", 9, "bold")])
            randomAction = random.randint(1, 2)
            match randomAction:
                case 1:
                    self.evalDamage(self.enemy, self.player)
                case 2:
                    printInfo([(self.enemy.name, 3, None), (" uses a spell", 9, None)])
                    if self.haveBuff("invulnerable", self.player):
                        printInfo([("You ", 5, None), ("are invulnerable !", 9, None)])
                        printInfo([(self.enemy.name, 3, None), ("'s spell has no effect on ", 5, None), ("You", 5, None)])
                    else:
                        self.enemySpell()
        spaceToContinue()

    def playerTurn(self):
        """Player Turn Handler. Manages the player turn"""
        if self.haveDebuff("stun", self.player):
            printInfo([("You ", 5, None), ("are stunned and can't do anything", 9, None)])
        else:
            #player choose an action
            printInfo([("Choose an action", 9, None)])
            printInfo([("1. Attack    2. Spell    3. Item    4. Run", 9, None)])
            getInput = True
            while getInput:
                if keyPress('1'): #attack
                    self.evalDamage(self.player, self.enemy)
                    getInput = False
                    spaceToContinue()
                elif keyPress('2'): #skill
                    if len(self.player.spells) == 0:
                        printInfo([("You ", 5, None), ("don't have any spell", 9, None)])
                        spaceToContinue()
                        self.print()
                        self.playerTurn()
                    else:
                        if self.haveBuff("invulnerable", self.enemy):
                            printInfo([(self.enemy.name, 3, None), (" is invulnerable !", 9, None)])
                            printInfo([("Your spell has no effect on him", 9, None)])
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
                        printInfo([("You ", 5, None), ("don't have any item", 9, None)])
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
                    printInfo([("You ", 5, None), ("try to flee", 9, None)])
                    flee = random.randint(1, 2)
                    if flee == 1:
                        printInfo([("You ", 5, None), ("successfully flee", 9, None)])
                        self.flee = True
                    else:
                        printInfo([("You ", 5, None), ("failed to flee", 9, None)])
                    getInput = False
        if self.player.mana < self.player.maxMana:
            self.player.mana += self.player.maxMana // 20
            if self.player.mana > self.player.maxMana:
                self.player.mana = self.player.maxMana
        if self.haveBuff("purify", self.player):
            self.player.debuff = []
            printInfo([("You ", 5, None), ("are purified ! All debuffs are removed", 9, None)])

    def evalDamage(self, user, target):
        """Evaluates the damage dealt by the user to the target and applies it"""
        if self.haveBuff("invulnerable", target):
            if user == self.player:
                printInfo([(target.name, 3, None), (" is invulnerable !", 9, None)])
                printInfo([("Your attack has no effect on him", 9, None)])
            else:
                printInfo([("You ", 5, None), ("are invulnerable !", 9, None)])
                printInfo([(user.name, 3, None), ("'s attack has no effect on ", 5, None), ("You", 5, None)])
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
                printInfo([("You ", 5, None), ("deal ", 9, None), (f"{atk} damage", 4, None), (" to ", 9, None), (target.name, 3, None)])

                if self.haveBuff("vampirism", user):
                    user.health += atk // 4
                    if user.health > 100:
                        user.health = 100
                    printInfo([("You ", 5, None), ("gain ", 9, None), (f"{atk // 4} health", 4, None), (" from ", 9, None), (target.name, 3, None), ("'s blood", 9, None)])
            else:
                printInfo([(user.name, 3, None), (" attacks you and deals ", 9, None), (f"{atk} damage", 4, None), (" to ", 9, None), ("You", 5, None)])

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
        clearAll()
        #print enemy info
        printText(statsWin, 0, [("Enemy: ", 9, None), (f"{self.enemy.name} - {self.enemy.type}", 3, None)])
        healthText = f'Health: {self.enemy.health}/100'
        printText(statsWin, 1, [(healthText, 4, None)])
        healthBar = bar(self.enemy.health, 100)
        printText(statsWin, 2, [(healthBar, 4, None)])
        buffList = [element[0] for element in self.enemy.buff]
        printText(statsWin, 3, [(f"Buff: {buffList}", 9, None)])
        debuffList = [element[0] for element in self.enemy.debuff]
        printText(statsWin, 4, [(f"Debuff: {debuffList}", 9, None)])
        self.enemy.render()
        #print player info
        printText(statsWin, 5, [(separator, 9, None)])
        printText(statsWin, 6, [("You: ", 5, None)])
        healthText = f'Health: {self.player.health}/100'
        manaText = f'Mana: {self.player.mana}/{self.player.maxMana}'
        textSpace = " " * (59 - len(healthText) - len(manaText))
        healthBar = bar(self.player.health, 100)
        manaBar = bar(self.player.mana, self.player.maxMana, reversed=True)
        barSpace = " " * (59 - len(healthBar) - len(manaBar))
        printText(statsWin, 7, [(healthText, 4, None), (textSpace, 9, None), (manaText, 6, None)])
        printText(statsWin, 8, [(healthBar, 4, None), (barSpace, 9, None), (manaBar, 6, None)])
        buffList = [element[0] for element in self.player.buff]
        printText(statsWin, 9, [(f"Buff: {buffList}", 9, None)])
        debuffList = [element[0] for element in self.player.debuff]
        printText(statsWin, 10, [(f"Debuff: {debuffList}", 9, None)])
