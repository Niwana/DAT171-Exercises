import enum
import abc
import random


# ♣♦♠♥


class Suit(enum.IntEnum):
    clubs = 0
    diamonds = 1
    spades = 2
    hearts = 3

    def __str__(self):
        return self.name


# Abstract class
class PlayingCards(metaclass=abc.ABCMeta):
    """ This is an abstract class for playing cards """

    def __str__(self):
        """ Returns a readable format of value and suit  """
        return "{}, {}".format(self.value, self.suit)

    @abc.abstractmethod
    def get_value(self):
        """ Returns the value of the card """
        raise NotImplementedError("Derived class did not override this method")

    @abc.abstractmethod
    def get_suit(self):
        """ Returns the suit of the card """
        raise NotImplementedError("Derived class did not override this method")


class NumberedCard(PlayingCards):
    def __init__(self, value: int, suit: Suit):
        self.value = value
        self.suit = suit

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

    def __str__(self):
        """ Returns a readable format of value and suit  """
        text = ""
        for card in self.cards:
            text += str(card) + "\n"
        return text

    def add_card(self, card):
        return self.cards.append(card)

    def remove_card(self, index):
        pass

    def sort_cards(self):
        pass


class StandardDeck:
    """ Text"""

    def __init__(self):
        self.card = None
        self.deck = []

    def __str__(self):
        """ Returns a readable format of value and suit  """
        text = ""
        for card in self.deck:
            text += str(card) + "\n"
        return text

    def create_deck(self):
        # Create the numbered cards
        for i in range(2, 11):
            card = NumberedCard(i, Suit.clubs)
            deck.append((card.value, card.suit))
        for i in range(2, 11):
            card = NumberedCard(i, Suit.diamonds)
            deck.append((card.value, card.suit))
        for i in range(2, 11):
            card = NumberedCard(i, Suit.spades)
            deck.append((card.value, card.suit))
        for i in range(2, 11):
            card = NumberedCard(i, Suit.hearts)
            deck.append((card.value, card.suit))

        return deck

    def shuffle(self):
        return random.shuffle(self.deck)


# full_deck = create_deck()
deck = []

card_1 = NumberedCard(2, Suit.spades)
card_2 = NumberedCard(2, Suit.hearts)

jack_1 = JackCard(Suit.spades)

deck.append((card_1.get_value(), (card_1.get_suit())))
deck.append((card_2.get_value(), (card_2.get_suit())))

print("card 1:", card_1)
print("card 2:", card_2)
# print("Deck:", deck)
# print(deck[0] < deck[1])
hand = Hand()
hand.add_card(card_1)
hand.add_card(card_2)
print(hand)

full_deck = StandardDeck()
print(full_deck.create_deck(), '\n')
print(random.shuffle(full_deck.create_deck()))
