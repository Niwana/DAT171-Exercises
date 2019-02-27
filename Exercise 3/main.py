import sys
from engine import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

qt_app = QApplication(sys.argv)


class OtherPlayer(QGroupBox):
    """ The inactive player """
    def __init__(self):
        super().__init__("Other player")

        font = QFont()
        font.setPointSize(20)

        remaining = QLabel(self)
        remaining.setText('Remaining money: 500')
        remaining.setAlignment(Qt.AlignCenter)

        player_name = QLabel(self)
        player_name.setText('Player 2')
        player_name.setMargin(20)
        player_name.setFont(font)
        player_name.setAlignment(Qt.AlignCenter)

        card1 = QLabel(self)
        card1_pixmap = QPixmap('cards\\Red_Back_2.svg')
        smaller_card1 = card1_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.FastTransformation)
        card1.setPixmap(smaller_card1)
        card1.setAlignment(Qt.AlignCenter)

        card2 = QLabel(self)
        card2_pixmap = QPixmap('cards\\Red_Back_2.svg')
        smaller_card2 = card2_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.FastTransformation)
        card2.setPixmap(smaller_card2)
        card2.setAlignment(Qt.AlignCenter)

        # TODO: Här används en annnan metod
        card3 = QLabel(self)
        card3_pixmap = QPixmap('cards\\Red_Back_2.svg')
        #smaller_card1 = card1_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.FastTransformation)
        smaller_card3 = QPixmap.scaledToHeight(card3_pixmap, 200)
        card3.setPixmap(smaller_card3)
        card3.setAlignment(Qt.AlignCenter)

        empty = QLabel(self)

        hbox = QHBoxLayout()
        hbox.addWidget(empty)
        hbox.addWidget(card1)
        hbox.addWidget(card2)
        hbox.addWidget(card3)
        hbox.addWidget(remaining)

        hbox_player = QHBoxLayout()
        hbox_player.addWidget(player_name)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox_player)

        self.setLayout(vbox)


class CommunityCards(QGroupBox):
    """ Community cards """
    def __init__(self):
        super().__init__("Community cards")
        card1 = QLabel(self)
        card1.setPixmap(QPixmap('cards\\2C.svg'))
        card1.setAlignment(Qt.AlignCenter)

        card2 = QLabel(self)
        card2.setPixmap(QPixmap('cards\\3C.svg'))
        card2.setAlignment(Qt.AlignCenter)

        card3 = QLabel(self)
        card3.setPixmap(QPixmap('cards\\4C.svg'))
        card3.setAlignment(Qt.AlignCenter)

        card4 = QLabel(self)
        card4.setPixmap(QPixmap('cards\\5C.svg'))
        card4.setAlignment(Qt.AlignCenter)

        card5 = QLabel(self)
        card5.setPixmap(QPixmap('cards\\6C.svg'))
        card5.setAlignment(Qt.AlignCenter)
        QPixmap()

        hbox = QHBoxLayout()
        #hbox.addStretch()
        hbox.addWidget(card1)
        hbox.addWidget(card2)
        hbox.addWidget(card3)
        hbox.addWidget(card4)
        hbox.addWidget(card5)
        #hbox.addStretch()


        vbox = QVBoxLayout()

        font = QFont()
        font.setPointSize(20)

        pot = QLabel(self)
        pot.setText('Pot 1000')
        pot.setMargin(20)
        pot.setFont(font)
        pot.setAlignment(Qt.AlignCenter)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(pot)


        vbox.addLayout(hbox)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)


class ActivePlayer(QGroupBox):
    """ Active player """
    def __init__(self):
        super().__init__("Active player")
        font = QFont()
        font.setPointSize(20)

        remaining = QLabel(self)
        remaining.setText('Remaining money: 250')
        remaining.setAlignment(Qt.AlignCenter)

        player_name = QLabel(self)
        player_name.setText('Player 1')
        player_name.setMargin(20)
        player_name.setFont(font)
        player_name.setAlignment(Qt.AlignCenter)

        card1 = QLabel(self)
        card1.setPixmap(QPixmap('cards\\KC.svg'))
        card1.setAlignment(Qt.AlignLeft)

        card2 = QLabel(self)
        card2.setPixmap(QPixmap('cards\\JS.svg'))
        card2.setAlignment(Qt.AlignRight)


        # Buttons
        call_button = QPushButton('Call')
        #call_button.setFixedWidth(100)
        raise_button_field = QLineEdit()
        #raise_button_field.setFixedWidth(100)

        raise_button = QPushButton('Raise')
        #raise_button.setFixedWidth(100)

        fold_button = QPushButton('Fold')
        #fold_button.setFixedWidth(100)
        hbox_raise = QHBoxLayout()

        hbox_raise.addWidget(raise_button_field)
        hbox_raise.addWidget(raise_button)

        vbox_buttons = QVBoxLayout()
        vbox_buttons.addWidget(call_button)
        vbox_buttons.addLayout(hbox_raise)
        vbox_buttons.addWidget(fold_button)

        hbox = QHBoxLayout()

        hbox_cards = QHBoxLayout()
        hbox_cards.addWidget(card1)
        hbox_cards.addWidget(card2)

        hbox_remaining = QHBoxLayout()
        hbox_remaining.addWidget(remaining)

        hbox.addStretch()
        hbox.addLayout(vbox_buttons)
        hbox.addStretch()
        hbox.addLayout(hbox_cards)
        hbox.addStretch()
        hbox.addLayout(hbox_remaining)
        hbox.addStretch()

        hbox_player = QHBoxLayout()
        hbox_player.addWidget(player_name)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_player)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


class Window(QGroupBox):
    """ main window """
    def __init__(self):
        super().__init__("main window")
        # w = QWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(OtherPlayer())
        vbox.addWidget(CommunityCards())
        vbox.addWidget(ActivePlayer())

        self.setLayout(vbox)
        #self.setGeometry(300, 300, 1000, 600)
        self.setWindowTitle("Texas Hold Em'")


win = Window()
win.show()
qt_app.exec_()
