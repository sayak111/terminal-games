import curses
import random
import time

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    height, width = 20, 40
    win = curses.newwin(height, width, 1, 1)
    win.keypad(True)
    win.timeout(150)

    # initial snake and food
    snake = [[height//2, width//4 + i] for i in range(3)][::-1]
    direction = curses.KEY_RIGHT
    food = [random.randint(1, height - 2), random.randint(1, width - 2)]
    score = 0

    while True:
        win.clear()
        win.border()

        # Draw food
        win.addstr(food[0], food[1], "🍎", curses.color_pair(2))

        # Draw snake
        for y, x in snake:
            win.addstr(y, x, "█", curses.color_pair(1))

        # Score
        win.addstr(0, 2, f" Score: {score} ", curses.color_pair(3))

        # Input
        key = win.getch()
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            # Prevent 180° turns
            if (key == curses.KEY_UP and direction != curses.KEY_DOWN) or \
               (key == curses.KEY_DOWN and direction != curses.KEY_UP) or \
               (key == curses.KEY_LEFT and direction != curses.KEY_RIGHT) or \
               (key == curses.KEY_RIGHT and direction != curses.KEY_LEFT):
                direction = key
        elif key in [ord('q'), ord('Q')]:
            break

        # Next head position
        head_y, head_x = snake[0]
        if direction == curses.KEY_UP:
            head_y -= 1
        elif direction == curses.KEY_DOWN:
            head_y += 1
        elif direction == curses.KEY_LEFT:
            head_x -= 1
        elif direction == curses.KEY_RIGHT:
            head_x += 1

        new_head = [head_y, head_x]

        # Collision check
        if (new_head in snake or
            head_y == 0 or head_y == height - 1 or
            head_x == 0 or head_x == width - 1):
            win.clear()
            msg = f"💀 Game Over! Score: {score}"
            win.addstr(height // 2, (width - len(msg)) // 2, msg, curses.color_pair(2))
            win.refresh()
            time.sleep(2)
            break

        snake.insert(0, new_head)

        # Eat food
        if new_head == food:
            score += 1
            food = [random.randint(1, height - 2), random.randint(1, width - 2)]
            # Increase speed slightly
            win.timeout(max(50, 150 - score * 5))
        else:
            snake.pop()

if __name__ == "__main__":
    curses.wrapper(main)
