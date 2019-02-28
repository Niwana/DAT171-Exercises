from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

qt_app = QApplication(sys.argv)


class AddOneGame(QObject):
    new_total = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.cards = ['a']

    def add_card(self):
        self.cards.append('b')
        self.new_total.emit()


class GameView(QGroupBox):
    def __init__(self, game_model):
        super().__init__()

        button = QPushButton("OK")

        self.label = QLabel('')
        self.label.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(button)

        self.setLayout(vbox)

        self.model = game_model
        self.update_cards()
        game_model.new_total.connect(self.update_cards)

        # Controllers
        def press_button():
            game_model.add_card()

        button.clicked.connect(press_button)

    def update_cards(self):
        self.label.setText(str(self.model.cards))


qt_app = QApplication.instance()
model = AddOneGame()
view = GameView(model)
view.show()
qt_app.exec_()
