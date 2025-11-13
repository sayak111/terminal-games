import curses
import random
import time


def generate_maze(width, height):
    """Random maze generator using recursive backtracking."""
    maze = [["█" for _ in range(width)] for _ in range(height)]

    def carve(x, y):
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and maze[ny][nx] == "█":
                maze[ny][nx] = " "
                maze[y + dy // 2][x + dx // 2] = " "
                carve(nx, ny)

    # Start carving
    maze[1][1] = " "
    carve(1, 1)

    # Mark exit
    maze[height - 2][width - 2] = "E"
    return maze


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    width, height = 31, 21
    maze = generate_maze(width, height)

    player_y, player_x = 1, 1
    start_time = time.time()

    while True:
        stdscr.clear()

        # Draw maze
        for y, row in enumerate(maze):
            stdscr.addstr(y, 0, "".join(row))

        # Draw player
        stdscr.addstr(player_y, player_x, "@", curses.color_pair(1))

        # Timer
        elapsed = int(time.time() - start_time)
        stdscr.addstr(height, 0, f"Time: {elapsed}s  |  Press Q to quit", curses.color_pair(2))

        stdscr.refresh()

        key = stdscr.getch()
        new_y, new_x = player_y, player_x

        if key == curses.KEY_UP:
            new_y -= 1
        elif key == curses.KEY_DOWN:
            new_y += 1
        elif key == curses.KEY_LEFT:
            new_x -= 1
        elif key == curses.KEY_RIGHT:
            new_x += 1
        elif key in [ord('q'), ord('Q')]:
            break

        # Check for collision
        if maze[new_y][new_x] == " " or maze[new_y][new_x] == "E":
            player_y, player_x = new_y, new_x

        # Check for win
        if maze[player_y][player_x] == "E":
            stdscr.clear()
            total_time = int(time.time() - start_time)
            msg = f"🎉 You escaped in {total_time} seconds! Press any key to exit."
            stdscr.addstr(height // 2, (width - len(msg)) // 2, msg, curses.color_pair(1))
            stdscr.refresh()
            stdscr.nodelay(False)
            stdscr.getch()
            break


if __name__ == "__main__":
    curses.wrapper(main)
