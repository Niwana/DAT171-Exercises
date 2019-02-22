import enum
import abc
import random
import heapq as hq

# ♣♦♠♥


class Suit(enum.IntEnum):
    """ Class Suit contains the four suits (club, diamond, spade, heart) and their respective order
    (club < diamond < spade < heart)"""
    clubs = 0
    diamonds = 1
    spades = 2
    hearts = 3

    def __str__(self):
        """ Return the name of the enum value """
        return self.name


# Abstract class
class PlayingCards(metaclass=abc.ABCMeta):
    """ This is an abstract class for the playing cards """

    def __init__(self, suit: Suit):
        """ """
        self.suit = suit

    def __str__(self):
        """ Returns a readable format of value and suit """
        return "{}, {}".format(self.get_value(), self.get_suit())

    def __repr__(self):
        """ Returns a readable format of value and suit from a list"""
        # This gets printed when calling StandardDeck(). Strange?
        return repr((self.get_value(), str(self.get_suit())))

    def __lt__(self, other):
        """ Returns self < other """
        return (self.get_value(), self.get_suit()) < (other.get_value(), other.get_suit())

    def __eq__(self, other):
        """ Returns self == other"""
        return (self.get_value(), self.get_suit()) == (other.get_value(), other.get_suit())

    @abc.abstractmethod
    def get_value(self):
        """ Returns the value of the card """
        raise NotImplementedError("Derived class did not override this method")

    @abc.abstractmethod
    def get_suit(self):
        """ Returns the suit of the card """
        raise NotImplementedError("Derived class did not override this method")


class NumberedCard(PlayingCards):
    """ Creates a card of a given value and suit """

    def __init__(self, value: int, suit: Suit):
        """ """
        self.value = value
        super().__init__(suit)

    def get_value(self):
        """ Returns the value of the card """
        return self.value

    def get_suit(self):
        """ Returns the suit of the card """
        return self.suit


class JackCard(PlayingCards):
    """ Creates the Jack card of a given suit"""

    def __init__(self, suit: Suit):
        """ """
        super().__init__(suit)

    def get_value(self):
        """ Returns the value of the card """
        return 11

    def get_suit(self):
        """ Returns the suit of the card """
        return self.suit


class QueenCard(PlayingCards):
    """ Creates the Queen card of a given suit"""

    def __init__(self, suit: Suit):
        """ """
        super().__init__(suit)

    def get_value(self):
        """ Returns the value of the card """
        return 12

    def get_suit(self):
        """ Returns the suit of the card """
        return self.suit


class KingCard(PlayingCards):
    """ Creates the King card of a given suit"""

    def __init__(self, suit: Suit):
        """ """
        super().__init__(suit)

    def get_value(self):
        """ Returns the value of the card """
        return 13

    def get_suit(self):
        """ Returns the suit of the card """
        return self.suit


class AceCard(PlayingCards):
    """ Creates the Ace card of a given suit"""

    def __init__(self, suit: Suit):
        """ """
        super().__init__(suit)

    def get_value(self):
        """ Returns the value of the card """
        return 14

    def get_suit(self):
        """ Returns the suit of the card """
        return self.suit


class EmptyDeckError(Exception):
    def __init__(self):
        """Beskrivning"""
        #self.value = value

    def __str__(self):
        return print("Cannot remove cards from empty deck.")


class Hand:
    def __init__(self):
        """ """
        self.cards = []

    def __str__(self):
        """ Returns a readable format of value and suit """
        hand = []
        for card in self.cards:
            hand.append((card.get_value(), card.get_suit()))
        return repr(hand)

    def __getitem__(self, index):
        """ Returns a card at given index """
        return self.cards[index]

    def __len__(self):
        """ Returns the number of cards in hand """
        return len(self.cards)

    def add_card(self, card):
        """ Adds a card to the players hand. Takes a card as argument"""
        return self.cards.append(card)

    def remove_card(self, index=[]):
        """ Removes a card from the players hand. Takes an index as argument, starting from 0."""
        index.sort(reverse=True)
        #print(index)
#        for i in index:
#            self.cards.remove(i)
#        return self.cards


    def sort_cards(self):
        """ Sorts the cards on hand from lowest to highest"""
        return self.cards.sort()

    def best_poker_hand(self, cards=[]):
        cards = self.cards + cards

        """ Calculates the best poker hand."""
        if PokerHand.check_straight_flush(cards):
            print("Your best hand is a straight flush. Highest card:", PokerHand.check_straight_flush(self, cards))
        elif PokerHand.check_straight_flush(self, cards):
            pass
        elif PokerHand.check_four_of_a_kind(self, cards):
            pass
        elif PokerHand.check_full_house(self, cards):
            pass
        elif PokerHand.check_flush(self, cards):
            pass
        elif PokerHand.check_straight(self, cards):
            pass
        elif PokerHand.check_three_of_a_kind(self, cards):
            pass
        elif PokerHand.check_two_pair(self, cards):
            print("Two pairs:", PokerHand.cards)
        elif PokerHand.check_one_pair(self, cards):
            print("One pair:", PokerHand.cards)
        elif PokerHand.check_high_card(self, cards):
            print("High cards:", PokerHand.cards)


class StandardDeck:
    """ A class that represent a standard card game deck, with functions
    for creating a complete deck and shuffling it."""

    def __init__(self):
        self.cards = []

#    def __str__(self): # This never gets called
#        return str(self.cards)

    def __repr__(self):
        return repr(self.cards)

    def __eq__(self, other):
        return self.cards == other.cards

    def __len__(self):
        """ """
        return len(self.cards)

#    def __setitem__(self, key, value):
#        super().__setitem__(key, value)

#    def __getitem__(self, key):
#        super().__getitem__(key)

    def create_deck(self):
        """ Creates a standard deck of 52 cards"""
        for i in range(9):
            for suit in Suit:
                self.cards.append(NumberedCard(i + 2, suit))
        for suit in Suit:
            self.cards.append(JackCard(suit))
        for suit in Suit:
            self.cards.append(QueenCard(suit))
        for suit in Suit:
            self.cards.append(KingCard(suit))
        for suit in Suit:
            self.cards.append(AceCard(suit))
        return self.cards

    def shuffle(self):
        return random.shuffle(self.cards)


class PokerHand(Hand):
    """ A class that represent the poker hand with functions for identifying the best poker hand."""

    def __init__(self, cards):
        super().__init__()
        self.cards = cards

    def check_high_card(self, cards=[]):
        """ Checks for the highest card in a list of cards and returns it.
           Takes a list of tuples and return the biggest tuple. Starts with the first element, then the second etc"""

        cards = self.cards + cards
        highest_card = cards[0]

        for card in cards:
            if card > highest_card:
                highest_card = card
        PokerHand.cards = highest_card  # Makes it possible to access the cards somewhere else
        return highest_card

    def check_one_pair(self, cards=[]):
        """ Checks for the best pair in a list of cards. If no pair is found it returns None.

        :param cards: List of cards to check in addition of self.
        :return: A list containing the best pair in seperate tuples for each card. Returns None if no pair is found.
        """
        cards = self.cards + cards
        cards.sort(reverse=True)
        pairs = []
        print(cards)

        for i in range(len(cards)):
            for j in range(i+1, len(cards)):
                if cards[i].get_value() == cards[j].get_value():
                    if cards[i] not in pairs:
                        pairs.append(cards[i])
                    if cards[j] not in pairs:
                        pairs.append(cards[j])
        return pairs[:2]

    def check_two_pair(self, cards=[]):
        """ Returns the two highest pairs if cards_to_evaluate has at least two pairs in it.
            If less than two pairs are found it returns None. """
        cards = self.cards + cards
        cards.sort(reverse=True)
        pairs = []
        print(cards)

        for i in range(len(cards)):
            for j in range(i+1, len(cards)):
                if cards[i].get_value() == cards[j].get_value():
                    if cards[i] not in pairs:
                        pairs.append(cards[i])
                    if cards[j] not in pairs:
                        pairs.append(cards[j])
        print(pairs)
        return pairs[:4]


    def check_three_of_a_kind(self, cards):
        triplet = []
        values = []
        cards = self.cards + cards
        cards.sort()
        """
               for ...
            if card[i].get_value() == (card[i+1].get_value() and card[i+2].get_value()):
                triplet.append(card[i], card[i+1], card[i+2])
        """
        for c in reversed(cards):
            values.append((cards.get_value(), cards.get_suit()))
        for i in range(len(values)):
            for j in range(len(values)):
                # Check if the value of card i and card j is the same and whether or not they are not already in
                # the list of pairs
                if values[i][0] == values[j][0] and values[i][1] != values[j][1] and \
                        (values[i] not in triplet or values[j] not in triplet):
                    triplet += values[i], values[j]
        # Return the pair with the highest value, return None if no pair exist
        if len(triplet) >= 3:
            return hq.nlargest(3, triplet)
        else:
            pass

    def check_straight(self, cards=[]):
        """ Checks for the best straight in a list of cards.

        :return: The value of the top card, if no straight is found the return is None.
        """
        values = []
        cards = self.cards + cards
        cards.sort()

        for card in cards:
            values.append(card.get_value())

        for card in cards:
            if card.get_value() == 14:
                values.append(1)

        for card in reversed(cards):
            found_straight = True

            for k in range(1, 5):
                if (card.get_value() - k) not in values:
                    found_straight = False
                    break
            if found_straight:
                return card.get_value()

    def check_flush(self, cards=[]):
        """ Checks for the best flush in a list of cards. It can handle multiple flushes
        within a single list of cards.

        :param cards:
        :return: Returns a list of the five highest cards of the suit with the highest flush.
        """
        cards = self.cards + cards
        cards.sort(reverse=True)
        club_cards = []
        diamond_cards = []
        spade_cards = []
        heart_cards = []
        list_of_flushes = [[], [], [], []]

        for card in cards:
            if card.get_suit() == Suit.clubs:
                club_cards.append(card)
                if len(club_cards) >= 5:
                    list_of_flushes[0] = club_cards
            if card.get_suit() == Suit.diamonds:
                diamond_cards.append(card)
                if len(diamond_cards) >= 5:
                    list_of_flushes[1] = diamond_cards
            if card.get_suit() == Suit.spades:
                spade_cards.append(card)
                if len(spade_cards) >= 5:
                    list_of_flushes[2] = spade_cards
            if card.get_suit() == Suit.hearts:
                heart_cards.append(card)
                if len(heart_cards) >= 5:
                    list_of_flushes[3] = heart_cards
        return max(list_of_flushes)[:5]

    def check_full_house(self):
        pass

    def check_four_of_a_kind(self):
        pass

    def check_straight_flush(self, cards=[]): # Lägg till suit för vinnande kortet
        values = []
        cards = self.cards + cards
        cards.sort(reverse=True)
        for card in cards:
            values.append((card.get_value(), card.get_suit()))

        for card in cards:
            if card.get_value() == 14:
                values.append((1, card.get_suit()))

        for card in cards:
            found_straight = True

            for k in range(1, 5):
                if (card.get_value() - k, card.get_suit()) not in values:
                    found_straight = False
                    break
            if found_straight:
                return card.get_value()

'''
        for card in cards:
            values.append((card.get_value(), card.get_suit()))

        for i in range(len(values)):
            for j in range(len(values)):
                # Check if the value of card i and card j is the same and whether or not they are not already in
                # the list of pairs
                if values[i][0] == values[j][0] and values[i][1] != values[j][1] and \
                        (values[i] not in pairs or values[j] not in pairs):
                    pairs += [values[i], values[j]]
        print('pairs:', pairs)
        print(type(pairs))
        #print(pairs[0])
        print(type(pairs[0]))
        # Return the pair with the highest value, return None if no pair exist
        if len(pairs) >= 2:
            return hq.nlargest(2, pairs)
        else:
            pass
'''

'''
        list_of_suits = [[], [], [], []]
        for card in cards:
            for suit in Suit:
                if card.get_suit() == suit:
                    list_of_suits[suit].append(card)
                    if len(list_of_suits[suit]) >= 5:
                        list_of_flushes[suit].append(list_of_suits[suit])
        return max(list_of_flushes)
'''

'''
        for card in cards:
            values.append(card.get_value())
        for card in cards:
            values.remove(card.get_value())
            if card.get_value() in values:
                pairs.append(card)
                
        return hq.nlargest(2, pairs)
'''