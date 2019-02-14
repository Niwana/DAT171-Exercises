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

    def __init__(self):
        self.value = None
        self.suit = None

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
    """ Description """
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

    def best_poker_hand(self):  # best_poker_hand(self, cards=[]):
        if PokerHand.two_pair(self) == True:
            print("Two pairs:", PokerHand.cards)
        elif PokerHand.one_pair(self) == True:
            print("One pair:", PokerHand.cards)
        elif PokerHand.high_card(self) == True:
            print("High cards:", PokerHand.cards)


'''
def best_hand(onHand):
    if PokerHand.two_pair(onHand) == True:
        print("Two pairs:", PokerHand.cards)
    elif PokerHand.one_pair(onHand) == True:
        print("One pair:", PokerHand.cards)
    elif PokerHand.high_card(onHand) == True:
        print("High cards:", PokerHand.cards)
'''


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


class PokerHand:
    def __init__(self, cards):
        self.cards = cards

    def high_card(self):
        """ Takes a list of tuples and return the biggest tuple. Starts with the first element, than the second """
        highest_card = ()
        for i in range(len(self)):
            if self[i] > highest_card:
                highest_card = self[i]
            else:
                pass
        PokerHand.cards = highest_card  # Makes it possible to access the cards somewhere else
        return True

    def one_pair(self):
        """ Return true if cards_to_evaluate has a pair in it """
        pairs = []
        for i in range(len(self)):
            for j in range(len(self)):
                # Check if the value of card i and card j is the same and whether or not they are not already in
                # the list of pairs
                if self[i][0] == self[j][0] and self[i][1] != self[j][1] and (
                        self[i] not in pairs or self[j] not in pairs):
                    pairs += self[i], self[j]
        # Check if the hand only has one pair or multiple
        if len(pairs) == 2:
            PokerHand.cards = pairs
            return True
        else:
            return False

    def two_pair(self):
        pairs = []
        for i in range(len(self)):
            for j in range(len(self)):
                # Check if the value of card i and card j is the same and whether or not they are not already in
                # the list of pairs
                if self[i][0] == self[j][0] and self[i][1] != self[j][1] and (
                        self[i] not in pairs or self[j] not in pairs):
                    pairs += self[i], self[j]
        # return pairs
        if len(pairs) == 4:
            PokerHand.cards = pairs
            return True
        else:
            return False

    def three_of_a_kind(self):
        pass

    def straight(self):
        pass

    def flush(self):
        pass

    def full_house(self):
        pass

    def four_of_a_kind(self):
        pass

    def straight_flush(self):
        pass


community_cards = [(4, Suit.spades), (3, Suit.hearts), (5, Suit.hearts), (6, Suit.spades), (10, Suit.spades)]
player_1_cards = [(2, Suit.spades), (7, Suit.hearts)]
cards_to_evaluate = community_cards + player_1_cards

# print("Highest card:", PokerHand.high_card(onHand))
# print("Pair:", PokerHand.one_pair(onHand))
# print("Two pairs:", PokerHand.two_pair(onHand))


Hand.best_poker_hand(cards_to_evaluate)

'''
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
'''
