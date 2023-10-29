from classes.Item import Weapon
import os
import json

class Player:
    def __init__(self, role = "warrior", weapon = None, armor = None, level = 1, exp = 0, health = 100, mana = 100):
        if weapon == None:
            weapon = Weapon("Starter Stick", "A simple stick to start your adventure", 1, 10, 1, 0)
        self.health = health
        self.mana = mana
        self.exp = exp
        self.level = level
        self.role = role # warrior, mage, archer
        self.weapon = weapon
        self.armor = armor
        self.inventory = Inventory()

    def loadData(self):
        if os.path.exists("save/stats.json"):
            with open("save/stats.json", "r") as f:
                data = json.load(f)
                self.health = data["health"]
                self.mana = data["mana"]
                self.exp = data["exp"]
                self.level = data["level"]
                self.role = data["role"]
                self.weapon = data["weapon"]
                self.armor = data["armor"]


class Inventory:
    def __init__(self):
        self.items = [[None, 0]] * 20 # (item, quantity)
        self.gear = [None] * 20 # max 20 gear
        self.gold = 0

    def loadData(self):
        if os.path.exists("save/inventory.json"):
            with open("save/inventory.json", "r") as f:
                data = json.load(f)
                self.items = data["items"]
                self.gear = data["gear"]
                self.gold = data["gold"]
        else:
            return False

    def addItem(self, item, quantity = 1):
        if item in [element[0] for element in self.items]:
            self.items[item][1] += quantity
            return True
        elif [None, 0] in self.items:
            self.items[self.items.index([None, 0])] = [item, quantity]
            return True
        else:
            return False
        
    def removeItem(self, item, quantity = 1):
        if item in [element[0] for element in self.items]:
            self.items[item][1] -= quantity
            if self.items[item][1] <= 0:
                self.items[item] = [None, 0]
            return item
        else:
            return False
        
    def addGear(self, gear):
        if None in self.gear:
            self.gear[self.gear.index(None)] = gear
            return gear
        else:
            return False
        
    def removeGear(self, gear):
        if gear in self.gear:
            self.gear[self.gear.index(gear)] = None
            return gear
        else:
            return False
        
    def addGold(self, gold):
        self.gold += gold

    def removeGold(self, gold):
        if self.gold >= gold:
            self.gold -= gold
            return gold
        else:
            return False

    def getItem(self, item):
        if item in [element[0] for element in self.items]:
            return self.items[item]
        else:
            return False

    def getGear(self, gear):
        if gear in self.gear:
            return self.gear[gear]
        else:
            return False
        
    def getGold(self):
        return self.gold