import cardlib

card = cardlib.NumberedCard
hand = cardlib.Hand()
# num_card = cardlib.NumberedCard
# queen_card =
suit = cardlib.Suit


def test_cards():
    card_1 = cardlib.NumberedCard(2, cardlib.Suit.clubs)
    assert card_1.get_value() == 2
    assert card_1.get_suit() == 0

    card_2 = cardlib.JackCard(cardlib.Suit.diamonds)
    assert card_2.get_value() == 11
    assert card_2.get_suit() == 1

    card_3 = cardlib.QueenCard(cardlib.Suit.spades)
    assert card_3.get_value() == 12
    assert card_3.get_suit() == 2

    card_4 = cardlib.KingCard(cardlib.Suit.diamonds)
    assert card_4.get_value() == 13
    assert card_4.get_suit() == 1

    card_5 = cardlib.AceCard(cardlib.Suit.diamonds)
    assert card_5.get_value() == 14
    assert card_5.get_suit() == 1


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
    # Test the add_card function
    hand.add_card(card(5, cardlib.Suit.spades))
    hand.add_card(card(5, cardlib.Suit.diamonds))
    hand.add_card(card(7, cardlib.Suit.diamonds))
    assert len(hand) == 3

    # Test the sort function
    hand.sort_cards()
    assert (hand[0].get_value(), hand[0].get_suit()) <= (hand[1].get_value(), hand[1].get_suit())

    # Test the remove_card function
    hand.remove_card([2, 1])
    hand.remove_card([0])

    assert len(hand) == 0


def test_deck():
    # Test that all cards are in the deck
    deck_1 = cardlib.StandardDeck()
    deck_1.create_deck()
    assert len(deck_1) == 52

    # Test the shuffle function
    deck_2 = cardlib.StandardDeck()
    deck_2.create_deck()
    deck_2.shuffle()
    assert deck_2 != deck_1


def test_high_card():
    card_1 = card(9, suit.hearts)
    card_2 = card(7, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)
    community_cards = [(card(2, suit.hearts)), (card(3, suit.clubs)), (card(4, suit.spades)),
                       (card(4, suit.diamonds)), (card(5, suit.diamonds))]

    check = cardlib.PokerHand.check_high_card(player_1_cards, community_cards)
    assert check == [card(9, suit.hearts)]


def test_one_pair():
    card_1 = card(5, suit.hearts)
    card_2 = card(4, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)
    community_cards = [(card(2, suit.hearts)), (card(2, suit.clubs)), (card(4, suit.spades)),
                       (card(4, suit.diamonds)), (card(5, suit.diamonds))]

    check = cardlib.PokerHand.check_one_pair(player_1_cards, community_cards)
    assert check == [card(5, suit.hearts), card(5, suit.diamonds)]


def test_two_pair():
    card_1 = card(5, suit.hearts)
    card_2 = card(4, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)
    community_cards = [(card(2, suit.hearts)), (card(5, suit.clubs)), (card(1, suit.spades)),
                       (card(4, suit.diamonds)), (card(5, suit.diamonds))]

    check = cardlib.PokerHand.check_two_pair(player_1_cards, community_cards)
    assert check == [card(5, suit.hearts), card(5, suit.diamonds), card(4, suit.spades), card(4, suit.diamonds)]


def test_three_of_a_kind():
    card_1 = card(7, suit.hearts)
    card_2 = card(9, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)
    community_cards = [(card(9, suit.hearts)), (card(3, suit.diamonds)), (card(7, suit.clubs)),
                       (card(7, suit.diamonds)), (card(2, suit.clubs))]

    check = cardlib.PokerHand.check_three_of_a_kind(player_1_cards, community_cards)
    assert check == [(card(7, suit.hearts)), (card(7, suit.diamonds)), (card(7, suit.clubs))]


def test_straight():
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


def test_full_house():
    card_1 = card(7, suit.hearts)
    card_2 = card(9, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)
    community_cards = [(card(9, suit.hearts)), (card(10, suit.spades)), (card(7, suit.clubs)),
                       (card(10, suit.diamonds)), (card(1, suit.spades)), card(9, suit.clubs)]

    check = cardlib.PokerHand.check_full_house(player_1_cards, community_cards)
    assert check == [(card(9, suit.hearts)), (card(9, suit.spades)), (card(9, suit.clubs)), (card(10, suit.spades)), (card(10, suit.diamonds))]


def test_four_of_a_kind():
    card_1 = card(7, suit.hearts)
    card_2 = card(9, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)
    community_cards = [(card(9, suit.hearts)), (card(3, suit.diamonds)), (card(7, suit.clubs)),
                       (card(7, suit.diamonds)), (card(7, suit.spades))]

    check = cardlib.PokerHand.check_four_of_a_kind(player_1_cards, community_cards)
    assert check == [(card(7, suit.hearts)), (card(7, suit.spades)), (card(7, suit.diamonds)), (card(7, suit.clubs))]


def test_straight_flush():
    card_1 = card(6, suit.spades)
    card_2 = card(7, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)

    community_cards = [(card(1, suit.spades)), (card(2, suit.spades)), (card(3, suit.spades)),
                       (card(4, suit.spades)), (card(5, suit.spades))]

    check = cardlib.PokerHand.check_straight_flush(player_1_cards, community_cards)
    assert check == [card(7, suit.spades)]


def test_best_poker_hand():
    deck_1 = cardlib.StandardDeck()
    deck_1.create_deck()

    card_1 = card(6, suit.spades)
    card_2 = card(7, suit.hearts)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)
    check_high_card = cardlib.PokerHand.best_poker_hand(player_1_cards)
#    assert check_high_card == card_2



#test_best_poker_hand()