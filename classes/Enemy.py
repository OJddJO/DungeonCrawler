class Enemy:
    def __init__(self, name, health, damage, exp, armor = None):
        self.name = name
        self.health = health
        self.damage = damage
        self.armor = armor
        self.exp = exp
