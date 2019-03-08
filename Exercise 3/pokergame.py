import model
from main_view import *

# TODO: Ska detta köras mer än 1 gång?

# Create the players
card_model = model.DeckModel()
players = [model.Player('B1', card_model), model.Player('B2', card_model)]
#players[0].active = True

# Create the game model
texas_model = model.TexasHoldEm(players, card_model, starting_credits=50000)
view = GameView(texas_model, players)
print(len(card_model.deck))
view.show()
qt_app.exec_()