import cardlib

num_card = cardlib.NumberedCard
jack_card = cardlib.JackCard
queen_card = cardlib.QueenCard
king_card = cardlib.KingCard
ace_card = cardlib.AceCard

hand = cardlib.Hand()


suit = cardlib.Suit


def test_cards():
    card_1 = num_card(2, cardlib.Suit.clubs)
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
    card_1 = num_card(2, cardlib.Suit.clubs)
    card_2 = num_card(2, cardlib.Suit.clubs)
    card_3 = num_card(3, cardlib.Suit.clubs)
    card_4 = num_card(2, cardlib.Suit.hearts)
    card_5 = num_card(2, cardlib.Suit.hearts)

    # Test comparison of values for different cards
    assert card_1 == card_2
    assert card_2 < card_3

    # Test comparison of suits for different cards
    assert card_4 == card_5
    assert card_4 > card_1


def test_hand():
    # Test the add_card function
    hand.add_card(num_card(5, cardlib.Suit.spades))
    hand.add_card(num_card(5, cardlib.Suit.diamonds))
    hand.add_card(num_card(7, cardlib.Suit.diamonds))
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

    # Test the draw function
    drawn_cards = deck_1.draw_card(5)
    assert drawn_cards[0] == num_card(2, suit.clubs) and drawn_cards[4] == num_card(3, suit.clubs)
    assert len(deck_1) < 52
    assert drawn_cards[0] not in deck_1


def test_high_card():
    card_1 = num_card(9, suit.hearts)
    card_2 = num_card(7, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)
    community_cards = [(num_card(2, suit.hearts)), (num_card(3, suit.clubs)), (num_card(4, suit.spades)),
                       (num_card(4, suit.diamonds)), (num_card(5, suit.diamonds))]

    check = cardlib.PokerHand.check_high_card(player_1_cards, community_cards)
    assert check == [num_card(9, suit.hearts)]


def test_one_pair():
    card_1 = num_card(5, suit.hearts)
    card_2 = num_card(4, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)
    community_cards = [(num_card(2, suit.hearts)), (num_card(2, suit.clubs)), (num_card(4, suit.spades)),
                       (num_card(4, suit.diamonds)), (num_card(5, suit.diamonds))]

    check = cardlib.PokerHand.check_one_pair(player_1_cards, community_cards)
    assert check == [num_card(5, suit.hearts), num_card(5, suit.diamonds)]


def test_two_pair():
    card_1 = num_card(5, suit.hearts)
    card_2 = num_card(4, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)
    community_cards = [(num_card(2, suit.hearts)), (num_card(5, suit.clubs)), (num_card(1, suit.spades)),
                       (num_card(4, suit.diamonds)), (num_card(5, suit.diamonds))]

    check = cardlib.PokerHand.check_two_pair(player_1_cards, community_cards)
    assert check == [num_card(5, suit.hearts), num_card(5, suit.diamonds), num_card(4, suit.spades), num_card(4, suit.diamonds)]


def test_three_of_a_kind():
    card_1 = num_card(7, suit.hearts)
    card_2 = num_card(9, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)
    community_cards = [(num_card(9, suit.hearts)), (num_card(3, suit.diamonds)), (num_card(7, suit.clubs)),
                       (num_card(7, suit.diamonds)), (num_card(2, suit.clubs))]

    check = cardlib.PokerHand.check_three_of_a_kind(player_1_cards, community_cards)
    assert check == [(num_card(7, suit.hearts)), (num_card(7, suit.diamonds)), (num_card(7, suit.clubs))]


def test_straight():
    card_1 = num_card(6, suit.spades)
    card_2 = num_card(7, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)

    community_cards = [(num_card(2, suit.hearts)), (num_card(3, suit.clubs)), (num_card(4, suit.spades)),
                       (num_card(4, suit.diamonds)), (num_card(5, suit.diamonds))]
    check = cardlib.PokerHand.check_straight(player_1_cards, community_cards)
    assert check == [num_card(7, suit.spades)]


def test_flush():
    card_1 = num_card(12, suit.hearts)
    card_2 = num_card(7, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)

    # Create a large list of community cards resulting in multiple flushes, with
    # 12 of hearts being the highest-ranking card and thus the best flush.
    community_cards = [(num_card(2, suit.hearts)), (num_card(3, suit.hearts)), (num_card(4, suit.hearts)),
                       (num_card(6, suit.hearts)), (num_card(5, suit.hearts)),
                       (num_card(2, suit.spades)), (num_card(3, suit.spades)), (num_card(4, suit.spades)),
                       (num_card(6, suit.spades)), (num_card(5, suit.spades))]
    check = cardlib.PokerHand.check_flush(player_1_cards, community_cards)
    assert check[0] == card_1


def test_full_house():
    card_1 = num_card(7, suit.hearts)
    card_2 = num_card(9, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)
    community_cards = [(num_card(9, suit.hearts)), (num_card(10, suit.spades)), (num_card(7, suit.clubs)),
                       (num_card(10, suit.diamonds)), (num_card(1, suit.spades)), num_card(9, suit.clubs)]

    check = cardlib.PokerHand.check_full_house(player_1_cards, community_cards)
    assert check == [(num_card(9, suit.hearts)), (num_card(9, suit.spades)), (num_card(9, suit.clubs)), (num_card(10, suit.spades)), (num_card(10, suit.diamonds))]


def test_four_of_a_kind():
    card_1 = num_card(7, suit.hearts)
    card_2 = num_card(9, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)
    community_cards = [(num_card(9, suit.hearts)), (num_card(3, suit.diamonds)), (num_card(7, suit.clubs)),
                       (num_card(7, suit.diamonds)), (num_card(7, suit.spades))]

    check = cardlib.PokerHand.check_four_of_a_kind(player_1_cards, community_cards)
    assert check == [(num_card(7, suit.hearts)), (num_card(7, suit.spades)), (num_card(7, suit.diamonds)), (num_card(7, suit.clubs))]


def test_straight_flush():
    card_1 = num_card(6, suit.spades)
    card_2 = num_card(7, suit.spades)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)

    community_cards = [(num_card(1, suit.spades)), (num_card(2, suit.spades)), (num_card(3, suit.spades)),
                       (num_card(4, suit.spades)), (num_card(5, suit.spades))]

    check = cardlib.PokerHand.check_straight_flush(player_1_cards, community_cards)
    assert check == [num_card(7, suit.spades)]

'''
def test_best_poker_hand():
    deck_1 = cardlib.StandardDeck()
    deck_1.create_deck()

    card_1 = num_card(9, suit.spades)
    card_2 = ace_card(suit.hearts)

    player_1_cards = cardlib.Hand()
    player_1_cards.add_card(card_1)
    player_1_cards.add_card(card_2)

    # High card
    community_cards = [(num_card(1, suit.diamonds)), (num_card(8, suit.spades)), (num_card(3, suit.spades)),
                       (num_card(4, suit.clubs)), (num_card(5, suit.spades))]
    check_high_card = player_1_cards.best_poker_hand(community_cards)
#    assert check_high_card == [card_2]

    # One pair
    community_cards = [(num_card(3, suit.diamonds)), (num_card(8, suit.spades)), (num_card(3, suit.spades)),
                       (num_card(4, suit.clubs)), (num_card(5, suit.spades))]
    check_one_pair = player_1_cards.best_poker_hand(community_cards)
#    assert check_one_pair == [num_card(3, suit.spades), num_card(3, suit.diamonds)]

    # Two pairs
    community_cards = [(num_card(3, suit.diamonds)), (num_card(8, suit.spades)), (num_card(3, suit.spades)),
                       (num_card(4, suit.clubs)), (ace_card(suit.spades))]
    check_two_pairs = player_1_cards.best_poker_hand(community_cards)
#    assert check_two_pairs == [ace_card(suit.hearts), ace_card(suit.spades),
#                               num_card(3, suit.spades), num_card(3, suit.diamonds)]

    # Three of a kind
    community_cards = [(num_card(3, suit.diamonds)), (num_card(3, suit.clubs)), (num_card(3, suit.spades)),
                       (num_card(4, suit.clubs)), (num_card(2, suit.spades))]
    check_three_of_a_kind = player_1_cards.best_poker_hand(community_cards)
#    assert check_three_of_a_kind == [(num_card(3, suit.spades)),
#                                     (num_card(3, suit.diamonds)), (num_card(3, suit.clubs))]

    # Straight
    community_cards = [(num_card(7, suit.diamonds)), (num_card(5, suit.clubs)), (num_card(8, suit.spades)),
                       (num_card(6, suit.clubs)), (num_card(2, suit.spades))]
    check_straight = player_1_cards.best_poker_hand(community_cards)
#    assert check_straight == [(num_card(9, suit.spades))]

    # Flush
    community_cards = [(num_card(3, suit.hearts)), (num_card(3, suit.hearts)), (num_card(3, suit.hearts)),
                       (num_card(4, suit.hearts)), (num_card(2, suit.spades))]
    check_flush = player_1_cards.best_poker_hand(community_cards)
#    assert check_flush == [(ace_card(suit.hearts)), (num_card(4, suit.hearts)), (num_card(3, suit.hearts)),
#                           (num_card(3, suit.hearts)), (num_card(3, suit.hearts))]

    # Full house
    community_cards = [(ace_card(suit.diamonds)), (num_card(3, suit.clubs)), (num_card(3, suit.spades)),
                       (num_card(3, suit.clubs)), (num_card(2, suit.spades))]
    check_full_house = player_1_cards.best_poker_hand(community_cards)
#    assert check_full_house == [(num_card(3, suit.spades)), (num_card(3, suit.clubs)), (num_card(3, suit.clubs)),
#                                (ace_card(suit.hearts)), (ace_card(suit.diamonds))]

    # Four of a kind
    community_cards = [(num_card(3, suit.diamonds)), (num_card(3, suit.clubs)), (num_card(3, suit.spades)),
                       (num_card(3, suit.hearts)), (num_card(2, suit.spades))]
    check_four_of_a_kind = player_1_cards.best_poker_hand(community_cards)
#    assert check_four_of_a_kind == [(num_card(3, suit.hearts)), (num_card(3, suit.spades)),
#                                    (num_card(3, suit.diamonds)), (num_card(3, suit.clubs))]

    # Straight flush
    community_cards = [(king_card(suit.hearts)), (jack_card(suit.hearts)), (queen_card(suit.hearts)),
                       (num_card(10, suit.hearts)), (num_card(2, suit.spades))]
    check_straight_flush = player_1_cards.best_poker_hand(community_cards)
#    assert check_straight_flush == [(ace_card(suit.hearts))]

    print("high", type(check_high_card))
    print("pair", type(check_one_pair))
    print("three", type(check_three_of_a_kind))
    print("two pairs", type(check_two_pairs))
    print("straight", type(check_straight))
    print("flush", type(check_flush))
    print("full house", type(check_full_house))
    print("four", type(check_four_of_a_kind))
    print("straight flush", type(check_straight_flush))


test_best_poker_hand()
'''


community_cards = [(num_card(6, suit.hearts)), (num_card(2, suit.hearts)), (num_card(3, suit.hearts))]

player_1_cards = cardlib.Hand()
player_1_cards.add_card(num_card(6, suit.spades))
player_1_cards.add_card(num_card(8, suit.hearts))


player_2_cards = cardlib.Hand()
player_2_cards.add_card(num_card(9, suit.spades))
player_2_cards.add_card(num_card(9, suit.hearts))


p1 = player_1_cards.best_poker_hand(community_cards)
#p2 = player_2_cards.best_poker_hand(community_cards)

#print("p1:", p1)
#print("p1 value:", p1.highest_value)
#print(type(p1))
#print("p2:", p2)
#print(p1 > p2)


poker_hand = cardlib.PokerHand()
p3 = poker_hand.check_high_card(player_1_cards)
print("player 3:", p3)
print(type(p3), "\n")

p4 = poker_hand.check_one_pair(player_2_cards)
print("player 4:", p4)
print(type(p4), "\n")

print("Comparison:", p3 < p4)


""" Vet inte om det var detta man skulle kunna få ut, eftersom det inte get något utan att köra de olika funktionerna"""
'''
poker = cardlib.PokerHand(player_1_cards)
print(poker)
print(poker.type)
print(poker.highest_value)
print(type(poker))
'''