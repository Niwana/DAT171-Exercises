import cardlib

#print(type(cardlib.Suit))
cardlib

test = cardlib.NumberedCard(2, cardlib.Suit.clubs)
test2 = cardlib.KingCard(cardlib.Suit.clubs)
#test2 = cardlib.JackCard
print(test)

#print(cardlib.Suit.club < cardlib.Suit.diamond)
#print(cardlib.Suit.club)