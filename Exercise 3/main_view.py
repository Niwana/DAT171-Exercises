import sys
import model
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


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

    def __init__(self, cards, card_spacing=250, padding=0):
        self.scene = QGraphicsScene()
        super().__init__(self.scene)

        self.card_spacing = card_spacing
        self.padding = padding

        self.cards = cards
        self.change_cards()

        # self.cards.new_player_cards.connect(self.change_cards)
        # self.cards.new_community_cards.connect(self.change_cards)

    def change_cards(self):
        self.scene.clear()
        for index, card_ref in enumerate(self.cards.cards_to_view):
            renderer = self.all_cards[card_ref]
            card = CardItem(renderer, index)

            shadow = QGraphicsDropShadowEffect(card)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))  # Semi-transparent black!
            card.setGraphicsEffect(shadow)

            self.scene.addItem(card)

        self.update_view()

    def update_view(self):
        for card in self.scene.items():
            orig_card_height = card.boundingRect().bottom()
            orig_card_width = card.boundingRect().width()

            scale = (self.viewport().height() - 2 * self.padding) / orig_card_height
            scale_width = (self.viewport().width() - (len(self.scene.items()) + 1) * self.padding) / (orig_card_width * len(self.scene.items()))

            # scale_width = ((self.viewport().width() - 2 * len(self.scene.items()) * self.padding) / (orig_card_width * len(self.scene.items())))

            req_width = self.card_spacing * scale * len(self.scene.items())

            # TODO: identifera vad som är fel. Stämmer villkoren och skalningen? Korten hoppar i storlek vid övergången
            if req_width > self.viewport().width():
                scale = scale_width * 0.9

            margin_height = (self.viewport().height() - (orig_card_height * scale)) / 2
            margin_width = (self.viewport().width() - (len(self.scene.items()) -1) * self.card_spacing * scale - (orig_card_width * scale))/2

            card.setPos(margin_width + card.position * self.card_spacing * scale, margin_height)
            card.setScale(scale)

        self.scene.setSceneRect(-self.padding, -self.padding, self.viewport().width(), self.viewport().height())

    def resizeEvent(self, painter):
        self.update_view()
        super().resizeEvent(painter)


class CommunityCards(QGroupBox):
    """ Community cards """

    def __init__(self, texas_model):
        super().__init__("Community cards")
        self.texas_model = texas_model

        font = QFont()
        font.setPointSize(18)

        self.pot = QLabel(self)
        self.pot.setText('Pot Value')
        self.pot.setMargin(18)
        self.pot.setFont(font)
        self.pot.setAlignment(Qt.AlignCenter)

        community_card_view = CardView(texas_model.community_cards)

        hbox = QHBoxLayout()
        hbox.addWidget(community_card_view)

        hbox_pot = QHBoxLayout()
        hbox_pot.addWidget(self.pot)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox_pot)

        self.setLayout(vbox)
        self.setStyleSheet("background-image: url(cards/table.png)")

        texas_model.new_pot.connect(self.update_label)
        self.update_label()

    def update_label(self):
        self.pot.setText("Pot:" + str(self.texas_model.pot))


class InputBoxLayout(QGroupBox):
    """ Input box with buttons for call, fold and raise. """

    def __init__(self, texas_model):
        super().__init__("Input box")

        # Buttons
        self.call_button = QPushButton('Call')
        self.raise_button_field = QLineEdit(self)
        self.raise_button = QPushButton('Raise')
        self.fold_button = QPushButton('Fold')

        hbox_raise = QHBoxLayout()
        hbox_raise.addWidget(self.raise_button_field)
        hbox_raise.addWidget(self.raise_button)

        vbox_buttons = QVBoxLayout()
        vbox_buttons.addWidget(self.call_button)
        vbox_buttons.addLayout(hbox_raise)
        vbox_buttons.addWidget(self.fold_button)

        self.setLayout(vbox_buttons)

        # Logic
        self.model = texas_model
        self.call_button.clicked.connect(self.model.call)
        self.fold_button.clicked.connect(self.model.fold)

        def bet():
            bet_amount = self.raise_button_field.text()
            if bet_amount.isdigit():
                self.model.bet(int(bet_amount))

        self.raise_button.clicked.connect(bet)


class PlayerView(QGroupBox):
    """ Active player """

    def __init__(self, texas_model, player):
        super().__init__("Player view")
        self.model = texas_model
        self.player = player
        font = QFont()
        font.setPointSize(18)

        self.player_credits = QLabel()
        self.player_credits.setAlignment(Qt.AlignCenter)

        self.player_name = QLabel()
        self.player_name.setText(player.name)
        self.player_name.setMargin(20)
        self.player_name.setFont(font)
        self.player_name.setAlignment(Qt.AlignCenter)
        self.player_name.backgroundRole()

        player_card_view = CardView(player)

        hbox_cards = QHBoxLayout()
        hbox_cards.addWidget(player_card_view)

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

        texas_model.new_credits.connect(self.update_labels)
        self.update_labels()

    def update_labels(self):
        self.player_credits.setText("Credits:" + str(self.player.credits))


class GameView(QGroupBox):
    """ main window """

    def __init__(self, texas_model, players):
        super().__init__("main window")
        self.model = texas_model

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        hbox.addWidget(InputBoxLayout(texas_model), 1)

        for cv_index, player in enumerate(players):
            hbox.addWidget(PlayerView(texas_model, player), 10)

        vbox.addWidget(CommunityCards(texas_model))
        vbox.addLayout(hbox)

        # self.setGeometry(300, 300, 1000, 600)
        self.setWindowTitle("Texas Hold'em")
        self.setLayout(vbox)

        texas_model.game_message.connect(self.alert_user)

    def alert_user(self, text):
        box = QMessageBox()
        box.setText(text)
        box.exec_()




