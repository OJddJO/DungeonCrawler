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
        self.trueDamage = damage + level*2
        self.mana = mana

    def onUse(self):
        return self.trueDamage


class Armor(Item):
    def __init__(self, name, description, level, armor, rarity):
        super().__init__(name, description)
        self.baseArmor = armor
        self.trueArmor = armor
        self.level = level
        self.rarity = rarity

    def onUse(self):
        return self.trueArmor


class Treasure:
    def __init__(self, role, level, coord):
        self.role = role
        self.level = level
        self.gold = random.randint(1, 10)*level
        self.coord = coord

    def randomLoot(self):
        #give random loot depending on the role and the level
        if self.role not in ["warrior", "mage", "archer"]:
            raise KeyError("Invalid role")
        else:
            if self.role == "warrior":
                weapon = "swords"
                armor = "chestplates"
            elif self.role == "mage":
                weapon = "staves"
                armor = "robes"
            elif self.role == "archer":
                weapon = "bows"
                armor = "tunics"
        with open("data/weapon.json", "r") as f:
            weaponData = json.load(f)
        with open("data/armor.json", "r") as f:
            armorData = json.load(f)
        lootTable = [randomWeapon(self.role, self.level), randomArmor(self.role, self.level)]
        return random.choice(lootTable)


def randomWeapon(role, level):
    if role not in ["warrior", "mage", "archer"]:
        raise KeyError("Invalid role")
    else:
        if role == "warrior":
            key = "swords"
        elif role == "mage":
            key = "staves"
        elif role == "archer":
            key = "bows"
    with open("data/weapon.json", "r") as f:
        data = json.load(f)

    weapon = random.choice(data[key])
    rarity = [1]*10 + [2]*7 + [3]*5 + [4]*3 + [5] + [6]
    random.shuffle(rarity)
    rarity = random.choice(rarity) # 1 = common 2 = uncommon 3 = rare 4 = epic 5 = legendary 6 = mythic
    baseDamage = random.randint(1, 10)*level
    modifier = int(baseDamage*rarity*0.5)
    baseDamage += modifier

    mana = random.randint(0, 10)
    modifier = int(mana*rarity)
    mana = int((mana + modifier))

    return Weapon(weapon["name"], weapon["description"], level, baseDamage, rarity, mana)


def randomArmor(role, level):
    if role not in ["warrior", "mage", "archer"]:
        raise KeyError("Invalid role")
    else:
        if role == "warrior":
            key = "chestplates"
        elif role == "mage":
            key = "robes"
        elif role == "archer":
            key = "tunics"
    with open("data/armor.json", "r") as f:
        data = json.load(f)
        
    armor = random.choice(data[key])
    rarity = [1]*10 + [2]*7 + [3]*5 + [4]*3 + [5] + [6]
    random.shuffle(rarity)
    rarity = random.choice(rarity) # 1 = common 2 = uncommon 3 = rare 4 = epic 5 = legendary 6 = mythic
    baseArmor = int(random.randint(1, 10)*(level/2))
    modifier = int(baseArmor*rarity)
    baseArmor += modifier

    return Armor(armor["name"], armor["description"], level, baseArmor, rarity)


if __name__ == '__main__':
    weapon = randomWeapon("warrior", 1)
    print(f"{weapon.name} - {weapon.description} - {weapon.trueDamage} - {weapon.mana} - {weapon.rarity}")
