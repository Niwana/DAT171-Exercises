import cardlib



def create_deck():
    deck = []
    suit = cardlib.Suit
    # Create the numbered cards
    for i in range(2, 11):
        card = cardlib.NumberedCard(i, suit.clubs)
        deck.append((card.value, card.suit))
    for i in range(2, 11):
        card = cardlib.NumberedCard(i, suit.diamonds)
        deck.append((card.value, card.suit))
    for i in range(2, 11):
        card = cardlib.NumberedCard(i, suit.spades)
        deck.append((card.value, card.suit))
    for i in range(2, 11):
        card = cardlib.NumberedCard(i, suit.hearts)
        deck.append((card.value, card.suit))

    return deck

#deck = create_deck()
deck = []

card_1 = cardlib.NumberedCard(2, cardlib.Suit.spades)
card_2 = cardlib.NumberedCard(2, cardlib.Suit.hearts)

jack_1 = cardlib.JackCard(cardlib.Suit.spades)

deck.append((card_1.get_value(), (card_1.get_suit())))
deck.append((card_2.get_value(), (card_2.get_suit())))

print("card 1:", card_1)
print("card 2:", card_2)
print("Deck:", deck)



