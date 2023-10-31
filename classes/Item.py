import json
import random

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description


class Weapon(Item):
    def __init__(self, name, description, level, damage, rarity, mana):
        super().__init__(name, description)
        self.baseDamage = damage
        self.level = level
        self.rarity = rarity
        self.mana = mana

    def onUse(self):
        return self.baseDamage

    def __dict__(self):
        return {
            "type": "weapon",
            "name": self.name,
            "description": self.description,
            "level": self.level,
            "damage": self.baseDamage,
            "rarity": self.rarity,
            "mana": self.mana
        }


class Armor(Item):
    def __init__(self, name, description, level, armor, rarity):
        super().__init__(name, description)
        self.baseArmor = armor
        self.level = level
        self.rarity = rarity

    def onUse(self):
        return self.baseArmor
    
    def __dict__(self):
        return {
            "type": "armor",
            "name": self.name,
            "description": self.description,
            "level": self.level,
            "armor": self.baseArmor,
            "rarity": self.rarity
        }


class Treasure:
    def __init__(self, role, level, coord):
        self.role = role
        self.level = level
        self.gold = random.randint(1, 10)*level
        self.coord = coord

    def randomLoot(self):
        #give random loot depending on the role and the level
        lootTable = [randomWeapon(self.role, self.level), randomArmor(self.role, self.level)]
        return random.choice(lootTable)


def randomWeapon(role, level):
    if role not in ["warrior", "mage", "archer"]:
        raise KeyError("Invalid role")
    else:
        if role == "warrior":
            key = "swords"
            damageMultiplier = 1 #polyvalent
            manaMultiplier = 1
        elif role == "mage":
            key = "staves"
            damageMultiplier = 0.5 #relies on skill
            manaMultiplier = 1.5
        elif role == "archer":
            key = "bows"
            damageMultiplier = 1.5 #relies on true damage
            manaMultiplier = 0.5
    with open("data/weapon.json", "r") as f:
        data = json.load(f)

    weapon = random.choice(data[key])
    rarity = [1]*10 + [2]*7 + [3]*5 + [4]*3 + [5] + [6]
    random.shuffle(rarity)
    rarity = random.choice(rarity) # 1 = common 2 = uncommon 3 = rare 4 = epic 5 = legendary 6 = mythic
    baseDamage = int(random.randint(5, 15)*level*damageMultiplier)
    modifier = int(baseDamage*rarity*0.5)
    baseDamage += modifier

    mana = int(random.randint(0, 10)*manaMultiplier)
    modifier = int(mana*rarity)
    mana += modifier

    return Weapon(weapon["name"], weapon["description"], level, baseDamage, rarity, mana)


def randomArmor(role, level):
    if role not in ["warrior", "mage", "archer"]:
        raise KeyError("Invalid role")
    else:
        if role == "warrior":
            key = "chestplates"
            armorMultiplier = 1.5 #polyvalent
        elif role == "mage":
            key = "robes"
            armorMultiplier = 0.5 #relies on skill
        elif role == "archer":
            key = "tunics"
            armorMultiplier = 1
    with open("data/armor.json", "r") as f:
        data = json.load(f)

    armor = random.choice(data[key])
    rarity = [1]*10 + [2]*7 + [3]*5 + [4]*3 + [5] + [6]
    random.shuffle(rarity)
    rarity = random.choice(rarity) # 1 = common 2 = uncommon 3 = rare 4 = epic 5 = legendary 6 = mythic
    baseArmor = int(random.randint(1, 10)*(level/2)*armorMultiplier)
    modifier = int(baseArmor*rarity*0.5)
    baseArmor += modifier

    return Armor(armor["name"], armor["description"], level, baseArmor, rarity)


if __name__ == '__main__':
    weapon = randomWeapon("warrior", 1)
    print(f"{weapon.name} - {weapon.description} - {weapon.baseDamage} - {weapon.mana} - {weapon.rarity}")
