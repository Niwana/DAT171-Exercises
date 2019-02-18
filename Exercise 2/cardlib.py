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

    def __init__(self, suit):
        self.suit = suit

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
        super().__init__(suit)
        self.value = value

    def __str__(self):
        """ Returns a readable format of value and suit  """
        return "{}, {}".format(self.get_value(), self.get_suit())

    def __repr__(self):
        """ """
        return repr((self.get_value(), self.get_suit()))

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit


class JackCard(PlayingCards):
    """ Creates the Jack card of a given suit"""

    def __init__(self, suit: Suit):
        """ Description """
        super().__init__(suit)

    def __str__(self):
        """ Returns a readable format of value and suit  """
        return "{}, {}".format(self.get_value(), self.get_suit())

    def __repr__(self):
        """ """
        return repr((self.get_value(), self.get_suit()))

    def get_value(self):
        return 11

    def get_suit(self):
        return self.suit


class QueenCard(PlayingCards):
    """ Creates the Queen card of a given suit"""

    def __init__(self, suit: Suit):
        """ Description """
        super().__init__(suit)

    def __str__(self):
        """ Returns a readable format of value and suit  """
        return "{}, {}".format(self.get_value(), self.get_suit())

    def __repr__(self):
        """ """
        return repr((self.get_value(), self.get_suit()))

    def get_value(self):
        return 12

    def get_suit(self):
        return self.suit


class KingCard(PlayingCards):
    """ Creates the King card of a given suit"""

    def __init__(self, suit: Suit):
        """Description """
        super().__init__(suit)

    def __str__(self):
        """ Returns a readable format of value and suit  """
        return "{}, {}".format(self.get_value(), self.get_suit())

    def __repr__(self):
        """ """
        return repr((self.get_value(), self.get_suit()))

    def get_value(self):
        return 13

    def get_suit(self):
        return self.suit


class AceCard(PlayingCards):
    """ Creates the Ace card of a given suit"""

    def __init__(self, suit: Suit):
        """Description """
        super().__init__(suit)

    def __str__(self):
        """ Returns a readable format of value and suit  """
        return "{}, {}".format(self.get_value(), self.get_suit())

    def __repr__(self):
        """ """
        return repr((self.get_value(), self.get_suit()))

    def get_value(self):
        return 14

    def get_suit(self):
        return self.suit


class Hand():
    def __init__(self):
        self.cards = []

    def __str__(self):
        """ Returns a readable format of value and suit  """
        hand = []
        for card in self.cards:
            hand.append((card.get_value(), card.get_suit()))
        return repr(hand)

    def add_card(self, card):
        return self.cards.append(card)

    def remove_card(self, index):
        return self.cards.remove(index)

    def sort_cards(self):
        pass

    def best_poker_hand(self, cards):  # best_poker_hand(self, cards=[]):
        if PokerHand.check_straight_flush(self+cards):
            print("Your best hand is a straight flush. Highest card:", PokerHand.check_straight_flush(self+cards))
       # if full_house
        elif PokerHand.two_pair(self, cards):
            print("Two pairs:", PokerHand.cards)
        elif PokerHand.one_pair(self,cards):
            print("One pair:", PokerHand.cards)
        elif PokerHand.high_card(self, cards):
            print("High cards:", PokerHand.cards)


class StandardDeck:
    """ Text"""

    def __init__(self):
        self.cards = []

    def __str__(self):
        return str(self.cards)

    def __repr__(self):
        """ """
        return repr(self.cards)

    def __len__(self):
        """ """
        return 52

    def __setitem__(self, key, value):
        super().__setitem__(key, value)

    def __getitem__(self, key):
        super().__getitem__(key)

    def create_deck(self):
        """ Take an empty list and creates a 52 card deck"""
        # Create the numbered cards
        for i in range(2, 11):  # !!! Denna deck skapar 15 st NumberedCards, inga JackCards etc.
            card = NumberedCard(i, Suit.clubs)
            self.cards.append(card)
        for i in range(2, 11):
            card = NumberedCard(i, Suit.diamonds)
            self.cards.append(card)
        for i in range(2, 11):
            card = NumberedCard(i, Suit.spades)
            self.cards.append(card)
        for i in range(2, 11):
            card = NumberedCard(i, Suit.hearts)
            self.cards.append(card)
        # Adds the other cards...
        self.cards.append(JackCard(Suit.clubs))
        self.cards.append(JackCard(Suit.diamonds))
        self.cards.append(JackCard(Suit.spades))
        self.cards.append(JackCard(Suit.hearts))
        self.cards.append(QueenCard(Suit.clubs))
        self.cards.append(QueenCard(Suit.diamonds))
        self.cards.append(QueenCard(Suit.spades))
        self.cards.append(QueenCard(Suit.hearts))
        self.cards.append(KingCard(Suit.clubs))
        self.cards.append(KingCard(Suit.diamonds))
        self.cards.append(KingCard(Suit.spades))
        self.cards.append(KingCard(Suit.hearts))
        self.cards.append(AceCard(Suit.clubs))
        self.cards.append(AceCard(Suit.diamonds))
        self.cards.append(AceCard(Suit.spades))
        self.cards.append(AceCard(Suit.hearts))

        return self.cards

    def shuffle(self):
        return random.shuffle(self.cards)


class PokerHand(list):
    def __init__(self, cards):
        super().__init__()
        self.cards = cards

    def check_high_card(self):
        """ Takes a list of tuples and return the biggest tuple. Starts with the first element, than the second """
        highest_card = ()
        for i in range(len(self)):
            if self[i] > highest_card:
                highest_card = self[i]
            else:
                pass
        PokerHand.cards = highest_card  # Makes it possible to access the cards somewhere else
        return True

    def check_one_pair(self):
        """ Return true if cards_to_evaluate has a pair in it """
        pairs = []
        for i in range(len(self)):
            for j in range(len(self)):
                # Check if the value of card i and card j is the same and whether or not they are not already in
                # the list of pairs
                if self[i][0] == self[j][0] and self[i][1] != self[j][1] and \
                        (self[i] not in pairs or self[j] not in pairs):
                    pairs += self[i], self[j]
        # Check if the hand only has one pair or multiple
        if len(pairs) == 2:
            PokerHand.cards = pairs
            return True
        else:
            return False

    def check_two_pair(self):
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

    def check_three_of_a_kind(self):
        pass

    def check_straight(self):
        pass

    def check_flush(self):
        pass

    def check_full_house(self):
        pass

    def check_four_of_a_kind(self):
        pass

    def check_straight_flush(self):
        values = []

        for c in self:
            values.append((c.get_value(), c.get_suit()))

        for c in self:
            if c.get_value() == 14:
                values.append((1, c.get_suit()))

        for c in reversed(self):
            found_straight = True

            for k in range(1, 5):
                if (c.get_value() - k, c.get_suit()) not in values:
                    found_straight = False
                    break
            if found_straight:
                return c.get_value()

        print(values)


community_cards = [(NumberedCard(1, Suit.spades)), (NumberedCard(2, Suit.spades)), (NumberedCard(3, Suit.spades)),
                   (NumberedCard(4, Suit.spades)), (NumberedCard(5, Suit.spades))]
#player_1_cards = [(NumberedCard(6, Suit.spades)), (NumberedCard(7, Suit.spades))]

#cards_to_evaluate = community_cards + player_1_cards

card_1 = NumberedCard(6, Suit.spades)
card_2 = NumberedCard(4, Suit.spades)

player_1_cards = Hand()

player_1_cards.add_card(card_1)
player_1_cards.add_card(card_2)
print(player_1_cards)

player_1_cards.remove_card(card_1)
print(player_1_cards)


#print(player_1_cards)

'''
    def __str__(self):
        """ Returns a readable format of value and suit  """
        text = ""
        for card in self.cards:
            text += str(card) + "\n"
        return text
'''
