import enum


class Suit(enum.IntEnum):
    clubs = 0
    diamonds = 1
    spades = 2
    hearts = 3

    def __str__(self):
        return self.name


class NumberedCard:
    def __init__(self, value: int, suit: Suit):
        """Description """
        self.value = value
        self.suit = suit
        self.rank = value

    def __str__(self):
        return "{} of {}".format(self.value, self.suit.name)


class JackCard:
    def __init__(self, suit: [Suit]):
        """Description """
        self.suit = suit
        self.rank = 11

    def __str__(self):
        return "{} Jack".format(self.suit.name)


class QueenCard:
    def __init__(self, suit: [Suit]):
        """Description """
        self.suit = suit
        self.rank = 12

    def __str__(self):
        return "{} Queen".format(self.suit.name)


class KingCard:
    def __init__(self, suit: [Suit]):
        """Description """
        self.suit = suit
        self.rank = 13

    def __str__(self):
        return "{} King".format(self.suit.name)


class AceCard:
    def __init__(self, suit: [Suit]):
        """Description """
        self.suit = suit
        self.rank = 14

    def __str__(self):
        return "{} Ace".format(self.suit.name)
