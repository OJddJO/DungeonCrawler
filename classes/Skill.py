import json
from typing import Any

class Skill:
    def __init__(self, name, symbol, cost, scale, description, unlock):
        self.name = name
        self.description = description
        self.symbol = symbol
        self.cost = cost
        self.scale = scale
        self.unlock = unlock
        
class DamageSkill(Skill):
    def __init__(self, name, symbol, cost, damage, scale, description, unlock):
        super().__init__(name, symbol, cost, scale, description, unlock)
        self.damage = damage
        self.scale = scale

    def onUse(self, user, target):
        return self.damage, user, target

class HealSkill(Skill):
    def __init__(self, name, symbol, cost, heal, scale, description, unlock):
        super().__init__(name, symbol, cost, scale, description, unlock)
        self.heal = heal
        self.scale = scale

    def onUse(self, user, target):
        target.hp += self.heal
        if target.hp > 100:
            target.hp = 100
        return f"{user.name} used {self.name} on {target.name} for {self.heal} health"

class BuffSkill(Skill):
    def __init__(self, name, symbol, cost, heal, scale, buff, duration, description, unlock):
        super().__init__(name, symbol, cost, scale, description, unlock)
        self.heal = heal
        self.scale = scale
        self.buff = buff
        self.duration = duration

    def onUse(self, user, target):
        for buff in self.buff:
            existingBuff = [element[0] for element in target.buff]
            if buff in existingBuff:
                target.buff[existingBuff.index(buff)][1] += self.duration
            else:
                target.buff.append([buff, self.duration])
        return f"{user.name} used {self.name} on {target.name} for {self.buff} health"

class DebuffSkill(Skill):
    def __init__(self, name, symbol, cost, damage, scale, debuff, duration, description, unlock):
        super().__init__(name, symbol, cost, scale, description, unlock)
        self.damage = damage
        self.scale = scale
        self.debuff = debuff
        self.duration = duration

    def onUse(self, user, target):
        for debuff in self.debuff:
            existingDebuff = [element[0] for element in target.debuff]
            if debuff in existingDebuff:
                target.debuff[existingDebuff.index(debuff)][1] += self.duration
            else:
                target.debuff.append([debuff, self.duration])
        return f"{user.name} used {self.name} on {target.name} for {self.debuff} health"

class Tree:
    def __init__(self, spell, branches = []):
        self.spell = spell
        self.branches = branches


class SkillTree:
    def __init__(self, role):
        self.tree = self.createTree(role)
        self.current = self.tree


    def render(self):
        separator = "─" * 61
        print(separator)
        def offset(x): return ' ' * x
        def sliceSpell(spell):
            symbol = spell.symbol
            line1 = f"╔═╩═╗"
            line2 = f"║{symbol} ║"
            line3 = f"╚═╦═╝"
            return line1, line2, line3

        #render self.current, center self.current
        print(f'{offset(30)}║')
        skillSlice = sliceSpell(self.current.spell)
        print(offset(28) + skillSlice[0])
        print(offset(28) + skillSlice[1])
        print(offset(28) + skillSlice[2])
        # if len(self.current.branches) == 1:
        #     print(f'{offset(30)}║')
        #     sliceSpell(self.current.branches[0].spell)
        #     print(offset(28) + skillSlice[0])
        #     print(offset(28) + skillSlice[1])
        #     print(offset(28) + skillSlice[2])
        #     print(f'{offset(30)}║')
        # elif len(self.current.branches) == 2:
        #     print(f'{offset(15)}╔══════════════╩══════════════╗')
        #     skill1 = sliceSpell(self.current.branches[0].spell)
        #     skill2 = sliceSpell(self.current.branches[1].spell)
        #     print(offset(13) + skill1[0] + offset(26) + skill2[0])
        #     print(offset(13) + skill1[1] + offset(26) + skill2[1])
        #     print(offset(13) + skill1[2] + offset(26) + skill2[2])
        #     print(f'{offset(15)}║{offset(30)}║')
        # elif len(self.current.branches) == 3:
        #     print(f'{offset(10)}╔═══════════════════╬═══════════════════╗')
        #     skill1 = sliceSpell(self.current.branches[0].spell)
        #     skill2 = sliceSpell(self.current.branches[1].spell)
        #     skill3 = sliceSpell(self.current.branches[2].spell)
        #     print(offset(8) + skill1[0] + offset(16) + skill2[0] + offset(16) + skill3[0])
        #     print(offset(8) + skill1[1] + offset(16) + skill2[1] + offset(16) + skill3[1])
        #     print(offset(8) + skill1[2] + offset(16) + skill2[2] + offset(16) + skill3[2])
        #     print(f'{offset(10)}║{offset(20)}║{offset(20)}║')

        qty = len(self.current.branches)
        if qty == 1:
            print(f'{offset(30)}║')
            sliceSpell(self.current.branches[0].spell)
            print(offset(28) + skillSlice[0])
            print(offset(28) + skillSlice[1])
            print(offset(28) + skillSlice[2])
            print(f'{offset(30)}║')
        elif qty%2 == 0:
            deriv = (qty - 2)//2 #get the number of derivations excluding the one on the border for each side
            text = "╔"
            n = 1 #current derivation index
            for i in range(1, 60):
                if i < n*61//qty//2: #if the current index is less than the next derivation index
                    text += "═"
                elif n == qty//2: #if the current index is the middle derivation index
                    text += "╩"
                    n += 1
                else: #if the current index is the next derivation index
                    text += "╦"
                    n += 1
            text += "╗"
            print({offset(60//qty//2)}+text)



    def createTree(self, role):
        if role == "mage":
            data = json.load(open("data/spells/mage.json", "r", encoding="utf-8"))
        firstKey = list(data.keys())[0]
        
        def createTree(key, data):
            spellData = data[key]
            if spellData['type'] == "damage":
                spell = DamageSkill(spellData['name'], spellData['symbol'], spellData['cost'], spellData['damage'], spellData['scale'], spellData['description'], spellData['unlock'])
            elif spellData['type'] == "heal":
                spell = HealSkill(spellData['name'], spellData['symbol'], spellData['cost'], spellData['heal'], spellData['scale'], spellData['description'], spellData['unlock'])
            elif spellData['type'] == "buff":
                spell = BuffSkill(spellData['name'], spellData['symbol'], spellData['cost'], spellData['heal'], spellData['scale'], spellData['buff'], spellData['duration'], spellData['description'], spellData['unlock'])
            elif spellData['type'] == "debuff":
                spell = DebuffSkill(spellData['name'], spellData['symbol'], spellData['cost'], spellData['damage'], spellData['scale'], spellData['debuff'], spellData['duration'], spellData['description'], spellData['unlock'])
            branches = []
            for nextKey in data[key]['next']:
                branches.append(createTree(nextKey, data[key]['next']))
            return Tree(spell, branches)
        
        return createTree(firstKey, data)


if __name__ == "__main__":
    tree = SkillTree("mage")
    tree.render()

