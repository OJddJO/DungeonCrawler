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
    def __init__(self, name, description, armor):
        super().__init__(name, description)
        self.baseArmor = armor


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
    modifier = int(mana*rarity*0.5)
    mana = int((mana + modifier))

    return Weapon(weapon["name"], weapon["description"], level, baseDamage, rarity, mana)

if __name__ == '__main__':
    weapon = randomWeapon("warrior", 3)
    print(f"{weapon.name} - {weapon.description} - {weapon.trueDamage} - {weapon.mana} - {weapon.rarity}")
