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
    def __init__(self, name, description, cost, buff, heal):
        super().__init__(name, description, cost, buff)
        self.buff = buff
        self.heal = heal #secondary

    def onUse(self, user, target):
        target.buff.append(self.buff)
        return f"{user.name} used {self.name} on {target.name} for {self.buff} health"

class DebuffSkill(Skill):
    def __init__(self, name, description, cost, debuff, damage):
        super().__init__(name, description, cost, debuff)
        self.debuff = debuff
        self.damage = damage #secondary

    def onUse(self, user, target):
        target.debuff.append(self.debuff)
        return f"{user.name} used {self.name} on {target.name} for {self.debuff} health"

class Tree:
    def __init__(self):
        self.root = None
        self.branches = []
        self.skill = None

    def addBranch(self, branch):
        self.branches.append(branch)

    def addSkill(self, skill):
        self.skill = skill
