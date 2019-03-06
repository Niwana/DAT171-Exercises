from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

qt_app = QApplication(sys.argv)


class AddOneGame(QObject):
    new_total = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.credits = 0

    def add_card(self):
        self.credits += 1
        self.new_total.emit()


class PlayerView(QGroupBox):
    def __init__(self, game_model):
        super().__init__()

        self.button = QPushButton("OK")

        vbox = QVBoxLayout()
        vbox.addWidget(self.button)

        self.setLayout(vbox)

        def press_button():
            game_model.add_card()

        self.button.clicked.connect(press_button)


class GameView(QGroupBox):
    def __init__(self, game_model):
        super().__init__()

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(PlayerView(game_model))

        self.setLayout(vbox)

        self.model = game_model
        self.update_cards()
        game_model.new_total.connect(self.update_cards)

    def update_cards(self):
        self.label.setText(str(self.model.credits))


qt_app = QApplication.instance()
model = AddOneGame()
view = GameView(model)
view.show()
qt_app.exec_()
