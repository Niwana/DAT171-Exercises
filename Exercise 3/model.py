from cardlib import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


# TODO: konstruera en välkomstruta där man anger spelarnas namn, startpengar och (big blind?) blinds värde?
#  När rutan stängs (ok-knapp?) startar spelet.

#  TODO: Läs på om nedanstående. Vi har inga separata potter. Så det går till vid 1v1?
#   "Att syna (engelska call) innebär att man går med på att betala så att ens pott innehåller samma belopp som den som
#   öppnade eller höjde. Om spelaren A till höger B till exempel öppnade med 2 kr så måste B lägga 2 kr i sin egen pott
#   för att syna. Observera än en gång att allt satsande sker i separata potter. Den stora potten i mitten är bara
#   uppsamlingsplats för de marker som satsats i de enskilda satsningsrundorna." ~ wikipedia

# TODO: Lägg till small blind och big blind. Spelarna turas om med varje. Blind dubbleras för varje game (?). Small
#  blind är 50% av big blind. Big blind är 1/100 av spelarnas startsumma, så $10 för $1000.
#  Lämpligt att köra på $50 k som start?
#  "The normal case is that each player starts the tournament with 100 big blinds. If the small blind is 5 and the big
#  blind is 10 chips, then each player would start with 1000 chips (10*100=1000). If you double the blinds from now on,
#  from 5/10 to 10/20 to 20/40, then the blinds are sizable, resulting in a swift, but not chaotic game."

# TODO: visa i text på skärmen vad senaste bet/raise var?

# TODO: om ena spelaren har bettat måste nästa call:a och sen checka.

# TODO: implementera vem som är dealer.

# TODO: Spelarna _MÅSTE_ call:a summorna från respektive blind vid rundands start (?) Ante däremot ökar linjärt (?)

# TODO: highlighta de vinnande korten?

# TODO: Efter att en spelare har raisat måste den andra spelaren ta ett beslut. Det läggs inga fler kort på bordet
#  innan det är gjort.


class TexasHoldEm(QObject):
    new_credits = pyqtSignal()
    new_pot = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.players = ['Name 1', 'Name 2']
        self.credits = [50000, 50000]
        self.pot = 0
        self.active_player = 0
        self.round_counter = 0
        self.blind = self.credits[0]/100
        self.previous_bet = 0

        print("Blind:", self.blind)

    def call(self):
        """ Måste satsa lika mycket som den spelare som satsat mest."""
        if self.credit(self.active_player) >= self.previous_bet and not self.previous_bet == 0:
            self.pot += self.previous_bet
            self.credits[self.active_player] -= self.previous_bet
            print("Call")
        else:
            print('Otillåten handling eller fel i call-funktionen')

    def check(self):
        """ "Att checka (eller passa) betyder att man väljer att inte satsa något nu, men ändå vill
        stanna kvar i given tillsvidare. Man kan checka så länge ingen annan öppnat."""
        self.active_player = 1 - self.active_player

    def allin(self):
        # TODO: när någon gör all in måste den andra spelaren folda eller också göra all in
        self.pot += self.credit(self.active_player)
        self.credit[self.active_player] = 0

    def flop(self):
        # TODO: Dela ut tre community cards på en gång. Efter det ett i taget tills fem stycken ligger på bordet.
        #   "In the third and fourth betting rounds, the stakes double." (???????)
        pass

    def bet(self, amount):
        # TODO: Besluta om vi ska köra no-limit texas holdem, limit eller pot-limit.
        # TODO: Visa blinds värde på skärmen.
        # TODO: Byt från print() till dialogrutor vid varningar. box = QMessageBox(), box.setText(), box.exec__()
        # TODO: Hur hantera all-in?

        if self.previous_bet == 0 and amount < self.blind:
            print("Bet must be equal to or higher than the blind!")
        elif amount + self.blind < self.previous_bet:
            print("Bet must be equal to or higher than the previous raise")
        elif amount + self.blind <= self.credits[self.active_player]:
            self.pot += amount + self.blind
            self.credits[self.active_player] -= amount
            self.previous_bet = amount + self.blind
            # self.new_pot.emit()
            self.new_credits.emit()
            # Swap the active player
            self.active_player = 1 - self.active_player

            print("Credits:", self.credits)
            print("Pot", self.pot)
            print("Previous bet", self.previous_bet)
        else:
            print("Not enough money!")

    def fold(self):
        """ Då vinner automatiskt motståndaren? """
        # TODO: Avsluta spelet på något vis? Starta om?
        self.credits[1 - self.active_player] += self.pot    # Ge motståndaren hela potten.
        self.pot = 0

    def showdown(self):
        # TODO: Modifiera best_poker_hand så att även typ av hand returneras, inte bara det högsta kortet?
        # TODO: Implementera en metod som vänder/visar alla kort

        """
        best_hand_player_0 = PokerHand.best_poker_hand(community_cards + player_0_hand) # hur göra detta?
        best_hand_player_1 = PokerHand.best_poker_hand(community_cards + player_0_hand)

        if best_hand_player_0 > best_hand_player_1:
            print("Player 0 won!")
            self.credits[0] += self.pot

        if best_hand_player_0 < best_hand_player_1:
            print("Player 1 won!")
            self.credits[1] += self.pot

        if best_hand_player_0 == best_hand_player_1
            # fördela potten jämnt om det är identiska vinnande händer
            print("Oavgjort")
            self.credits[0] += (self.pot / 2)
            self.credits[1] += (self.pot / 2)
        else:
            print(" Fel vid jämförelsen?")
        """


class Player:
    def __init__(self):
        self.cards = ['QS', '7C']
        self.marked_cards = [False] * len(self.cards)
        # self.credits = 1000
        # self.folded = False
        self.cb = None


class CommunityCards(QObject):
    new_card = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.cards = ['2S', '3S', '4S']

    def add_card(self):
        self.cards.append('2H')
        self.new_card.emit()


class Buttons:
    def __init__(self):
        super().__init__()

    def print_click(self):
        print('klick')
        # TexasHoldEm.call()

    def print_fold(self):
        print('fold')