from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from grid import Board


class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setGeometry(100, 100, 350, 400)

        layout = QVBoxLayout()

        board = Board()          # Create the Board instance
        layout.addWidget(board)  # Add it to main layout

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication([])
    window = TicTacToe()
    window.show()
    app.exec()
