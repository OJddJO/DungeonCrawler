class Spell:
    def __init__(self, name, symbol, cost, scale, description, unlock):
        self.name = name
        self.description = description
        self.symbol = symbol
        self.cost = cost
        self.scale = scale
        self.unlock = unlock


def haveBuff(buff, target):
    buffsList = [element[0] for element in target.buff]
    if buff in buffsList:
        return True
    return False

def haveDebuff(debuff, target):
        debuffsList = [element[0] for element in target.debuff]
        if debuff in debuffsList:
            return True
        return False


class DamageSpell(Spell):
    def __init__(self, name, symbol, cost, damage, scale, description, unlock):
        super().__init__(name, symbol, cost, scale, description, unlock)
        self.damage = damage
        self.scale = scale

    def onUse(self, user, target):
        user.mana -= self.cost
        dmg = int(self.damage+(user.mana*self.scale))
        if haveDebuff("break", target):
            dmg -= target.armor.onUse()//2
        else:
            dmg -= target.armor.onUse()
        if dmg < 0:
            dmg = 0
        text = f"{user.name} used {self.name} on {target.name} for {dmg} damage"
        if haveBuff("vampirism", user):
            user.health += dmg // 4
            if user.health > 100:
                user.health = 100
            text += f"\n\033[32mYou\033[0m gain \033[1;31m{dmg // 4} health\033[0m from \033[31m{target.name}\033[0m's blood"
        target.health -= dmg
        return text
    
    def __dict__(self):
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
    def __init__(self, name, symbol, cost, heal, scale, description, unlock):
        super().__init__(name, symbol, cost, scale, description, unlock)
        self.heal = heal
        self.scale = scale

    def onUse(self, user, target):
        user.mana -= self.cost
        hp = int(self.heal+(user.mana*self.scale))
        target.health += hp
        if target.health > 100:
            target.health = 100
        return f"{user.name} used {self.name} on {target.name} for {hp} health"
    
    def __dict__(self):
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
    def __init__(self, name, symbol, cost, heal, scale, buff, duration, description, unlock):
        super().__init__(name, symbol, cost, scale, description, unlock)
        self.heal = heal
        self.scale = scale
        self.buff = buff
        self.duration = duration

    def onUse(self, user, target):
        user.mana -= self.cost
        text = ""
        for buff in self.buff:
            existingBuff = [element[0] for element in target.buff]
            if buff in existingBuff:
                target.buff[existingBuff.index(buff)][1] += self.duration
            else:
                target.buff.append([buff, self.duration])
            text += f"{target.name} gained {buff} for {self.duration} turns\n"
        if self.heal > 0:
            hp = int(self.heal+(user.mana*self.scale))
            target.health += hp
            if target.health > 100:
                target.health = 100
            text += f"{target.name} healed {hp} health"
        return text
    
    def __dict__(self):
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
    def __init__(self, name, symbol, cost, damage, scale, debuff, duration, description, unlock):
        super().__init__(name, symbol, cost, scale, description, unlock)
        self.damage = damage
        self.scale = scale
        self.debuff = debuff
        self.duration = duration

    def onUse(self, user, target):
        user.mana -= self.cost
        text = ""
        for debuff in self.debuff:
            existingDebuff = [element[0] for element in target.debuff]
            if debuff in existingDebuff:
                target.debuff[existingDebuff.index(debuff)][1] += self.duration
            else:
                target.debuff.append([debuff, self.duration])
            text += f"{target.name} gained {debuff} for {self.duration} turns\n"
        if self.damage > 0:
            dmg = int(self.damage+(user.mana*self.scale))
            if haveDebuff("break", target):
                dmg -= target.armor.onUse()//2
            else:
                dmg -= target.armor.onUse()
            if dmg < 0:
                dmg = 0
            target.health -= dmg
            text += f"{target.name} took {dmg} damage"
            
            if haveBuff("vampirism", user):
                user.health += dmg // 4
                if user.health > 100:
                    user.health = 100
                text += f"\n\033[32mYou\033[0m gain \033[1;31m{dmg // 4} health\033[0m from \033[31m{target.name}\033[0m's blood"

        return text    
    
    def __dict__(self):
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
    def __init__(self, spell, branches = []):
        self.spell = spell
        self.branches = branches

    def __str__(self):
        return f'{self.spell.name} {self.branches}'
