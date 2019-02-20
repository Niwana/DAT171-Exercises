import cardlib


def test_cards():
    # Test if the created cards has correct value and suit
    card_1 = cardlib.NumberedCard(2, cardlib.Suit.clubs)
    assert card_1.get_value() == 2
    assert card_1.get_suit() == 0

    card = cardlib.JackCard(cardlib.Suit.diamonds)
    assert card.get_value() == 11
    assert card.get_suit() == 1

    card = cardlib.QueenCard(cardlib.Suit.spades)
    assert card.get_value() == 12
    assert card.get_suit() == 2

    card = cardlib.KingCard(cardlib.Suit.diamonds)
    assert card.get_value() == 13
    assert card.get_suit() == 1

    card = cardlib.AceCard(cardlib.Suit.diamonds)
    assert card.get_value() == 14
    assert card.get_suit() == 1


def test_comparison_of_cards():
    card_1 = cardlib.NumberedCard(2, cardlib.Suit.clubs)
    card_2 = cardlib.NumberedCard(2, cardlib.Suit.clubs)
    card_3 = cardlib.NumberedCard(3, cardlib.Suit.clubs)
    card_4 = cardlib.NumberedCard(2, cardlib.Suit.hearts)
    card_5 = cardlib.NumberedCard(2, cardlib.Suit.hearts)

    # Test comparison of values for different cards
    assert card_1 == card_2
    assert card_2 < card_3

    # Test comparison of suits for different cards
    assert card_4 == card_5
    assert card_4 > card_1


def test_hand():
    # Creates a hand of two cards
    hand = cardlib.Hand()
    card = cardlib.NumberedCard

    # Test the add_card function
    hand.add_card(card(5, cardlib.Suit.spades))
    hand.add_card(card(5, cardlib.Suit.diamonds))
    assert len(hand) == 2

    # Test the sort function
    print(hand)
    hand.sort_cards()
    print(hand)
    assert (hand[0].get_value(), hand[0].get_suit()) <= (hand[1].get_value(), hand[1].get_suit())

    # Test the remove_card function
    hand.remove_card(hand[1])
    assert len(hand) == 1


def test_deck():
    # Test that all cards are in the deck
    deck_1 = cardlib.StandardDeck()
    deck_1.create_deck()
    print(deck_1)

    # Test the shuffle function
    deck_2 = cardlib.StandardDeck()
    deck_2.create_deck()
    deck_2.shuffle()
    assert deck_2 != deck_1

'''
    a = [(1,cardlib.Suit.clubs),(2,cardlib.Suit.clubs)]
    b = [(1,cardlib.Suit.clubs),(2,cardlib.Suit.clubs)]
    c = [(2,cardlib.Suit.clubs),(1,cardlib.Suit.clubs)]

    print(a == c)
'''

test_deck()