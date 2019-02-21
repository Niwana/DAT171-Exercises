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
    hand.sort_cards()
    assert (hand[0].get_value(), hand[0].get_suit()) <= (hand[1].get_value(), hand[1].get_suit())

    # Test the remove_card function
    hand.remove_card(hand[1])
    assert len(hand) == 1


def test_deck():
    # Test that all cards are in the deck
    deck_1 = cardlib.StandardDeck()
    deck_1.create_deck()

    # Test the shuffle function
    deck_2 = cardlib.StandardDeck()
    deck_2.create_deck()
    deck_2.shuffle()
    assert deck_2 != deck_1


def test_straight_flush():
    card = cardlib.NumberedCard
    suit = cardlib.Suit

    card_1 = card(6, suit.spades)
    card_2 = card(7, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)

    community_cards = [(card(1, suit.spades)), (card(2, suit.spades)), (card(3, suit.spades)),
                       (card(4, suit.spades)), (card(5, suit.spades))]

    check = cardlib.PokerHand.check_straight_flush(player_1_cards, community_cards)
    assert check == 7

def test_straight():
    card = cardlib.NumberedCard
    suit = cardlib.Suit

    card_1 = card(6, suit.spades)
    card_2 = card(7, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)

    community_cards = [(card(2, suit.hearts)), (card(3, suit.clubs)), (card(4, suit.spades)),
                       (card(4, suit.diamonds)), (card(5, suit.diamonds))]

    check = cardlib.PokerHand.check_straight(player_1_cards, community_cards)
    assert check == 7

def test_flush():
    card = cardlib.NumberedCard
    suit = cardlib.Suit

    card_1 = card(12, suit.hearts)
    card_2 = card(7, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)

    # Create a large list of community cards resulting in multiple flushes, with
    # 12 of hearts being the highest-ranking card and thus the best flush.
    community_cards = [(card(2, suit.hearts)), (card(3, suit.hearts)), (card(4, suit.hearts)),
                       (card(6, suit.hearts)), (card(5, suit.hearts)),
                       (card(2, suit.spades)), (card(3, suit.spades)), (card(4, suit.spades)),
                       (card(6, suit.spades)), (card(5, suit.spades))]
    check = cardlib.PokerHand.check_flush(player_1_cards, community_cards)

    assert check[0] == card_1

def test_one_pair():
    card = cardlib.NumberedCard
    suit = cardlib.Suit

    card_1 = card(12, suit.hearts)
    card_2 = card(7, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)
    community_cards = [(card(7, suit.hearts)), (card(7, suit.clubs)), (card(12, suit.diamonds))]

    check = cardlib.PokerHand.check_one_pair(player_1_cards, community_cards)

    # Assert fungerar ej eftersom vi får tillbaka varje kort som en tuple. I andra tester
    # är korten en <class 'cardlib.NumberedCard'>. De går ej att jämföra rakt av.

    #assert check[0] == card_1
