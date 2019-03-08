from cardlib import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


# TODO: konstruera en välkomstruta där man anger spelarnas namn, startpengar och (big blind?) blinds värde?
#  När rutan stängs (ok-knapp?) startar spelet.

# TODO: visa i text på skärmen vad senaste bet/raise var?

# TODO: om ena spelaren har bettat måste nästa call:a och sen checka.

# TODO: implementera vem som är dealer.

# TODO: Efter att en spelare har raisat måste den andra spelaren ta ett beslut. Det läggs inga fler kort på bordet
#  innan det är gjort.

# TODO: Visa blinds värde på skärmen.

# TODO: Gör så att spelaren förlorar om credits är mindre än blind vid start av rundan

# TODO: Man kan ej folda när alla community cards är lagda. Då återstår check, bet och all in.

# deck = StandardDeck()
# deck.create_deck()
# deck.shuffle()


class DeckModel:
    def __init__(self):
        super().__init__()
        self.deck = StandardDeck()
        self.deck.create_deck()
        self.deck.shuffle()


class TexasHoldEm(QObject):
    new_credits = pyqtSignal()
    new_pot = pyqtSignal()
    game_message = pyqtSignal((str,))

    new_cards = pyqtSignal()

    def __init__(self, players, deck_model, starting_credits):
        super().__init__()
        self.players = players
        self.active_player = 0
        players[0].active = True
        self.deck = deck_model

        self.pot = 0
        self.big_blind = starting_credits // 100
        self.small_blind = self.big_blind // 2
        self.initiate_blind(self.small_blind + self.big_blind)
        self.previous_bet = self.small_blind
        self.actions = 0

        # Create the community cards view
        self.community_cards = CommunityCards(self.deck)

    def initiate_blind(self, blinds):
        for player in self.players:
            if player.active:
                player.credits -= self.small_blind
            else:
                player.credits -= self.big_blind
        self.pot += blinds
        self.new_pot.emit()

    def call(self):
        """ Måste satsa lika mycket som den spelare som satsat mest."""
        if self.players[self.active_player].credits >= self.previous_bet and not self.previous_bet == 0:
            self.pot += self.previous_bet
            # print(self.previous_bet)
            self.players[self.active_player].credits -= self.previous_bet
            self.actions += 1
            self.new_pot.emit()
            self.new_credits.emit()

            self.active_player = (self.active_player + 1) % len(self.players)
            if self.actions == len(self.players):
                pass
                # self.community_cards.flop()
                # self.new_cards.emit()
            if self.actions == 3 * len(self.players):
                self.showdown()

        else:
            text = 'Action not allowed'
            self.game_message.emit(text)

    def flop(self):
        self.card_model.deck.draw_card(0)
        convert_card_names(self.cards)

    def turn(self):  # Add the 4th card
        pass

    def river(self):  # Add the 5th card
        pass

    def bet(self, amount):
        # TODO: applicera villkoren nedan
        self.pot += amount
        self.new_pot.emit()

        self.players[self.active_player].credits -= amount
        self.new_credits.emit()

        self.previous_bet = amount

        self.active_player = (self.active_player + 1) % len(self.players)

        '''
        if self.previous_bet == 0 and amount < self.blind:
            print("Bet must be equal to or higher than the blind!")
        elif amount + self.blind < self.previous_bet:
            print("Bet must be equal to or higher than the previous raise.\n"
            "You tried raising {} + {} (blind) for a total bet of {}.".format(amount, self.blind, amount+self.blind)) # TODO: Printar 1000 när man raisar med 500

        elif amount + self.blind <= self.players[self.player.active].credits:
            self.pot += amount + self.blind
            self.players[self.active_player].credits -= amount
            self.previous_bet = amount + self.blind

            # Swap the active player
            #self.player.active = 1 - self.active_player

        else:
            print("Not enough money!")
        '''

    def fold(self):
        """ Då vinner automatiskt motståndaren? """
        self.players[1-self.active_player].credits += self.pot  # Ge motståndaren hela potten.
        self.pot = 0
        self.new_pot.emit()
        self.new_credits.emit()

    def showdown(self):
        p0 = self.players[0].hand.best_poker_hand(self.community_cards.cards)
        p1 = self.players[1].hand.best_poker_hand(self.community_cards.cards)

        if p0.type > p1.type:
            text = "Player {} won!".format(self.players[0].name)
            self.game_message.emit(text)
            self.players[0].credits += self.pot

        if p0.type < p1.type:
            text = "Player {} won!".format(self.players[1].name)
            self.game_message.emit(text)
            self.players[1].credits += self.pot

        if p0.type == p1.type:
            if p0.highest_values > p1.highest_values:
                text = "Player {} won!".format(self.players[0].name)
                self.game_message.emit(text)
                self.players[0].credits += self.pot

            elif p0.highest_values < p1.highest_values:
                text = "Player {} won!".format(self.players[1].name)
                self.game_message.emit(text)
                self.players[1].credits += self.pot

            elif p0.highest_values == p1.highest_values:
                text = "Draw!"
                self.game_message.emit(text)
                for player in self.players:
                    player.credits += (self.pot // len(self.players))
            else:
                self.game_message.emit("Incorrect comparison of poker hands")

        self.new_credits.emit()
        self.pot = 0
        self.new_pot.emit()

    def restart(self):
        pass




def convert_card_names(hand):
    cards = []
    for i, color in enumerate('CDSH'):
        for card in hand:
            if card.get_suit() == i and card.get_value() < 11:
                cards.append('{}{}'.format(card.get_value(), color))
            if card.get_suit() == i and card.get_value() == 11:
                cards.append('{}{}'.format('J', color))
            if card.get_suit() == i and card.get_value() == 12:
                cards.append('{}{}'.format('Q', color))
            if card.get_suit() == i and card.get_value() == 13:
                cards.append('{}{}'.format('K', color))
            if card.get_suit() == i and card.get_value() == 14:
                cards.append('{}{}'.format('A', color))
    return cards


class Player(QObject):
    # new_community_cards = pyqtSignal()

    def __init__(self, player_name, deck_model, starting_credits=50000):
        super().__init__()
        self.cards = deck_model.deck.draw_card(2)  # TODO: Fixa
        self.hand = Hand()
        for card in self.cards:
            self.hand.add_card(card)
        self.cards_to_view = convert_card_names(self.cards)
        self.name = player_name

        self.credits = starting_credits
        self.active = False

        # self.new_community_cards.emit()


class CommunityCards(QObject):
    # new_community_cards = pyqtSignal()

    def __init__(self, deck_model):
        super().__init__()
        self.deck = deck_model.deck
        self.cards = deck_model.deck.draw_card(5)
        self.cards_to_view = convert_card_names(self.cards)

    def flop(self):
        self.cards = self.deck.deck.draw_card(3)
        self.cards_to_view = convert_card_names(self.cards)

        # self.new_community_cards.emit()

        # self.deck.draw_card(3)
        # self.cards_to_view = convert_card_names(self.cards)

'''
class Buttons:
    def __init__(self):
        super().__init__()

    def print_click(self):
        print('Call')
        texas_model = TexasHoldEm.call()

    def print_fold(self):
        print('Fold')
'''

# TODO: Lägg till nedan om tid finns till
'''
    def check(self):
        """ "Att checka (eller passa) betyder att man väljer att inte satsa något nu, men ändå vill
        stanna kvar i given tillsvidare. Man kan checka så länge ingen annan öppnat."""
        self.active_player = 1 - self.active_player


    def all_in(self):
        """ När någon gör all in måste den andra spelaren folda eller också göra all in """
        self.pot += self.credit(self.active_player)
        self.credit[self.active_player] = 0
'''
