class Item:
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value


class Weapon(Item):
    def __init__(self, name, description, value, level, damage, rarity = 0, mana = 0):
        super().__init__(name, description, value)
        self.baseDamage = damage
        self.level = level
        self.rarity = rarity
        self.trueDamage = damage + level*2
        self.mana = mana


class Armor(Item):
    def __init__(self, name, description, value, armor):
        super().__init__(name, description, value)
        self.baseArmor = armor


meleeWeapons = [
    Weapon("Ebonshard Sword", "Made from the darkest of materials.", 70, 1, 10, "Common"),
    Weapon("Ivory Gladius", "Made from the tusks of ancient beasts.", 80, 1, 12, "Rare"),
    Weapon("Shattershield", "Capable of breaking through any defense.", 95, 1, 13, "Epic"),
    Weapon("Mithril Scimitar", "Light and sharp, made of mithril.", 80, 5, 12, "Common"),
    Weapon("Silverleaf Blade", "Blessed by the silver leaves of a sacred tree.", 90, 5, 14, "Rare"),
    Weapon("Windrider", "Allows its wielder to ride the wind.", 75, 7, 13, "Rare"),
    Weapon("Wyrmblade", "A blade that resembles a dragon's scale.", 75, 7, 15, "Epic"),
    Weapon("Obsidian Edge", "A blade as dark as night.", 75, 10, 13, "Common"),
    Weapon("Wraithblade", "Whispers of the undead surround it.", 70, 10, 15, "Rare"),
    Weapon("Aethersteel Longsword", "Forged from ethereal materials.", 100, 10, 17, "Epic"),
    Weapon("Demon's Claw", "Possessed by the essence of demons.", 95, 12, 17, "Epic"),
    Weapon("Serpent's Fang", "A serpent-shaped blade with poison.", 70, 15, 12, "Common"),
    Weapon("Runeblade", "Inscribed with ancient, mystic runes.", 85, 15, 14, "Rare"),
    Weapon("Celestial Sword", "Blessed by celestial beings.", 95, 15, 16, "Epic"),
    Weapon("Seraph's Grace", "A weapon of divine grace.", 85, 15, 19, "Legendary"),
    Weapon("Embersteel Sabre", "Forged from ember-fueled flames.", 80, 20, 12, "Common"),
    Weapon("Stormbringer", "Commands the power of the storm.", 85, 20, 15, "Rare"),
    Weapon("Phoenix Wingblade", "Bears the fiery spirit of a phoenix.", 85, 20, 16, "Rare"),
    Weapon("Doomslayer", "Fated to bring doom to its foes.", 100, 20, 18, "Epic"),
    Weapon("Sunfire Saber", "Blazing with the power of the sun.", 85, 20, 20, "Legendary"),
    Weapon("Thunderclap", "Crackling with electrical energy.", 75, 25, 12, "Common"),
    Weapon("Starfall", "Forged from fallen stars.", 90, 25, 14, "Rare"),
    Weapon("Soulreaver", "Feeds on the souls of its victims.", 95, 25, 17, "Epic"),
    Weapon("Moonlight Blade", "Shines like the moon in the night.", 90, 25, 21, "Legendary"),
    Weapon("Frostbite", "A sword with an icy chill.", 70, 30, 12, "Common"),
    Weapon("Bloodmoon", "A cursed weapon that thirsts for blood.", 75, 30, 13, "Common"),
    Weapon("Shadowstrike", "A blade shrouded in darkness.", 80, 30, 15, "Rare"),
    Weapon("Dragonblade", "Forged from the scales of a dragon.", 90, 30, 17, "Epic"),
    Weapon("Voidbringer", "Tainted by the power of the void.", 80, 30, 18, "Epic"),
    Weapon("Excalibur", "A legendary sword of great power.", 100, 30, 22, "Legendary"),
]

#need rework but the name sorting is good
magicStaves = [
    Weapon("Eldritch Willowwand", "Crafted from ancient willow trees.", 70, 1, 8, "Common", 25),
    Weapon("Enchanter's Ebonrod", "A tool of the arcane masters.", 80, 5, 10, "Rare", 50),
    Weapon("Runebound Rod", "Adorned with powerful runes.", 90, 10, 12, "Epic", 75),
    Weapon("Illusionist's Ebonyrod", "Weaves illusions with each gesture.", 70, 15, 14, "Common", 100),
    Weapon("Celestial Scepter", "Radiates celestial energy.", 80, 20, 16, "Rare", 125),
    Weapon("Serpent's Spire", "A staff with the venomous bite.", 85, 25, 18, "Epic", 150),
    Weapon("Moonshadow Scepter", "Draws power from the moon's glow.", 90, 30, 20, "Epic", 175),
    Weapon("Aetherial Staff", "Channels the essence of the aether.", 100, 30, 22, "Legendary", 200),
    Weapon("Timebender's Baton", "Manipulates the flow of time.", 70, 1, 8, "Common", 25),
    Weapon("Crystal Arcanum", "Contains the secrets of crystal magic.", 80, 5, 10, "Rare", 50),
    Weapon("Phoenix Feather Wand", "Fueled by the spirit of the phoenix.", 90, 10, 12, "Epic", 75),
    Weapon("Cursed Hexstaff", "Hexes and curses the target.", 70, 15, 14, "Common", 100),
    Weapon("Voidwalker's Wand", "Taps into the power of the void.", 80, 20, 16, "Rare", 125),
    Weapon("Dragonheart Staff", "Houses the heart of a dragon.", 85, 25, 18, "Epic", 150),
    Weapon("Soulharvest Scepter", "Feasts upon the souls of the fallen.", 90, 30, 20, "Epic", 175),
    Weapon("Mindbender's Rod", "Twists the minds of adversaries.", 100, 30, 22, "Legendary", 200),
    Weapon("Arcane Oakenstaff", "Made from ancient enchanted oaks.", 70, 1, 8, "Common", 25),
    Weapon("Frostbite Wand", "Chills the air with an icy touch.", 80, 5, 10, "Rare", 50),
    Weapon("Stormcaller's Staff", "Commands the fury of the storm.", 90, 10, 12, "Epic", 75),
    Weapon("Phoenix Wingblade", "Bears the fiery spirit of a phoenix.", 70, 15, 14, "Common", 100),
    Weapon("Doomslayer", "Fated to bring doom to its foes.", 80, 20, 16, "Rare", 125),
    Weapon("Sunfire Saber", "Blazing with the power of the sun.", 85, 25, 18, "Epic", 150),
    Weapon("Thunderclap", "Crackling with electrical energy.", 90, 30, 20, "Epic", 175),
    Weapon("Starfall", "Forged from fallen stars.", 100, 30, 22, "Legendary", 200),
    Weapon("Soulreaver", "Feeds on the souls of its victims.", 70, 1, 8, "Common", 25),
    Weapon("Moonlight Blade", "Shines like the moon in the night.", 80, 5, 10, "Rare", 50),
    Weapon("Frostbite", "A sword with an icy chill.", 90, 10, 12, "Epic", 75),
    Weapon("Bloodmoon", "A cursed weapon that thirsts for blood.", 70, 15, 14, "Common", 100),
    Weapon("Shadowstrike", "A blade shrouded in darkness.", 80, 20, 16, "Rare", 125),
    Weapon("Dragonblade", "Forged from the scales of a dragon.", 85, 25, 18, "Epic", 150),
    Weapon("Voidbringer", "Tainted by the power of the void.", 80, 30, 20, "Epic", 175),
    Weapon("Excalibur", "A legendary sword of great power.", 100, 30, 22, "Legendary", 200)
]