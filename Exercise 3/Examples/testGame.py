from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

qt_app = QApplication(sys.argv)

class AddOneGame(QObject):
    new_total = pyqtSignal()
    winner = pyqtSignal(str, )

    def __init__(self):
        super().__init__()
        self.players = ['Micke', 'Thomas']
        self.total = [0, 0]

    def player_click(self, ind):
        self.total[ind] += 1
        self.new_total.emit()
        self.check_winner()

    def reset(self):
        self.total = [0, 0]
        self.new_total.emit()

    def check_winner(self):
        if self.total[0] >= 10:
            self.winner.emit(self.players[0] + " won!")
            self.reset()
        elif self.total[1] >= 10:
            self.winner.emit(self.players[1] + " won!")
            self.reset()


class GameView(QWidget):
    def __init__(self, game_model):
        super().__init__()
        buttons = [QPushButton(game_model.players[0]), QPushButton(game_model.players[1])]
        self.labels = [QLabel(), QLabel()]
        vbox = QVBoxLayout()
        vbox.addWidget(buttons[0])
        vbox.addWidget(self.labels[0])
        vbox.addWidget(buttons[1])
        vbox.addWidget(self.labels[1])

        reset_button = QPushButton('Reset')
        reset_button.clicked.connect(game_model.reset)

        vbox.addWidget(reset_button)

        self.setLayout(vbox)
        self.show()

        # Model!
        self.game = game_model
        self.update_labels()
        game_model.new_total.connect(self.update_labels)
        game_model.winner.connect(self.alert_winner)

        # Controller!
        def player0_click():
            game_model.player_click(0)

        buttons[0].clicked.connect(player0_click)

        def player1_click():
            game_model.player_click(1)

        buttons[1].clicked.connect(player1_click)

    def update_labels(self):
        for i in range(2): self.labels[i].setText(str(self.game.total[i]))

    def alert_winner(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.exec()


qt_app = QApplication.instance()
game = AddOneGame()
view = GameView(game)
qt_app.exec_()