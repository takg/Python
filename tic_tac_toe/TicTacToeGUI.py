from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QGridLayout, QWidget, QMessageBox
import TicTacToeBoard


class TicTacToeGUI(QWidget):
    def __init__(self, board, parent=None):
        super(TicTacToeGUI, self).__init__(parent)

        self.board = board
        self.grid_layout = QGridLayout(self)
        self.buttons = []
        self.setWindowIcon(QIcon("images/tic_tac_toe.png"))
        self.setFixedHeight(250)
        self.setFixedWidth(250)

        for i in range(9):
            button = QPushButton("")
            button.setFixedWidth(75)
            button.setFixedHeight(75)
            button.clicked.connect(self.on_clicked)
            self.buttons.append(button)

        self.setup_home_screen()
        self.refresh_board()

    def setup_home_screen(self):
        self.setWindowTitle('Tic Tac Toe')
        # display the board
        for i in range(9):
            self.grid_layout.addWidget(self.buttons[i], i / 3, i % 3)

        self.setLayout(self.grid_layout)

    def on_clicked(self):
        button = self.sender()
        index = 0

        for i in range(9):
            if button == self.buttons[i]:
                index = i
                break

        if self.board.check_game_over():
            r_value = QMessageBox.warning(self,
                                "Game Over",
                                "Game Over! Do you want to play a new game",
                                QMessageBox.Yes,
                                QMessageBox.No)
            self.new_game(r_value)
        elif not self.board.take(index):
            QMessageBox.warning(self,
                                "Warning",
                                "This position is taken! Please choose an open position.")
        else:
            self.refresh_board()
            if self.board.check_win():
                self.game_won()
            elif not self.board.check_more_slots_available():
                self.game_drawn()

    def game_won(self):
        r_value = QMessageBox.information(self,
                                "Game Over",
                                "You win! Do you want to play a new game?",
                                QMessageBox.Yes,
                                QMessageBox.No)

        self.new_game(r_value)

    def new_game(self, value):
        if value == QMessageBox.Yes:
            self.board.save_game_and_reset()
            self.refresh_board()

    def game_drawn(self):
        r_value = QMessageBox.information(self,
                                          "Game Over", "Game drawn. Do you want to play a new game?",
                                          QMessageBox.Yes,
                                          QMessageBox.No)
        self.new_game(r_value)

    def refresh_board(self):
        for i in range(9):
            if self.board.check_position_empty(i):
                self.buttons[i].setIcon(QIcon())
            elif self.board.check_position_taken_by_first_player(i):
                self.buttons[i].setIcon(QIcon("images/tick.png"))
                self.buttons[i].setIconSize(QSize(70, 70))
            else:
                self.buttons[i].setIcon(QIcon("images/cross.jfif"))
                self.buttons[i].setIconSize(QSize(70, 70))
