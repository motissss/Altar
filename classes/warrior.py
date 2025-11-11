from classes.player import Player

class Warrior(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.attack_power = 10
        self.hp = 150

    def attack(self):
        print("Warrior slashes with sword!")
