class Skill:
    def __init__(self, name, description, cost):
        self.name = name
        self.description = description
        self.cost = cost #mana cost
        
class DamageSkill(Skill):
    def __init__(self, name, description, cost, damage):
        super().__init__(name, description, cost, damage)
        self.damage = damage

    def onUse(self, user, target):
        target.hp -= self.damage
        return f"{user.name} used {self.name} on {target.name} for {self.damage} damage"

class HealSkill(Skill):
    def __init__(self, name, description, cost, heal):
        super().__init__(name, description, cost, heal)
        self.heal = heal

    def onUse(self, user, target):
        target.hp += self.heal
        return f"{user.name} used {self.name} on {target.name} for {self.heal} health"

class BuffSkill(Skill):
    def __init__(self, name, description, cost, buff):
        super().__init__(name, description, cost, buff)
        self.buff = buff

    def onUse(self, user, target):
        target.buff.append(self.buff)
        return f"{user.name} used {self.name} on {target.name} for {self.buff} health"

class DebuffSkill(Skill):
    def __init__(self, name, description, cost, debuff):
        super().__init__(name, description, cost, debuff)
        self.debuff = debuff

    def onUse(self, user, target):
        target.debuff.append(self.debuff)
        return f"{user.name} used {self.name} on {target.name} for {self.debuff} health"
