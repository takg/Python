import TicTacToeBoard
import TicTacToeGUI
from PyQt5.QtWidgets import QApplication
import sys

game = TicTacToeBoard.TicTacToeBoard()
game.check_win()

# args = parse_args()
app = QApplication(sys.argv)
gui = TicTacToeGUI.TicTacToeGUI(game)
gui.show()
app.exec_()