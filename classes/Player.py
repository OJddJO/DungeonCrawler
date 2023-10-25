class Player:
    def __init__(self, role = "warrior", weapon = None, armor = None):
        self.health = 100
        self.mana = 100
        self.exp = 0
        self.level = 1
        self.role = role # warrior, mage, archer
        self.weapon = weapon
        self.armor = armor
        self.inventory = []
        self.skill = {}

    def addSkill(self, skill):
        self.skill[skill.name] = skill