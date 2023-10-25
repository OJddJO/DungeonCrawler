class Item:
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value


class Weapon(Item):
    def __init__(self, name, description, value, level, damage, rarity, mana = 0):
        super().__init__(name, description, value)
        self.baseDamage = damage
        self.level = level
        self.rarity = rarity
        self.value = value * level
        self.trueDamage = damage + level*2
        self.mana = mana

    def onUse(self):
        return self.trueDamage


class Armor(Item):
    def __init__(self, name, description, value, armor):
        super().__init__(name, description, value)
        self.baseArmor = armor

