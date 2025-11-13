from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from functools import partial


class Board(QWidget):
    def __init__(self):
        super().__init__()

        self.player = "X"
        self.board_values = [["" for _ in range(3)] for _ in range(3)]
        self.button_grid = [[None for _ in range(3)] for _ in range(3)]

        # Main layout
        main_layout = QVBoxLayout()

        # Status label
        self.status_label = QLabel("Player X's turn")
        self.status_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

        # Grid layout for buttons
        grid_layout = QGridLayout()
        grid_layout.setSpacing(5)

        for i in range(3):
            for j in range(3):
                button = QPushButton("")
                button.setFixedSize(100, 100)
                button.setStyleSheet(self.button_style())
                font = button.font()
                font.setPointSize(24)
                button.setFont(font)

                button.clicked.connect(partial(self.button_clicked, i, j))
                grid_layout.addWidget(button, i, j)
                self.button_grid[i][j] = button

        main_layout.addLayout(grid_layout)
        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #1e1e1e;")

    def button_clicked(self, y, x):
        if self.board_values[y][x] != "" or self.is_win():
            return  # ignore if filled or game already won

        # Update board
        self.board_values[y][x] = self.player
        self.button_grid[y][x].setText(self.player)

        # Check for win
        if self.is_win():
            self.status_label.setText(f"Player {self.player} wins!")
            self.highlight_win()
        elif self.is_draw():
            self.status_label.setText("It's a draw!")
        else:
            # Switch player
            self.player = "O" if self.player == "X" else "X"
            self.status_label.setText(f"Player {self.player}'s turn")

    def is_win(self) -> bool:
        b = self.board_values

        # Check rows
        for row in b:
            if row[0] != "" and row[0] == row[1] == row[2]:
                return True

        # Check columns
        for col in range(3):
            if b[0][col] != "" and b[0][col] == b[1][col] == b[2][col]:
                return True

        # Check diagonals
        if b[0][0] != "" and b[0][0] == b[1][1] == b[2][2]:
            return True
        if b[0][2] != "" and b[0][2] == b[1][1] == b[2][0]:
            return True

        return False

    def is_draw(self) -> bool:
        return all(cell != "" for row in self.board_values for cell in row) and not self.is_win()

    def button_style(self, color="#ffffff"):
        return f"""
            QPushButton {{
                background-color: #2e2e2e;
                color: {color};
                border: 2px solid #555;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: #3e3e3e;
            }}
            QPushButton:pressed {{
                background-color: #5e5e5e;
            }}
        """

    def highlight_win(self):
        """Optional: visually highlight winning line"""
        b = self.board_values
        for i in range(3):
            if b[i][0] != "" and b[i][0] == b[i][1] == b[i][2]:
                for j in range(3):
                    self.button_grid[i][j].setStyleSheet(self.button_style("#00ff00"))
        for j in range(3):
            if b[0][j] != "" and b[0][j] == b[1][j] == b[2][j]:
                for i in range(3):
                    self.button_grid[i][j].setStyleSheet(self.button_style("#00ff00"))
        if b[0][0] != "" and b[0][0] == b[1][1] == b[2][2]:
            for k in range(3):
                self.button_grid[k][k].setStyleSheet(self.button_style("#00ff00"))
        if b[0][2] != "" and b[0][2] == b[1][1] == b[2][0]:
            for k in range(3):
                self.button_grid[k][2-k].setStyleSheet(self.button_style("#00ff00"))
