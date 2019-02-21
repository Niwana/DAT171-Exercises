import enum
import abc
import random
import heapq as hq
import math

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
        return repr((self.get_value(), str(self.get_suit()))) # This gets printed when calling StandardDeck(). Strange?

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

    def count_values(self, value):
        val = 0
        for i in self:
            if i.count(value):
                print(i.count(value))
                val += 1
        return val


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

    def remove_card(self, index):
        """ Removes a card from the players hand. Takes an index as argument, starting from 0."""
        return self.cards.remove(index)

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
        return 52

    def __setitem__(self, key, value):
        super().__setitem__(key, value)

    def __getitem__(self, key):
        super().__getitem__(key)

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


class PokerHand(list):
    def __init__(self, cards):
        super().__init__()
        self.cards = cards

    def check_high_card(self):
        """ CChecks for the highest card in a list of cards and returns it.
           Takes a list of tuples and return the biggest tuple. Starts with the first element, than the second """

        highest_card = ()
        for i in range(len(self)):
            if self[i] > highest_card:
                highest_card = self[i]
            else:
                pass
        PokerHand.cards = highest_card  # Makes it possible to access the cards somewhere else
        return highest_card

    def check_one_pair(self):
        """ Returns the highest pair if cards_to_evaluate has a pair in it. If no pair is found it returns None. """
        """
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
        """

        pairs = []
        values = []
        for c in reversed(self):
            values.append((c.get_value(), c.get_suit()))
        for i in range(len(values)):
            for j in range(len(values)):
                # Check if the value of card i and card j is the same and whether or not they are not already in
                # the list of pairs
                if values[i][0] == values[j][0] and values[i][1] != values[j][1] and \
                        (values[i] not in pairs or values[j] not in pairs):
                    pairs += values[i], values[j]
        # Return the pair with the highest value, return None if no pair exist
        print(pairs)
        if len(pairs) >= 2:
            return hq.nlargest(2, pairs)
        else:
            pass

    def check_two_pair(self):
        """ Returns the two highest pairs if cards_to_evaluate has at least two pairs in it.
               If less than two pairs are found it returns None. """
        pairs = []
        values = []
        for card in reversed(self):
            values.append((card.get_value(), card.get_suit()))
        for i in range(len(values)):
            for j in range(len(values)):
                # Check if the value of card i and card j is the same and whether or not they are not already in
                # the list of pairs
                if values[i][0] == values[j][0] and values[i][1] != values[j][1] and \
                        (values[i] not in pairs or values[j] not in pairs):
                    pairs += values[i], values[j]
        # Return the pairs with the highest value, return None if less than two pairs exist
        print(pairs)
        if len(pairs) >= 4:  # GER FELAKTIGT RESULTAT, KAN EJ HANTERA 3 + 2 KORT
            return hq.nlargest(4, pairs)
        else:
            pass

    def check_three_of_a_kind(self):
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
        values = []
        cards = self.cards + cards
        cards.sort()

        flush_spades = []
        flush_clubs = []
        flush_diamonds = []
        flush_hearts = []
        print(cards)
        print(type(cards))

        card = NumberedCard
        suit = Suit

        #print(cards.count_values(cards, Suit.spades))

        for card in cards:
            values.append((card.get_value(), card.get_suit()))


        for card in reversed(cards):
            if card.get_suit() == Suit.spades:
                flush_spades.append(card)
            if card.get_suit() == Suit.clubs:
                flush_clubs.append(card)
            if card.get_suit() == Suit.diamonds:
                flush_diamonds.append(card)
            if card.get_suit() == Suit.hearts:
                flush_hearts.append(card)
        print(len(max(flush_spades)))

#        print(max(flush_spades if (flush_spades) >= 5))
        #return max((flush_spades if len(flush_spades) >= 5), (flush_clubs if len(flush_clubs) >= 5), (flush_diamonds if len(flush_diamonds) >= 5), (flush_hearts if len(flush_hearts) >= 5))

    def check_full_house(self):
        pass

    def check_four_of_a_kind(self):
        pass

    def check_straight_flush(self, cards=[]): # Lägg till suit för vinnande kortet
        values = []
        cards = self.cards + cards
        cards.sort()
        for card in cards:
            values.append((card.get_value(), card.get_suit()))

        for card in cards:
            if card.get_value() == 14:
                values.append((1, card.get_suit()))

        for card in reversed(cards):
            found_straight = True

            for k in range(1, 5):
                if (card.get_value() - k, card.get_suit()) not in values:
                    found_straight = False
                    break
            if found_straight:
                return card.get_value()



community_cards = [(NumberedCard(1, Suit.spades)), (NumberedCard(2, Suit.spades)), (NumberedCard(3, Suit.spades)),
                   (NumberedCard(4, Suit.spades)), (NumberedCard(5, Suit.spades))]
#player_1_cards = [(NumberedCard(6, Suit.spades)), (NumberedCard(7, Suit.spades))]

#cards_to_evaluate = community_cards + player_1_cards

card_1 = NumberedCard(6, Suit.spades)
card_2 = NumberedCard(4, Suit.spades)

player_1_cards = Hand()

player_1_cards.add_card(card_1)
player_1_cards.add_card(card_2)





