class Player(object):
    def __init__(self):
        self.coord = tuple
        self.health = 75
        self.inv = {}
        self.ammo = 0
        self.points = 0

    def printHealth(self):
        print self.health

    def addToInv(self, name, coord):
        self.inv[name] = coord

    def decreaseHealth(self, amount):
        self.health -= amount
        return self.health

    def increaseHealth(self, amount):
        if self.health < 100:
            self.health = min((self.health + amount), 100)
            return self.health

    def increasePoints(self, amount):
        self.points += amount
        return self.points