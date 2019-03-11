import sys
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsDropShadowEffect, QGroupBox, QLabel,\
    QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit, QPlainTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont


qt_app = QApplication(sys.argv)


class CardItem(QGraphicsSvgItem):
    """ A simple overloaded QGraphicsSvgItem that also stores the card position """

    def __init__(self, renderer, position):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = position


class CardView(QGraphicsView):

    def read_cards():
        """ A function for importing the .svg image files depicting the playing cards.
        """
        all_cards = dict()
        for suit in 'HDSC':
            for value in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
                file = value + suit
                all_cards[file] = QSvgRenderer('cards/' + file + '.svg')

        return all_cards

    back_card = QSvgRenderer('cards/Red_Back_2.svg')
    all_cards = read_cards()

    def __init__(self, card_models, card_spacing=250, padding=0):
        self.scene = QGraphicsScene()
        super().__init__(self.scene)

        self.card_spacing = card_spacing
        self.padding = padding

        self.cards = card_models

        # Update cards when a players data has changed
        card_models.update_cards_data.connect(self.change_cards)

        self.change_cards()

    def change_cards(self):
        """ A function for changing the displayed cards. """
        self.scene.clear()
        for index, card_ref in enumerate(self.cards.cards_to_view):
            if self.cards.flipped_cards[index]:
                renderer = self.back_card
            else:
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
        """ A function for updating the view and resizing the cards accordingly. """
        for card in self.scene.items():
            orig_card_height = card.boundingRect().bottom()
            orig_card_width = card.boundingRect().width()

            scale = (self.viewport().height() - 2 * self.padding) / orig_card_height
            scale_width = (self.viewport().width() - (len(self.scene.items()) + 1) * self.padding) / \
                          (orig_card_width * len(self.scene.items()))

            req_width = self.card_spacing * scale * len(self.scene.items())

            if req_width > self.viewport().width():
                scale = scale_width * 0.9

            margin_height = (self.viewport().height() - (orig_card_height * scale)) / 2
            margin_width = (self.viewport().width() - (len(self.scene.items()) - 1) *
                            self.card_spacing * scale - (orig_card_width * scale))/2

            card.setPos(margin_width + card.position * self.card_spacing * scale, margin_height)
            card.setScale(scale)

        self.scene.setSceneRect(-self.padding, -self.padding, self.viewport().width(), self.viewport().height())

    def resizeEvent(self, painter):
        self.update_view()
        super().resizeEvent(painter)


class CommunityCards(QGroupBox):
    """ A class representing the view of the community cards. """

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
    """ A class representing an input box with buttons for call, fold and raise. """

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
        self.setFixedWidth(180)

        # Logic
        self.model = texas_model
        self.call_button.clicked.connect(self.model.call)
        self.fold_button.clicked.connect(self.model.fold)

        def bet():
            bet_amount = self.raise_button_field.text()
            if bet_amount.isdigit():
                self.model.bet(int(bet_amount))
                self.raise_button_field.clear()

        self.raise_button.clicked.connect(bet)


class OutputBox(QGroupBox):
    """ A class representing an output screen in which the game model can print the player moves. """
    def __init__(self, texas_model):
        super().__init__()
        self.field = QPlainTextEdit(self)

        output_text = "Starting game...\n{} post the big blind [${}]\n{} post the small blind [${}]".format(
            texas_model.players[(texas_model.active_player + 1) % len(texas_model.players)].name, texas_model.big_blind,
            texas_model.players[texas_model.active_player].name, texas_model.small_blind)
        self.field.insertPlainText(output_text)
        self.field.setReadOnly(True)
        self.field.setFixedWidth(180)
        self.setFixedWidth(180)

        texas_model.new_output.connect(self.add_text)

    def add_text(self, text: str):
        self.field.appendPlainText("------\n{}".format(text))


class PlayerView(QGroupBox):
    """ A class representing the player view. """

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
    """ A class representing the main window. It contains functions for displaying pop-up
        messages alerting the user. """

    def __init__(self, texas_model, players):
        super().__init__("main window")
        self.model = texas_model

        vbox = QVBoxLayout()
        hbox_lower = QHBoxLayout()
        hbox_upper = QHBoxLayout()

        hbox_lower.addWidget(InputBoxLayout(texas_model))

        for cv_index, player in enumerate(players):
            hbox_lower.addWidget(PlayerView(texas_model, player))

        hbox_upper.addWidget(OutputBox(texas_model))
        hbox_upper.addWidget(CommunityCards(texas_model))

        vbox.addLayout(hbox_upper)
        vbox.addLayout(hbox_lower)

        self.setWindowTitle("Texas Hold'em")
        self.setLayout(vbox)

        texas_model.game_message.connect(self.alert_user)
        texas_model.game_message_warning.connect(self.alert_user_warning)

    def alert_user(self, text):
        box = QMessageBox()
        box.setText(text)
        box.setWindowTitle("Texas Hold'em")

        play_again_button = QPushButton("Play again")
        exit_button = QPushButton("Quit game")

        box.addButton(play_again_button, box.YesRole)
        box.addButton(exit_button, box.NoRole)

        play_again_button.clicked.connect(self.model.next_round)
        exit_button.clicked.connect(self.exit_application)

        box.exec_()

    def alert_user_warning(self, text):
        box = QMessageBox()
        box.setText(text)
        box.setWindowTitle("Texas Hold'em")
        box.exec_()

    @staticmethod
    def exit_application():
        sys.exit(qt_app.exec_())
