class Skill:
    def __init__(self, name, description, cost, damage):
        self.name = name
        self.description = description
        self.cost = cost #mana cost
        
class DamageSkill(Skill):
    def __init__(self, name, description, cost, damage):
        super().__init__(name, description, cost, damage)
        self.damage = damage

class HealSkill(Skill):
    def __init__(self, name, description, cost, heal):
        super().__init__(name, description, cost, heal)
        self.heal = heal

class BuffSkill(Skill):
    def __init__(self, name, description, cost, buff):
        super().__init__(name, description, cost, buff)
        self.buff = buff

class DebuffSkill(Skill):
    def __init__(self, name, description, cost, debuff):
        super().__init__(name, description, cost, debuff)
        self.debuff = debuff
