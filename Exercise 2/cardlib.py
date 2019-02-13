import enum


# ♣♦♠♥


class Suit(enum.IntEnum):
    clubs = 0
    diamonds = 1
    spades = 2
    hearts = 3

    def __str__(self):
        return self.name


# Abstract class
class PlayingCards:
    """ This is an abstract class for playing cards """

    def __init__(self, value: int, suit: Suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        """ Returns a readable format of value and suit  """
        return "{}, {}".format(self.value, self.suit)

    def get_value(self):
        """ Returns the value of the card """
        raise NotImplementedError("Derived class did not override this method")

    def get_suit(self):
        """ Returns the suit of the card """
        raise NotImplementedError("Derived class did not override this method")


class NumberedCard(PlayingCards):
    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit


class JackCard(PlayingCards):
    """ Creates the Jack card of a given suit"""

    def __init__(self, suit: Suit):
        """ Description """
        self.suit = suit
        self.value = 11

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit


class QueenCard(PlayingCards):
    """ Creates the Queen card of a given suit"""

    def __init__(self, suit: Suit):
        """ Description """
        self.suit = suit
        self.value = 12

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit


class KingCard(PlayingCards):
    """ Creates the King card of a given suit"""

    def __init__(self, suit: Suit):
        """Description """
        self.suit = suit
        self.value = 13

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit


class AceCard(PlayingCards):
    """ Creates the Ace card of a given suit"""

    def __init__(self, suit: Suit):
        """Description """
        self.suit = suit
        self.value = 14

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit



class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self):
        pass

    def sort_cards(self):
        pass
