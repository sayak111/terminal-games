import curses
import random
import time

# Define Tetris shapes with color index
SHAPES = {
    'I': ([[1,1,1,1]], 1),
    'O': ([[1,1],
           [1,1]], 2),
    'T': ([[0,1,0],
           [1,1,1]], 3),
    'S': ([[0,1,1],
           [1,1,0]], 4),
    'Z': ([[1,1,0],
           [0,1,1]], 5),
    'J': ([[1,0,0],
           [1,1,1]], 6),
    'L': ([[0,0,1],
           [1,1,1]], 7)
}

class Tetris:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        curses.start_color()
        # Initialize 7 colors
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)

        self.height, self.width = 20, 10
        self.board = [[0]*self.width for _ in range(self.height)]
        self.score = 0
        self.delay = 0.5
        self.next_shape, self.next_color = self.new_shape()
        self.shape, self.color = self.new_shape()
        self.shape_x = self.width // 2 - len(self.shape[0])//2
        self.shape_y = 0
        self.game_over = False

    def new_shape(self):
        s, color = random.choice(list(SHAPES.values()))
        return [row[:] for row in s], color

    def rotate(self):
        rotated = [list(row) for row in zip(*self.shape[::-1])]
        old_x, old_y = self.shape_x, self.shape_y
        if self.collision(rotated):
            return
        self.shape = rotated

    def collision(self, shape=None, dx=0, dy=0):
        if shape is None:
            shape = self.shape
        for y,row in enumerate(shape):
            for x,val in enumerate(row):
                if val:
                    nx = self.shape_x + x + dx
                    ny = self.shape_y + y + dy
                    if nx < 0 or nx >= self.width or ny >= self.height:
                        return True
                    if ny >= 0 and self.board[ny][nx]:
                        return True
        return False

    def place_shape(self):
        for y,row in enumerate(self.shape):
            for x,val in enumerate(row):
                if val:
                    self.board[self.shape_y+y][self.shape_x+x] = self.color
        self.clear_lines()
        self.shape, self.color = self.next_shape, self.next_color
        self.next_shape, self.next_color = self.new_shape()
        self.shape_x = self.width // 2 - len(self.shape[0])//2
        self.shape_y = 0
        if self.collision():
            self.game_over = True

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell==0 for cell in row)]
        cleared = self.height - len(new_board)
        self.score += cleared * 100
        for _ in range(cleared):
            new_board.insert(0,[0]*self.width)
        self.board = new_board

    def drop(self):
        if not self.collision(dy=1):
            self.shape_y += 1
        else:
            self.place_shape()

    def move(self, dx):
        if not self.collision(dx=dx):
            self.shape_x += dx

    def draw(self):
        self.stdscr.clear()
        y_offset = 1  # Shift everything down by 1 row

        # Draw border
        for y in range(self.height):
            self.stdscr.addstr(y + y_offset, 0, '│')
            self.stdscr.addstr(y + y_offset, self.width*2 + 1, '│')
        self.stdscr.addstr(y_offset - 1, 0, '┌' + '─'*(self.width*2) + '┐')
        self.stdscr.addstr(self.height + y_offset, 0, '└' + '─'*(self.width*2) + '┘')

        # Draw board
        for y,row in enumerate(self.board):
            for x,val in enumerate(row):
                if val:
                    self.stdscr.addstr(y + y_offset, x*2 + 1, '██', curses.color_pair(val))

        # Draw current shape
        for y,row in enumerate(self.shape):
            for x,val in enumerate(row):
                if val and self.shape_y+y >= 0:
                    self.stdscr.addstr(self.shape_y + y + y_offset, (self.shape_x + x)*2 + 1, '██', curses.color_pair(self.color))

        # Draw next shape preview
        self.stdscr.addstr(y_offset + 1, self.width*2 + 5, "Next:")
        for y,row in enumerate(self.next_shape):
            for x,val in enumerate(row):
                if val:
                    self.stdscr.addstr(y_offset + 2 + y, self.width*2 + 5 + x*2, '██', curses.color_pair(self.next_color))

        # Draw score
        self.stdscr.addstr(y_offset + 8, self.width*2 + 5, f"Score: {self.score}")
        self.stdscr.refresh()

    
    
    def run(self):
        last_time = time.time()
        self.stdscr.nodelay(True)
        while not self.game_over:
            now = time.time()
            if now - last_time > self.delay:
                self.drop()
                last_time = now

            try:
                key = self.stdscr.getkey()
            except:
                key = None

            if key in ['a','KEY_LEFT']:
                self.move(-1)
            elif key in ['d','KEY_RIGHT']:
                self.move(1)
            elif key in ['s','KEY_DOWN']:
                self.drop()
            elif key in ['w','KEY_UP']:
                self.rotate()
            elif key in [' ']:
                while not self.collision(dy=1):
                    self.shape_y +=1
                self.place_shape()

            self.draw()
            time.sleep(0.01)

        self.stdscr.addstr(self.height//2, self.width, "GAME OVER!")
        self.stdscr.refresh()
        time.sleep(2)

def main(stdscr):
    game = Tetris(stdscr)
    game.run()

curses.wrapper(main)
