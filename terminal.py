#!/usr/bin/env python3
"""
Terminal Tic-Tac-Toe using curses.
 - Arrow keys to move cursor
 - Enter/Space to place mark
 - r to restart
 - q to quit
Smooth rendering with minimal flicker, colors, and win highlight.
"""

import curses
from curses import wrapper


class CursesTicTacToe:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.reset()

    def reset(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.player = "X"
        self.cursor_y = 0
        self.cursor_x = 0
        self.winner = None
        self.win_cells = []  # list of (y,x) tuples that are winning line

    def start(self):
        curses.curs_set(0)  # hide real cursor
        self.stdscr.nodelay(False)  # blocking input
        self.stdscr.keypad(True)  # arrow keys, etc
        if curses.has_colors():
            curses.start_color()
            # define some color pairs: (pair_number, fg, bg)
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # normal
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # X
            curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)   # O
            curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)  # cursor bg
            curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)  # winning highlight

        while True:
            self.render()
            key = self.stdscr.getch()

            if key in (ord("q"), ord("Q")):
                break
            elif key in (ord("r"), ord("R")):
                self.reset()
            elif key in (curses.KEY_UP, ord("k")):
                self.cursor_y = (self.cursor_y - 1) % 3
            elif key in (curses.KEY_DOWN, ord("j")):
                self.cursor_y = (self.cursor_y + 1) % 3
            elif key in (curses.KEY_LEFT, ord("h")):
                self.cursor_x = (self.cursor_x - 1) % 3
            elif key in (curses.KEY_RIGHT, ord("l")):
                self.cursor_x = (self.cursor_x + 1) % 3
            elif key in (curses.KEY_ENTER, 10, 13, ord(" ")):
                self.try_move(self.cursor_y, self.cursor_x)

    def try_move(self, y, x):
        if self.winner:
            return  # game over
        if self.board[y][x] != "":
            return  # already taken
        self.board[y][x] = self.player
        if self.check_win():
            self.winner = self.player
        elif self.check_draw():
            self.winner = "Draw"
        else:
            self.player = "O" if self.player == "X" else "X"

    def check_win(self):
        b = self.board
        # rows
        for i in range(3):
            if b[i][0] != "" and b[i][0] == b[i][1] == b[i][2]:
                self.win_cells = [(i, 0), (i, 1), (i, 2)]
                return True
        # cols
        for j in range(3):
            if b[0][j] != "" and b[0][j] == b[1][j] == b[2][j]:
                self.win_cells = [(0, j), (1, j), (2, j)]
                return True
        # diag
        if b[0][0] != "" and b[0][0] == b[1][1] == b[2][2]:
            self.win_cells = [(0, 0), (1, 1), (2, 2)]
            return True
        if b[0][2] != "" and b[0][2] == b[1][1] == b[2][0]:
            self.win_cells = [(0, 2), (1, 1), (2, 0)]
            return True
        self.win_cells = []
        return False

    def check_draw(self):
        return all(cell != "" for row in self.board for cell in row)

    def render(self):
        self.stdscr.erase()
        h, w = self.stdscr.getmaxyx()

        # Title / help area
        title = "Terminal Tic-Tac-Toe"
        help_text = "Arrows/hjkl: move • Enter/Space: place • r: restart • q: quit"
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(1, (w - len(title)) // 2, title)
        self.stdscr.addstr(2, (w - len(help_text)) // 2, help_text)

        # Determine top-left of board to center it
        cell_w = 5  # width of one cell text area
        cell_h = 3  # height of one cell text area
        board_w = cell_w * 3 + 2  # plus vertical lines
        board_h = cell_h * 3 + 2  # plus horizontal lines
        start_y = max(4, (h - board_h) // 2)
        start_x = max(2, (w - board_w) // 2)

        # Draw grid with box-drawing characters
        # We'll draw cell areas and put mark centered in each cell
        for i in range(3):
            for j in range(3):
                top = start_y + i * (cell_h)
                left = start_x + j * (cell_w)
                # draw cell border (simple)
                for dx in range(cell_w):
                    # top border
                    self.stdscr.addch(top - 1, left + dx, curses.ACS_HLINE)
                    # bottom border
                    self.stdscr.addch(top + cell_h - 1, left + dx, curses.ACS_HLINE)
                for dy in range(cell_h):
                    # left border
                    self.stdscr.addch(top + dy - 1, left - 1, curses.ACS_VLINE)
                    # right border
                    self.stdscr.addch(top + dy - 1, left + cell_w - 1, curses.ACS_VLINE)

        # put intersections (corners)
        # top-left corner
        self.stdscr.addch(start_y - 1, start_x - 1, curses.ACS_ULCORNER)
        self.stdscr.addch(start_y - 1, start_x + board_w - 2, curses.ACS_URCORNER)
        self.stdscr.addch(start_y + board_h - 2, start_x - 1, curses.ACS_LLCORNER)
        self.stdscr.addch(start_y + board_h - 2, start_x + board_w - 2, curses.ACS_LRCORNER)
        # internal intersections: draw vertical and horizontal separators
        # vertical separators
        for i in range(3):
            for sep in (1, 2):
                y = start_y + i * cell_h - 1
                x = start_x + sep * cell_w - 1
                self.stdscr.addch(y, x, curses.ACS_VLINE)
        # horizontal separators
        for j in range(3):
            for sep in (1, 2):
                y = start_y + sep * cell_h - 1
                x = start_x + j * cell_w - 1
                self.stdscr.addch(y, x, curses.ACS_HLINE)

        # Render each cell content
        for i in range(3):
            for j in range(3):
                top = start_y + i * (cell_h) - 1
                left = start_x + j * (cell_w) - 1
                # position to put the mark centered
                mark_y = top + cell_h // 2
                mark_x = left + cell_w // 2
                ch = self.board[i][j] or " "
                attr = curses.color_pair(1)
                if ch == "X":
                    attr = curses.color_pair(2) | curses.A_BOLD
                elif ch == "O":
                    attr = curses.color_pair(3) | curses.A_BOLD

                # highlight winning cells
                if (i, j) in self.win_cells:
                    attr = curses.color_pair(5) | curses.A_BOLD

                # highlight cursor background when that cell is selected and game not over
                if (i, j) == (self.cursor_y, self.cursor_x) and not self.winner:
                    # invert or use special bg
                    # We'll draw a small background rectangle for the cell
                    for ry in range(cell_h - 1):
                        for rx in range(cell_w - 1):
                            try:
                                self.stdscr.addch(top + 1 + ry, left + 1 + rx, " ", curses.color_pair(4))
                            except curses.error:
                                pass
                    # place the mark char over it
                    try:
                        self.stdscr.addstr(mark_y, mark_x, ch, curses.color_pair(4) | curses.A_BOLD)
                    except curses.error:
                        pass
                else:
                    try:
                        self.stdscr.addstr(mark_y, mark_x, ch, attr)
                    except curses.error:
                        pass

        # Status line
        status = ""
        if self.winner is None:
            status = f"Player {self.player}'s turn"
        elif self.winner == "Draw":
            status = "It's a draw! (r to restart)"
        else:
            status = f"Player {self.winner} wins! (r to restart)"

        self.stdscr.addstr(start_y + board_h, max(0, (w - len(status)) // 2), status, curses.color_pair(1) | curses.A_BOLD)

        self.stdscr.refresh()


def main(stdscr):
    game = CursesTicTacToe(stdscr)
    game.start()


if __name__ == "__main__":
    wrapper(main)
