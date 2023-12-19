class Spell:
    """Base class for all spells"""
    def __init__(self, name, symbol, cost, scale, description, unlock):
        """Constructor for the Spell class, takes in name, symbol, cost, scale, description and unlock"""
        self.name = name
        self.description = description
        self.symbol = symbol
        self.cost = cost
        self.scale = scale
        self.unlock = unlock

# copy from classes/Game.py
# use only in this file
def haveBuff(buff, target):
    """Returns True if the target has the buff"""
    buffsList = [element[0] for element in target.buff]
    if buff in buffsList:
        return True
    return False

def haveDebuff(debuff, target):
    """Returns True if the target has the debuff"""
    debuffsList = [element[0] for element in target.debuff]
    if debuff in debuffsList:
        return True
    return False


class DamageSpell(Spell):
    """Damage spell, deals damage to the enemy"""
    def __init__(self, name, symbol, cost, damage, scale, description, unlock):
        """Constructor for the DamageSpell class, takes in name, symbol, cost, damage, scale, description and unlock"""
        super().__init__(name, symbol, cost, scale, description, unlock)
        self.damage = damage
        self.scale = scale

    def onUse(self, user, target):
        """Apply the spell to the target and returns a string of the action"""
        user.mana -= self.cost
        dmg = int(self.damage+(user.mana*self.scale))
        if haveDebuff("break", target):
            dmg -= target.armor.onUse()//2
        else:
            dmg -= target.armor.onUse()
        if dmg < 0:
            dmg = 0
        text = [[(f"{user.name} used {self.name} on {target.name} for {dmg} damage", 9, None)]]
        if haveBuff("vampirism", user):
            user.health += dmg // 4
            if user.health > 100:
                user.health = 100
            text.append([("You ", 5, None), ("gain ", 9, None), (f"{dmg // 4} health", 4, None), (" from ", 9, None), (f"{target.name}", 3, None), ("'s blood", 9, None)])
        target.health -= dmg
        return text
    
    def __dict__(self):
        """Returns a dictionary representation of the spell"""
        return {
            "type": "damage",
            "name": self.name,
            "symbol": self.symbol,
            "cost": self.cost,
            "damage": self.damage,
            "scale": self.scale,
            "description": self.description,
            "unlock": self.unlock
        }

class HealSpell(Spell):
    """Heal spell, heals the target"""
    def __init__(self, name, symbol, cost, heal, scale, description, unlock):
        """Constructor for the HealSpell class, takes in name, symbol, cost, heal, scale, description and unlock"""
        super().__init__(name, symbol, cost, scale, description, unlock)
        self.heal = heal
        self.scale = scale

    def onUse(self, user, target):
        """Apply the spell to the target and returns a string of the action"""
        user.mana -= self.cost
        hp = int(self.heal+(user.mana*self.scale))
        target.health += hp
        if target.health > 100:
            target.health = 100
        return [[(f"{user.name} used {self.name} on {target.name} for {hp} health", 9, None)]]
    
    def __dict__(self):
        """Returns a dictionary representation of the spell"""
        return {
            "type": "heal",
            "name": self.name,
            "symbol": self.symbol,
            "cost": self.cost,
            "heal": self.heal,
            "scale": self.scale,
            "description": self.description,
            "unlock": self.unlock
        }

class BuffSpell(Spell):
    """Buff spell, gives the target a buff for a certain amount of turns"""
    def __init__(self, name, symbol, cost, heal, scale, buff, duration, description, unlock):
        super().__init__(name, symbol, cost, scale, description, unlock)
        self.heal = heal
        self.scale = scale
        self.buff = buff
        self.duration = duration

    def onUse(self, user, target):
        """Apply the spell to the target and returns a string of the action"""
        user.mana -= self.cost
        text = []
        for buff in self.buff:
            existingBuff = [element[0] for element in target.buff]
            if buff in existingBuff:
                target.buff[existingBuff.index(buff)][1] += self.duration
            else:
                target.buff.append([buff, self.duration])
            text.append([(f"{target.name} gained {buff} for {self.duration} turns", 9, None)])
        if self.heal > 0:
            hp = int(self.heal+(user.mana*self.scale))
            target.health += hp
            if target.health > 100:
                target.health = 100
            text.append([(f"{target.name} healed {hp} health", 9, None)])
        return text
    
    def __dict__(self):
        """Returns a dictionary representation of the spell"""
        return {
            "type": "buff",
            "name": self.name,
            "symbol": self.symbol,
            "cost": self.cost,
            "heal": self.heal,
            "scale": self.scale,
            "buff": self.buff,
            "duration": self.duration,
            "description": self.description,
            "unlock": self.unlock
        }

class DebuffSpell(Spell):
    """Debuff spell, gives the target a debuff for a certain amount of turns"""
    def __init__(self, name, symbol, cost, damage, scale, debuff, duration, description, unlock):
        """Constructor for the DebuffSpell class, takes in name, symbol, cost, damage, scale, debuff, duration, description and unlock"""
        super().__init__(name, symbol, cost, scale, description, unlock)
        self.damage = damage
        self.scale = scale
        self.debuff = debuff
        self.duration = duration

    def onUse(self, user, target):
        """Apply the spell to the target and returns a string of the action"""
        user.mana -= self.cost
        text = []
        for debuff in self.debuff:
            existingDebuff = [element[0] for element in target.debuff]
            if debuff in existingDebuff:
                target.debuff[existingDebuff.index(debuff)][1] += self.duration
            else:
                target.debuff.append([debuff, self.duration])
            text.append([(f"{target.name} gained {debuff} for {self.duration} turns", 9, None)])
        if self.damage > 0:
            dmg = int(self.damage+(user.mana*self.scale))
            if haveDebuff("break", target):
                dmg -= target.armor.onUse()//2
            else:
                dmg -= target.armor.onUse()
            if dmg < 0:
                dmg = 0
            target.health -= dmg
            text.append([(f"{target.name} took {dmg} damage", 9, None)])
            
            if haveBuff("vampirism", user):
                user.health += dmg // 4
                if user.health > 100:
                    user.health = 100
                text.append([("You ", 5, None), ("gain ", 9, None), (f"{dmg // 4} health", 4, None), (" from ", 9, None), (f"{target.name}", 3, None), ("'s blood", 9, None)])
        return text    
    
    def __dict__(self):
        """Returns a dictionary representation of the spell"""
        return {
            "type": "debuff",
            "name": self.name,
            "symbol": self.symbol,
            "cost": self.cost,
            "damage": self.damage,
            "scale": self.scale,
            "debuff": self.debuff,
            "duration": self.duration,
            "description": self.description,
            "unlock": self.unlock
        }

class Tree:
    """Tree class, contains a spell and its branches to other spells"""
    def __init__(self, spell, branches = []):
        """Constructor for the Tree class, takes in spell and branches"""
        self.spell = spell
        self.branches = branches

    def __str__(self):
        """Returns a string representation of the tree"""
        return f'{self.spell.name} {self.branches}'
