from classes.Item import randomWeapon
import random

class Enemy:
    def __init__(self, name, level, coord):
        self.name = name
        self.health = 100
        self.weapon = randomWeapon("warrior", level)
        self.armor = None
        self.exp = random.randint(1, 10)*level
        self.level = level
        self.coord = coord
