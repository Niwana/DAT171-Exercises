import enum
import abc
from random import shuffle


# ♣♦♠♥


class Suit(enum.IntEnum):
    """ Class Suit contains the four suits (club, diamond, spade, heart) and their respective order
    (club < diamond < spade < heart)"""
    clubs = 0
    diamonds = 1
    spades = 2
    hearts = 3

    def __str__(self):
        """ Returns the name and symbol of the suit. """
        if self.name == 'clubs':
            return self.name + ' ♣'
        if self.name == 'diamonds':
            return self.name + ' ♦'
        if self.name == 'spades':
            return self.name + ' ♠'
        if self.name == 'hearts':
            return self.name + ' ♥'


class PlayingCards(metaclass=abc.ABCMeta):
    """ This is an abstract class for the playing cards. """

    def __init__(self, suit: Suit):
        self.suit = suit

    def __str__(self):
        """ Returns a readable format of value and suit. """
        return "{}, {}".format(self.get_value(), str(self.get_suit()))

    def __repr__(self):
        """ Returns a readable format of value and suit from a list. """
        # This gets printed when calling StandardDeck(). Strange?
        return repr((self.get_value(), str(self.get_suit())))

    def __lt__(self, other):
        """ Returns self < other """
        return (self.get_value(), self.get_suit()) < (other.get_value(), other.get_suit())

    def __eq__(self, other):
        """ Returns self == other """
        return (self.get_value(), self.get_suit()) == (other.get_value(), other.get_suit())

    @abc.abstractmethod
    def get_value(self):
        """ Returns the value of the card. """
        raise NotImplementedError("Derived class did not override this method")

    @abc.abstractmethod
    def get_suit(self):
        """ Returns the suit of the card. """
        raise NotImplementedError("Derived class did not override this method")


class NumberedCard(PlayingCards):
    """ Creates a card of a given value and suit. Only used for cards 2-10. """

    def __init__(self, value: int, suit: Suit):
        self.value = value
        super().__init__(suit)

    def get_value(self):
        """ Returns the value of the card. """
        return self.value

    def get_suit(self):
        """ Returns the suit of the card. """
        return self.suit


class JackCard(PlayingCards):
    """ Creates the Jack card of a given suit. """

    def __init__(self, suit: Suit):
        super().__init__(suit)

    def get_value(self):
        """ Returns the value of the card. """
        return 11

    def get_suit(self):
        """ Returns the suit of the card. """
        return self.suit


class QueenCard(PlayingCards):
    """ Creates the Queen card of a given suit. """

    def __init__(self, suit: Suit):
        super().__init__(suit)

    def get_value(self):
        """ Returns the value of the card. """
        return 12

    def get_suit(self):
        """ Returns the suit of the card. """
        return self.suit


class KingCard(PlayingCards):
    """ Creates the King card of a given suit. """

    def __init__(self, suit: Suit):
        super().__init__(suit)

    def get_value(self):
        """ Returns the value of the card. """
        return 13

    def get_suit(self):
        """ Returns the suit of the card. """
        return self.suit


class AceCard(PlayingCards):
    """ Creates the Ace card of a given suit. """

    def __init__(self, suit: Suit):
        super().__init__(suit)

    def get_value(self):
        """ Returns the value of the card. """
        return 14

    def get_suit(self):
        """ Returns the suit of the card. """
        return self.suit


class EmptyDeckError(Exception):
    def __init__(self):
        """ Raises an error when the user's trying to remove a card from an empty deck. """

    def __str__(self):
        return print("Cannot remove cards from empty deck!")


class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        """ Returns a readable format of value and suit. """
        hand = []
        for card in self.cards:
            hand.append((card.get_value(), str(card.get_suit())))
        return repr(hand)

    def __getitem__(self, index):
        """ Returns a card at given index. """
        return self.cards[index]

    def __len__(self):
        """ Returns the number of cards in hand. """
        return len(self.cards)

    def add_card(self, card):
        """ Adds a card to the players hand. Takes a card as argument"""
        return self.cards.append(card)

    def remove_card(self, index):
        """ Removes a card from the players hand. Takes a list containing indices as argument. """
        if len(self.cards) > 0:
            index.sort(reverse=True)
            for i in index:
                del self.cards[i]
            return self.cards
        else:
            raise EmptyDeckError

    def sort_cards(self):
        """ Sorts the cards on hand from lowest to highest. """
        return self.cards.sort()

    def best_poker_hand(self, cards=[]):
        """ Calculates the best poker hand. """

        p = PokerHand
        functions = [p.check_straight_flush, p.check_four_of_a_kind, p.check_full_house, p.check_flush,
                     p.check_straight, p.check_three_of_a_kind, p.check_two_pair, p.check_one_pair, p.check_high_card]
        # TODO: Körs fortfarande 2 gånger
        for function in functions:
            if function(self, cards) is not None:
                return function(self, cards)

        # p.type == Rank.high_card
        # p.highest_values


class StandardDeck:
    """ A class that represent a standard card game deck, with functions
    for creating a complete deck and shuffling it. """

    def __init__(self):
        self.cards = []

    def __repr__(self):
        """ Returns a readable format of the deck. """
        return repr(self.cards)

    def __eq__(self, other):
        """ Makes it possible to compare if two decks are the same. """
        return self.cards == other.cards

    def __len__(self):
        """ Returns the number of cards in the deck. """
        return len(self.cards)

    def __getitem__(self, index):
        """ Returns a card at given index. """
        return self.cards[index]

    def create_deck(self):
        """ Creates a standard deck of 52 cards. """
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
        """ Shuffles the cards in the deck. """
        return shuffle(self.cards)

    def draw_card(self, amount: int):
        """ Draws the specified amount of cards from the top of the deck. """
        drawn_cards = []
        for i in range(amount):
            drawn_cards.append(self.cards.pop(0))
        return drawn_cards


class Rank(enum.IntEnum):
    high_card = 0
    one_pair = 1
    two_pair = 2
    three_of_a_kind = 3
    straight = 4
    flush = 5
    full_house = 6
    four_of_a_kind = 7
    straight_flush = 8


class PokerHand:
    """ A class that represent the poker hand with functions for identifying the best poker hand. """

    def __init__(self):
        super().__init__()
        self.cards = []
        self.type = Rank
        self.highest_value = 0

    def __str__(self):
        """ Returns a readable format of value and suit. """
        return "type: {}, highest: {}".format(self.type, self.highest_value)

    def __lt__(self, other):
        """ Returns self < other """
        print(self.type, other.type)
        return self.type.value < other.type.value

    def check_high_card(self, cards=[]):
        """ Checks for the highest card in a list of cards and returns it.

        :param cards: List of cards to check in addition of self.
        :return: The card with the highest value.
        """
        # TODO: Får inte alla kort om inte cards = self.cards + cards
        #cards = self.cards + cards
        self.type = Rank.high_card
        print(cards)

        highest_card = cards[0]

        for card in cards:
            if card > highest_card:
                highest_card = card

        self.highest_value = (highest_card.get_value())
        return self # Hur får man detta till en PokerHand?
        #return self.highest_value, self.type

    def check_one_pair(self, cards=[]):
        """ Checks for the best pair in a list of cards. If no pair is found it returns None.

        :param cards: List of cards to check in addition of self.
        :return: A list containing the best pair in separate tuples for each card. Returns None if no pair is found.
        """
        #cards = self.cards + cards
        #cards.sort(reverse=True)
        self.type = Rank.one_pair
        values = []
        pairs = []

        for card in cards:
            values.append(card.get_value())

        for card in cards:
            if (values.count(card.get_value())) == 2 and len(pairs) < 2:
                pairs.append(card)
                self.highest_value = (card.get_value())

        if pairs:
            return self
            #return self.highest_value, self.type

    def check_two_pair(self, cards=[]):
        """ Returns the two highest pairs if the list of cards has at least two pairs in it.

        :param cards: List of cards to check in addition of self.
        :return: A list containing the best two pairs with the highest pair first. Returns None if no pairs are found.
        """
        cards = self.cards + cards
        cards.sort(reverse=True)
        self.type = Rank.two_pair
        values = []
        first_pair = []
        second_pair = []

        for card in cards:
            values.append(card.get_value())

        for card in cards:
            if (values.count(card.get_value())) >= 2 > len(first_pair):
                first_pair.append(card)
                self.highest_value = card.get_value()  # The first pair will always be the one with the highest value

        for card in cards:
            if (values.count(card.get_value())) >= 2 > len(second_pair) and \
                    card.get_value() != first_pair[0].get_value():
                second_pair.append(card)


        if first_pair and second_pair:
            return self.highest_value, self.type

    def check_three_of_a_kind(self, cards=[]):
        """ Checks if the list of cards contain three of a kind.

        :param cards: List of cards to check in addition of self.
        :return: A list containing the three cards as tuples. Returns None if no pair is found.
        """
        cards = self.cards + cards
        cards.sort(reverse=True)
        self.type = Rank.three_of_a_kind
        values = []

        for card in cards:
            values.append(card.get_value())

        for i, card in enumerate(cards):
            if (values.count(card.get_value())) >= 3:
                self.highest_value = card.get_value()
                return self.highest_value, self.type

    def check_straight(self, cards=[]):
        """ Checks for the best straight in a list of cards.

        :param cards: List of cards to check in addition of self.
        :return: The the highest value card in the straight. Returns None if no straight is found.
        """
        values = []

        cards = self.cards + cards
        cards.sort(reverse=True)
        self.type = Rank.straight

        for card in cards:
            values.append(card.get_value())

        for card in cards:
            if card.get_value() == 14:
                values.append(1)

        for card in cards:
            found_straight = True

            for k in range(1, 5):
                if (card.get_value() - k) not in values:
                    found_straight = False
                    break
            if found_straight:
                self.highest_value = card.get_value()
                return self.highest_value, self.type

    def check_flush(self, cards=[]):
        """ Checks for the best flush in a list of cards. It can handle multiple flushes
        within a single list of cards (if playing with more than one deck).

        :param cards: List of cards to check in addition of self.
        :return: Returns a list of the five highest cards of the suit with the highest flush. Returns None if
        no flush is found.
        """
        cards = self.cards + cards
        cards.sort(reverse=True)
        self.type = Rank.flush
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

        for i in range(len(list_of_flushes)):
            if list_of_flushes[i]:
                self.highest_value = max(list_of_flushes)[:5][0].get_value()
                return self.highest_value, self.type

    def check_full_house(self, cards=[]):
        """ Checks for the best full house in a list of cards.

        :param cards: List of cards to check in addition of self.
        :return: Returns a list with the triplet first and then the pair. Return None if no full house is found.
        """
        cards = self.cards + cards
        cards.sort(reverse=True)
        self.type = Rank.full_house
        values = []
        pair = []
        triplet = []

        for card in cards:
            values.append(card.get_value())

        for card in cards:
            if (values.count(card.get_value())) >= 3 > len(triplet):
                triplet.append(card)

        if triplet:
            for card in cards:
                if (values.count(card.get_value())) >= 2 > len(pair) and card.get_value() != triplet[0].get_value():
                    pair.append(card)
                    self.highest_value = card.get_value()

        if triplet and pair:
            return self.highest_value, self.type

    def check_four_of_a_kind(self, cards=[]):
        """ Checks if the list of cards contain four of a kind.

        :param cards: List of cards to check in addition of self.
        :return: Returns a list containing four cards. Returns None if no four of a kind is found.
        """
        cards = self.cards + cards
        cards.sort(reverse=True)
        self.type = Rank.four_of_a_kind
        values = []
        for card in cards:
            values.append(card.get_value())

        for i, card in enumerate(cards):
            if (values.count(card.get_value())) >= 4:
                self.highest_value = card.get_value()
                return self.highest_value, self.type

    def check_straight_flush(self, cards=[]):
        """ Checks a list of cards for the best straight flush.

        :param cards: List of cards to check in addition of self.
        :return: Returns the highest-ranking card in the flush. If no flush is found it returns None.
        """
        values = []
        cards = self.cards + cards
        cards.sort(reverse=True)
        self.type = Rank.straight_flush

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
                self.highest_value = card.get_value()
                return self.highest_value, self.type
