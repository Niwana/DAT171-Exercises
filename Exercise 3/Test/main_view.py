import sys
import model
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# TODO: lägg till bet, check, call?

# Låt vinsten vara en funktion med potten som input. Kom ihåg att lägga till signals.
# g.player[0].win_money(pot)
# Använd ej följande:
# g.player[0].money += pot

qt_app = QApplication(sys.argv)


class CardItem(QGraphicsSvgItem):
    """ A simple overloaded QGraphicsSvgItem that also stores the card position """

    def __init__(self, renderer, position):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = position


class CardView(QGraphicsView):
    def read_cards():
        """
        :return:
        """
        all_cards = dict()
        for suit in 'HDSC':
            for value in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
                file = value + suit
                all_cards[file] = QSvgRenderer('cards/' + file + '.svg')

        # print(type(all_cards))
        # print(all_cards)
        return all_cards

    back_card = QSvgRenderer('cards/Red_Back_2.svg')
    all_cards = read_cards()

    def __init__(self, player, card_spacing=250, padding=2):
        self.scene = QGraphicsScene()
        super().__init__(self.scene)

        self.card_spacing = card_spacing
        self.padding = padding

        self.player = player

        self.change_cards()

    def change_cards(self):
        self.scene.clear()
        for i, card_ref in enumerate(self.player.cards_to_view):
            renderer = self.all_cards[card_ref]
            card = CardItem(renderer, i)
            self.scene.addItem(card)

        self.update_view()

    def update_view(self):
        for card in self.scene.items():
            card_height = card.boundingRect().bottom()
            card_width = card.boundingRect().right()

            scale = (self.height() - 2 * self.padding) / card_height
            scale_width = (self.width() - 2 * self.padding) / card_width / len(self.scene.items())

            # card.setPos((self.width() - (self.card_spacing * len(self.scene.items()) / 2)) + card.position * self.card_spacing * scale, 0)
            card.setPos(card.position * self.card_spacing * scale, 0)

            # card.setPos(card.position * self.card_spacing * scale, 0)
            card.setScale(scale)

        self.scene.setSceneRect(-self.padding, -self.padding, self.viewport().width(), self.viewport().height())

    def resizeEvent(self, painter):
        self.update_view()
        super().resizeEvent(painter)


class CommunityCards(QGroupBox):
    """ Community cards """

    def __init__(self):
        super().__init__("Community cards")

        font = QFont()
        font.setPointSize(20)

        pot = QLabel(self)
        pot.setText('Pot 1000')
        pot.setMargin(20)
        pot.setFont(font)
        pot.setAlignment(Qt.AlignCenter)

        hbox = QHBoxLayout()
        hbox.addWidget(community_card_view)

        hbox_pot = QHBoxLayout()
        hbox_pot.addWidget(pot)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox_pot)

        self.setLayout(vbox)
        self.setStyleSheet("background-image: url(cards/table.png)")


class InputBoxLayout(QGroupBox):
    """ Input box with buttons for call, fold and raise. """

    def __init__(self, texas_model):
        super().__init__("Input box")
        self.model = texas_model

        # Buttons
        call_button = QPushButton('Call')
        self.raise_button_field = QLineEdit(self)
        raise_button = QPushButton('Raise')
        fold_button = QPushButton('Fold')

        call_button.clicked.connect(model.Buttons.print_click)

        hbox_raise = QHBoxLayout()
        hbox_raise.addWidget(self.raise_button_field)
        hbox_raise.addWidget(raise_button)

        vbox_buttons = QVBoxLayout()
        vbox_buttons.addWidget(call_button)
        vbox_buttons.addLayout(hbox_raise)
        vbox_buttons.addWidget(fold_button)

        self.setLayout(vbox_buttons)

        # game_model.new_card.connect(self.update_cards)

        # Controllers
        def press_fold_button():
            model.add_card()

        fold_button.clicked.connect(press_fold_button)

        def press_raise_button():
            input = self.raise_button_field.text()
            if input.isdigit():
                texas_model.bet(int(input))
                #PlayerView.update_labels()  # Crashar när man kör denna funktion
            else:
                print('The input format is incorrect. Please enter a value')

        raise_button.clicked.connect(press_raise_button)
'''
    def update_cards(self):
        print('print update cards')
        # CardView.update_view()
'''


class PlayerView(QGroupBox):
    """ Active player """

    def __init__(self, texas_model, player):
        super().__init__("Active player")

        font = QFont()
        font.setPointSize(20)

        self.player_credits = QLabel()
        self.player_credits.setAlignment(Qt.AlignCenter)

        self.player_name = QLabel()
        self.player_name.setText(player_0.name)
        self.player_name.setMargin(20)
        self.player_name.setFont(font)
        self.player_name.setAlignment(Qt.AlignCenter)
        self.player_name.backgroundRole()

        hbox_cards = QHBoxLayout()
        hbox_cards.addWidget(player_card_view[player])
        bla = player_card_view[player]
        print(bla)

        hbox_remaining = QHBoxLayout()
        hbox_remaining.addWidget(self.player_credits)

        hbox = QHBoxLayout()
        hbox.addLayout(hbox_cards, 2)
        hbox.addLayout(hbox_remaining, 1)

        hbox_name = QHBoxLayout()
        hbox_name.addWidget(self.player_name)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_name)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setStyleSheet("background-image: url(cards/table.png)")
        self.model = texas_model
        self.update_labels()
        texas_model.new_credits.connect(self.update_labels)

    def update_labels(self):
        print('RUN')
        self.player_credits.setText('Remaining money:' + str(self.model.credits[0]))


class GameView(QGroupBox):
    """ main window """

    def __init__(self):
        super().__init__("main window")

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        hbox.addWidget(InputBoxLayout(model.TexasHoldEm()), 1)
        for i in range(len(player_card_view)):
            hbox.addWidget(PlayerView(model.TexasHoldEm(), i), 10)
            print(players[i])


        # vbox.addWidget(PlayerView(model.TexasHoldEm()))
        vbox.addWidget(CommunityCards())
        vbox.addLayout(hbox)

        # self.setGeometry(300, 300, 1000, 600)
        self.setWindowTitle("Texas Hold'em")
        self.setLayout(vbox)

players = []
player_0 = model.Player('B1')
player_1 = model.Player('B2')
players.append(player_0)
players.append(player_1)

player_card_view = []
player_card_view.append(CardView(player_0))
player_card_view.append(CardView(player_1))
print((player_0.name))


community_cards = model.CommunityCards()
community_card_view = CardView(community_cards)
view = GameView()
view.show()
qt_app.exec_()
