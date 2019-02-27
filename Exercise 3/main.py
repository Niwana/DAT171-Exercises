import sys
from engine import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

qt_app = QApplication(sys.argv)


class OtherPlayer(QGroupBox):
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
        card1.setPixmap(QPixmap('cards\\Red_Back_2.svg'))
        card1.setAlignment(Qt.AlignCenter)

        card2 = QLabel(self)
        card2.setPixmap(QPixmap('cards\\Red_Back_2.svg'))
        card2.setAlignment(Qt.AlignCenter)

        empty = QLabel(self)

        hbox = QHBoxLayout()
        hbox.addWidget(empty)
        hbox.addWidget(card1)
        hbox.addWidget(card2)
        hbox.addWidget(remaining)

        hbox_player = QHBoxLayout()
        hbox_player.addWidget(player_name)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addLayout(hbox_player)

        self.setLayout(vbox)


class CommunityCards(QGroupBox):
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

        hbox = QHBoxLayout()
        hbox.addWidget(card1)
        hbox.addWidget(card2)
        hbox.addWidget(card3)
        hbox.addWidget(card4)
        hbox.addWidget(card5)

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
        card1.setAlignment(Qt.AlignCenter)

        card2 = QLabel(self)
        card2.setPixmap(QPixmap('cards\\JS.svg'))
        card2.setAlignment(Qt.AlignCenter)



        # Buttons
        call_button = QPushButton('Call')
        call_button.setFixedWidth(100)
        raise_button_field = QLineEdit()
        raise_button_field.setFixedWidth(100)

        raise_button = QPushButton('Raise')
        raise_button.setFixedWidth(100)

        fold_button = QPushButton('Fold')
        fold_button.setFixedWidth(100)
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

        hbox.addLayout(vbox_buttons)
        hbox.addLayout(hbox_cards)
        hbox.addLayout(hbox_remaining)


        hbox_player = QHBoxLayout()
        hbox_player.addWidget(player_name)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_player)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


class Window(QGroupBox):
    def __init__(self):
        super().__init__("main window")
        w = QWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(OtherPlayer())
        vbox.addWidget(CommunityCards())
        vbox.addWidget(ActivePlayer())

        self.setLayout(vbox)
        self.setGeometry(300, 300, 1000, 600)
        self.setWindowTitle("Texas Hold Em'")


win = Window()
win.show()
qt_app.exec_()


"""
def window2():
    app = QApplication(sys.argv)

    w = QWidget()
    top = QLabel(w)
    top.setText('Top')
    top.setAlignment(Qt.AlignCenter)

    callButton = QPushButton('Call')

    middle = QLabel(w)
    middle.setText('Middle')
    middle.setAlignment(Qt.AlignCenter)

    bottom = QLabel(w)
    bottom.setText('Bottom')
    bottom.setAlignment(Qt.AlignCenter)

    vbox = QVBoxLayout()
    vbox.addWidget(top)
    vbox.addWidget(middle)
    vbox.addWidget(bottom)
    #vbox.addStretch()

    hbox = QVBoxLayout(middle)
    #vbox2 = QVBoxLayout()
    vbox.addWidget(callButton)

    #label_mid_p1 = QLabel()
    #label_mid_p1.setAlignment(Qt.AlignCenter)
    #label_mid_p2 = QLabel()
    #label_mid_p2.setAlignment(Qt.AlignCenter)

    # label_mid_p3 = QtWidgets.QLabel(middle)
    # label_mid_p4 = QtWidgets.QLabel(middle)
    # label_mid_p5 = QtWidgets.QLabel(middle)

    #label_mid_p1.setPixmap(QPixmap('kort.png'))
    #label_mid_p2.setPixmap(QPixmap('kort.png'))
    # label_mid_p3.setPixmap(QtGui.QPixmap('kort.png'))
    # label_mid_p4.setPixmap(QtGui.QPixmap('kort.png'))
    # label_mid_p5.setPixmap(QtGui.QPixmap('kort.png'))

    #vbox2.addWidget(label_mid_p1)
    #vbox2.addWidget(label_mid_p2)




    #hbox.addWidget(label_mid_p1)
    #hbox.addWidget(label_mid_p2)

    #shbox.addLayout(vbox2)

    #hbox.addWidget(label_mid_p3)
    #hbox.addWidget(label_mid_p4)
    #hbox.addWidget(label_mid_p5)



    w.setLayout(vbox)
    w.setWindowTitle("Texas Hold Em'")

    w.show()
    sys.exit(app.exec_())
    # sys.exc_info(app.exec_())

window()

    #app = QtWidgets.QApplication(sys.argv)

    w = QtWidgets.QWidget()
    label_player_2 = QtWidgets.QLabel(w)
    label_player_3 = QtWidgets.QLabel(w)

    label_player_2.setText("player 2")
    label_player_1.setText("Player 1")
    label_player_3.setText("Player 3")

    h_box = QtWidgets.QHBoxLayout()
    h_box.addStretch()
    w.setWindowTitle("test")
    w.setGeometry(100,100,400,400)


    h_box = QtWidgets.QHBoxLayout()
    h_box.addWidget(label_player_2)
    h_box.addLayout(h_box)

    v_box2 = QtWidgets.QVBoxLayout()
    v_box2.addWidget(label_player_1)
    v_box2.addLayout(h_box)
    w.setLayout(h_box)

    #w.setBackgroundRole()

    #label1.move(100,20)
    #label2.move(200,40)

    w.setWindowTitle("Texas Hold Em'")


    w.show()
    sys.exit(app.exec_())
    #sys.exc_info(app.exec_())


    label_mid_p1 = QtWidgets.QLabel(w)
    label_mid_p2 = QtWidgets.QLabel(w)
    label_mid_p3 = QtWidgets.QLabel(w)
    label_mid_p4 = QtWidgets.QLabel(w)
    label_mid_p5 = QtWidgets.QLabel(w)

    label_mid_p1.setPixmap(QtGui.QPixmap('pika.jpg'))
    label_mid_p2.setPixmap(QtGui.QPixmap('pika.jpg'))
    label_mid_p3.setPixmap(QtGui.QPixmap('pika.jpg'))
    label_mid_p4.setPixmap(QtGui.QPixmap('pika.jpg'))
    label_mid_p5.setPixmap(QtGui.QPixmap('pika.jpg'))

    h_box.addWidget(label_mid_p1)
    h_box.addWidget(label_mid_p2)
    h_box.addWidget(label_mid_p3)
    h_box.addWidget(label_mid_p4)
    h_box.addWidget(label_mid_p5)

    h_box.addStretch()
"""
"""
card1 = QLabel(self)
        card1.setPixmap(QPixmap('cards\\2C.svg'))
        card1.setAlignment(Qt.AlignLeft)

        card2 = QLabel(self)
        card2.setPixmap(QPixmap('cards\\3C.svg'))
        #card2.setMargin(100)
        card2.setAlignment(Qt.AlignRight)

        vbox = QHBoxLayout()
        vbox.addStretch(1)
        #hbox.addWidget(card1)
        #hbox.addWidget(card2)
        vbox.addWidget(card1)
        vbox.addWidget(card2)

"""

