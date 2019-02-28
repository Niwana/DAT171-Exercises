import cardlib

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


class Player:
    def __init__(self):
        self.cards = ['QS', '7C']
        self.marked_cards = [False] * len(self.cards)
        # self.credits = 100
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
