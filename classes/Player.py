class Player:
    def __init__(self, weapon = None, armor = None):
        self.health = 100
        self.mana = 100
        self.weapon = weapon
        self.armor = armor
        self.inventory = []
        self.skill = {}

    def addSkill(self, skill):
        self.skill[skill.name] = skill