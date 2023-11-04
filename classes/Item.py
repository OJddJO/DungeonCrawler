import json
import random

color = {
    1: "\033[1;37m",
    2: "\033[1;36m",
    3: "\033[1;34m",
    4: "\033[1;35m",
    5: "\033[1;33m",
    6: "\033[1;31m"
}
rarities = {
    1: "Common",
    2: "Uncommon",
    3: "Rare",
    4: "Epic",
    5: "Legendary",
    6: "Mythic"
}

class Item:
    def __init__(self, name, description, rarity, value):
        self.name = name
        self.description = description
        self.rarity = rarity
        self.value = value
    
    def __str__(self):
        text = f"{color[self.rarity]}{self.name}\033[0m\n"
        text += f"{self.description}\n"
        text += f"Rarity: {color[self.rarity]+rarities[self.rarity]}\033[0m\n"
        text += f"Value: {self.value}"
        return text


class HealItem(Item):
    def __init__(self, name, description, health, mana, rarity, value):
        super().__init__(name, description, rarity, value)
        self.health = health
        self.mana = mana

    def onUse(self, user):
        #remove 1 qty
        text = ""
        user.health += self.health
        user.mana += self.mana
        if user.health > 100:
            user.health = 100
            text += f"{user.name} used {self.name} and healed {self.health} health\n"
        if user.mana > user.maxMana:
            user.mana = user.maxMana
            text += f"{user.name} used {self.name} and healed {self.mana} mana\n"
        #remove last \n
        text = text[:-1]
        return text


class BuffItem(Item):
    def __init__(self, name, description, health, mana, buff, duration, rarity, value):
        super().__init__(name, description, rarity, value)
        self.health = health
        self.mana = mana
        self.buff = buff
        self.duration = duration

    def onUse(self, user):
        text = ""
        user.health += self.health
        user.mana += self.mana
        if user.health > 100:
            user.health = 100
            text += f"{user.name} used {self.name} and healed {self.health} health\n"
        if user.mana > user.maxMana:
            user.mana = user.maxMana
            text += f"{user.name} used {self.name} and healed {self.mana} mana\n"
        for buff in self.buff:
            existingBuff = [element[0] for element in user.buff]
            if buff in existingBuff:
                user.buff[existingBuff.index(buff)][1] += self.duration
            else:
                user.buff.append([buff, self.duration])
        text += f"{user.name} used {self.name} and got {self.buff} for {self.duration} turns"
        return text


class Weapon:
    def __init__(self, name, description, level, damage, rarity, mana):
        self.name = name
        self.description = description
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


class Armor:
    def __init__(self, name, description, level, armor, rarity, mana):
        self.name = name
        self.description = description
        self.baseArmor = armor
        self.level = level
        self.rarity = rarity
        self.mana = mana

    def onUse(self):
        return self.baseArmor
    
    def __dict__(self):
        return {
            "type": "armor",
            "name": self.name,
            "description": self.description,
            "level": self.level,
            "armor": self.baseArmor,
            "rarity": self.rarity,
            "mana": self.mana
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
            manaMultiplier = 2
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
    baseDamage = int(random.randint(5, 15)*damageMultiplier+level)
    modifier = int(baseDamage*rarity*0.1)
    baseDamage += modifier

    mana = int(random.randint(0, 10)*manaMultiplier*level//2)
    modifier = int(mana*rarity*0.1)
    mana += modifier

    return Weapon(weapon["name"], weapon["description"], level, baseDamage, rarity, mana)


def randomArmor(role, level):
    if role not in ["warrior", "mage", "archer"]:
        raise KeyError("Invalid role")
    else:
        if role == "warrior":
            key = "chestplates"
            armorMultiplier = 1.5 #tanky
            manaMultiplier = 0.5
        elif role == "mage":
            key = "robes"
            armorMultiplier = 0.5 #relies on skill
            manaMultiplier = 2
        elif role == "archer":
            key = "tunics"
            armorMultiplier = 1 #polyvalent
            manaMultiplier = 1
    with open("data/armor.json", "r") as f:
        data = json.load(f)

    armor = random.choice(data[key])
    rarity = [1]*10 + [2]*7 + [3]*5 + [4]*3 + [5] + [6]
    random.shuffle(rarity)
    rarity = random.choice(rarity) # 1 = common 2 = uncommon 3 = rare 4 = epic 5 = legendary 6 = mythic
    baseArmor = int(random.randint(1, 15)*armorMultiplier+level)
    modifier = int(baseArmor*rarity*0.1)
    baseArmor += modifier

    mana = int(random.randint(10, 20)*manaMultiplier*level//2)
    modifier = int(mana*rarity*0.1)
    mana += modifier

    return Armor(armor["name"], armor["description"], level, baseArmor, rarity, mana)
