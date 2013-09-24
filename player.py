class Player(object):
    def __init__(self):
        self.coord = tuple
        self.health = 75
        self.inv = {}
        self.ammo = 0
        self.points = 0
        self.gun = False
        self.gunDamage = 0

    def addToInv(self, name, coord):
        self.inv[name] = coord

    def decreaseHealth(self, amount):
        self.health -= amount
        return self.health

    def increaseHealth(self, amount):
        if self.health < 100:
            self.health = min((self.health + amount), 100)

    def increasePoints(self, amount):
        self.points += amount

    def increaseAmmo(self, amount):
        self.ammo += amount

    def decreaseAmmo(self):
        if self.ammo > 0:
            self.ammo = max((self.ammo - 1), 0)

    def addToGunDamage(self, amount):
        self.gunDamage = amount

    def useGun(self):
        self.gun = True
        return True

    def putUpGun(self):
        self.gun = False
        return False
