import os
import json
from classes.Item import Weapon, Armor
from datetime import datetime

baseWeapon = Weapon("Starter Stick", "A simple stick to start your adventure", 1, 10, 1, 0)
baseArmor = Armor("Starter Hide", "A simple armor to start your adventure", 1, 5, 1, 0)
class Player:
    def __init__(self, role = None, weapon = baseWeapon, armor = baseArmor, level = 1, exp = 0, gold = 0, health = 100, mana = 100, spells = []):
        self.name = "You"
        self.health = health
        self.exp = exp
        self.gold = gold
        self.level = level
        self.role = role # warrior, mage, archer
        self.weapon = weapon
        self.armor = armor
        self.mana = mana
        self.spells = spells
        self.maxMana = 100 + self.armor.mana + self.weapon.mana
        self.inventory = Inventory()
        self.buff = []
        self.debuff = []

    def loadData(self):
        try:
            if os.path.exists('save/stats.json'):
                with open('save/stats.json', 'r') as f:
                    data = json.load(f)
                    self.health = data['health']
                    self.mana = data['mana']
                    self.exp = data['exp']
                    self.gold = data['gold']
                    self.level = data['level']
                    self.role = data['role']
                    self.spells = data['spells']
                    self.weapon = Weapon(data['weapon']['name'], data['weapon']['description'], data['weapon']['level'], data['weapon']['damage'], data['weapon']['rarity'], data['weapon']['mana'])
                    self.armor = Armor(data['armor']['name'], data['armor']['description'], data['armor']['level'], data['armor']['armor'], data['armor']['rarity'], data['armor']['mana'])
            else:
                raise Exception("No save file found")
        except:
            raise Exception("Save file corrupted")
        
    def save(self):
        with open("save/stats.json", "w") as f:
            json.dump({
                "health": self.health,
                "mana": self.mana,
                "exp": self.exp,
                "gold": self.gold,
                "level": self.level,
                "role": self.role,
                "weapon": self.weapon.__dict__(),
                "armor": self.armor.__dict__(),
                "spells": self.spells,
                "date": datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
            }, f)


class Inventory:
    def __init__(self):
        self.items = [[None, 0]] * 20 # (item, quantity)
        self.gear = [None] * 20 # max 20 gear

    def loadData(self):
        try:
            if os.path.exists('save/inventory.json'):
                with open('save/inventory.json', 'r') as f:
                    data = json.load(f)
                    self.gear = []
                    for element in data['gear']: # GEAR
                        if element == None:
                            self.gear.append(None)
                        elif element['type'] == "weapon":
                            self.gear.append(Weapon(element['name'], element['description'], element['level'], element['damage'], element['rarity'], element['mana']))
                        elif element['type'] == "armor":
                            self.gear.append(Armor(element['name'], element['description'], element['level'], element['armor'], element['rarity'], element['mana']))
                    # ITEM
            else:
                raise Exception("No save file found")
        except:
            raise Exception("Save file corrupted")
    
    def save(self):
        #decompose each item and gear to json to save
        data = {
            "items": [],
            "gear": []
        }
        for element in self.gear: # GEAR
            if element == None:
                data['gear'].append(None)
            else:
                data['gear'].append(element.__dict__())
        # ITEM
        json.dump(data, open('save/inventory.json', 'w'), indent=4)

    def addItem(self, item, quantity = 1):
        existingItem = [element[0] for element in self.items]
        if item in existingItem:
            self.items[existingItem.index(item)][1] += quantity
            return True
        elif [None, 0] in self.items:
            self.items[self.items.index([None, 0])] = [item, quantity]
            return True
        else:
            print("Item inventory full. You didn't pick up the item.")
            return False
        
    def removeItem(self, item, quantity = 1):
        existingItem = [element[0] for element in self.items]
        if item in existingItem:
            i = existingItem.index(item)
            self.items[i][1] -= quantity
            if self.items[i][1] <= 0:
                self.items[i] = [None, 0]
            return item
        else:
            return False
        
    def addGear(self, gear):
        if None in self.gear:
            self.gear[self.gear.index(None)] = gear
            return gear
        else:
            print("Gear inventory full. You didn't pick up the gear.")
            return False
        
    def removeGear(self, gear):
        if gear in self.gear:
            self.gear[self.gear.index(gear)] = None
            return gear
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
