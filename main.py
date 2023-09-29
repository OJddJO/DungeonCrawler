import random

class Player:
    def __init__(self):
        self.health = 100
        self.weapon = None
        self.armor = None
        self.inventory = []


class Item:
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value
    

class Weapon(Item):
    def __init__(self, name, description, value, damage):
        super().__init__(name, description, value)
        self.damage = damage


class Dungeon:
    def __init__(self):
        self.rooms = []


class Room:
    def __init__(self):
        self.matrix = [["¤" for i in range(10)] for i in range(10)]

    def generate(self):
        # Generate maze
        wall = "#"
        path = " "
        #Start Pos
        orientation = random.randint(0, 3)
        if orientation == 0:
            sx = 0
            sy = random.randint(0, 9)
        elif orientation == 1:
            sx = random.randint(0, 9)
            sy = 0
        elif orientation == 2:
            sx = 9
            sy = random.randint(0, 9)
        elif orientation == 3:
            sx = random.randint(0, 9)
            sy = 9
        self.matrix[sx][sy] = path
        walls = []
        walls.append([sx+1, sy])
        walls.append([sx-1, sy])
        walls.append([sx, sy+1])
        walls.append([sx, sy-1])
        self.matrix[sx+1][sy] = wall
        self.matrix[sx-1][sy] = wall
        self.matrix[sx][sy+1] = wall
        self.matrix[sx][sy-1] = wall

        


    def display(self):
        for i in range(10):
            for j in range(10):
                print(self.matrix[i][j], end="")
            print("")
