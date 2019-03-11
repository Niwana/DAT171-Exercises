from model import TexasHoldEm, DeckModel, Player
from main_view import GameView, qt_app


# Starting credits and player names.
starting_credits = 5000
player_0_name = 'B1'
player_1_name = 'B2'

# Create the card deck
deck_model = DeckModel()

# Create the players
players = [Player(player_0_name, deck_model, starting_credits),
           Player(player_1_name, deck_model, starting_credits)]

# Create the game model
texas_model = TexasHoldEm(players, deck_model, starting_credits)
view = GameView(texas_model, players)
view.show()
qt_app.exec_()
