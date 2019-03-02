import cardlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys



class TexasHoldEm(QObject):
    new_credits = pyqtSignal()
    new_pot = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.players = ['Name 1', 'Name 2']
        self.credits = [1000, 1000]
        self.pot = 0

    def call(self):
        pass

    def bet(self, amount):
        self.pot += amount
        self.credits[0] -= amount
        #self.new_pot.emit()
        self.new_credits.emit()
        print("Credits:", self.credits)
        print("Pot", self.pot)

    def fold(self):
        pass


class Player:
    def __init__(self):
        self.cards = ['QS', '7C']
        self.marked_cards = [False] * len(self.cards)
        # self.credits = 1000
        # self.folded = False
        self.cb = None


class CommunityCards(QObject):
    new_card = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.cards = ['2S', '3S', '4S']

    def add_card(self):
        self.cards.append('2H')
        self.new_card.emit()


class buttons():
    def __init__(self):
        super().__init__()

    def print_click(self):
        print('klick')
