import model
from main_view import *

# TODO: Ska detta köras mer än 1 gång?
deck_model = model.DeckModel()

# Create the players
players = [model.Player('B1', deck_model), model.Player('B2', deck_model)]

# Create the game model
texas_model = model.TexasHoldEm(players, deck_model, starting_credits=50000)
view = GameView(texas_model, players)
view.show()
qt_app.exec_()