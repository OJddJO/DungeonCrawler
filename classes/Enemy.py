from classes.Item import randomWeapon, randomArmor
import random
from cursesInit import *

class Enemy:
    """Enemy class, used to create enemies for the player to fight"""
    def __init__(self, name, type, level, coord):
        """Constructor for the Enemy class, takes in name, type, level, and coord"""
        self.name = name
        self.type = type
        self.health = 100
        self.mana = 100 + 20*(level-1)
        self.spells = ["Fireball", "Supernova", "Flamestrike", "Gravity Well", "Gravity Crush", "Atomic Burst", "Frost Nova", "Ice Lance", "Avalanche", "Magic Missile", "Heal"]
        self.weapon = randomWeapon("warrior", level)
        self.armor = randomArmor("mage", level-1)
        self.exp = random.randint(1, 5)*level
        self.gold = random.randint(1, 10)*level
        self.level = level
        self.coord = coord
        self.buff = []
        self.debuff = []

    def render(self):
        """Renders the enemy's ascii art"""
        with open(f"ascii/enemies/{self.type}", "r") as f:
            textList = f.readlines()
            textList = [[(str(line), 9, None)] for line in textList]
            printMultipleText(mainWin, 0, textList)
