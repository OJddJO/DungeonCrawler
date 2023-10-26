from classes.Item import Weapon

class Player:
    def __init__(self, role = "warrior", weapon = None, armor = None, level = 1, exp = 0, health = 100, mana = 100):
        if weapon == None:
            weapon = Weapon("Starter Stick", "A simple stick to start your adventure", 1, 5, 1, 0)
        self.health = health
        self.mana = mana
        self.exp = exp
        self.level = level
        self.role = role # warrior, mage, archer
        self.weapon = weapon
        self.armor = armor
