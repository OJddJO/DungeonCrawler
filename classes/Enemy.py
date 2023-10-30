from classes.Item import randomWeapon, randomArmor
import random

class Enemy:
    def __init__(self, name, type, level, coord):
        self.name = name
        self.type = type
        self.health = 100
        self.weapon = randomWeapon("warrior", level)
        self.armor = randomArmor("warrior", level-1)
        self.exp = random.randint(1, 10)*level
        self.level = level
        self.coord = coord
        self.buff = []
        self.debuff = []

    def render(self):
        with open(f"ascii/enemies/{self.type}", "r") as f:
            print(f.read())