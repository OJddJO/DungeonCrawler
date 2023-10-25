from classes.Item import randomWeapon

class Player:
    def __init__(self, role = "warrior", weapon = None, armor = None, level = 1, exp = 0, health = 100, mana = 100):
        if weapon == None:
            weapon = randomWeapon(role, 1)
        self.health = health
        self.mana = mana
        self.exp = exp
        self.level = level
        self.role = role # warrior, mage, archer
        self.weapon = weapon
        self.armor = armor
