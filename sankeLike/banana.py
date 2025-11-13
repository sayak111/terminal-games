import curses
import random
import time

# Game config
FPS = 20
PLAYER_EMOJI = "🟦"
APPLE_EMOJI = "🍎"
ENEMY_EMOJI = "🍌"
SPEED = 1  # lower is faster
COLORS = [curses.COLOR_BLACK, curses.COLOR_BLUE, curses.COLOR_GREEN,
          curses.COLOR_YELLOW, curses.COLOR_MAGENTA, curses.COLOR_RED, curses.COLOR_CYAN]

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.start_color()
    
    # Initialize color pairs
    for i, color in enumerate(COLORS):
        curses.init_pair(i + 1, color, curses.COLOR_BLACK)

    height, width = stdscr.getmaxyx()
    player_x, player_y = width // 2, height // 2

    apples = []
    enemies = []

    score = 0
    level = 100
    color_index = 1
    loop_on = True

    keys_down = set()

    frame_delay = 1000 // FPS  # milliseconds per frame

    def spawn_apple():
        if random.randint(1, 100) == 1:
            apples.append([random.randint(1, height - 2), random.randint(1, width - 2)])

    def spawn_enemy():
        if random.randint(1, level) == 1:
            enemies.append([0, random.randint(1, width - 2)])

    def draw():
        stdscr.clear()
        stdscr.bkgd(' ', curses.color_pair(color_index))
        # draw apples
        for ay, ax in apples:
            stdscr.addstr(ay, ax, APPLE_EMOJI)
        # draw enemies
        for ey, ex in enemies:
            stdscr.addstr(ey, ex, ENEMY_EMOJI)
        # draw player
        stdscr.addstr(player_y, player_x, PLAYER_EMOJI)
        # score
        stdscr.addstr(0, 2, f"Score: {score}  Level: {level}")
        stdscr.refresh()

    while True:
        start_time = time.time() * 1000  # milliseconds

        # Input handling
        try:
            while True:  # read all keys pressed this frame
                key = stdscr.getch()
                if key == -1:
                    break
                keys_down.add(key)
        except:
            pass

        if loop_on:
            # Player movement
            if curses.KEY_UP in keys_down: player_y = max(1, player_y - 1)
            if curses.KEY_DOWN in keys_down: player_y = min(height - 2, player_y + 1)
            if curses.KEY_LEFT in keys_down: player_x = max(1, player_x - 1)
            if curses.KEY_RIGHT in keys_down: player_x = min(width - 2, player_x + 1)
            if ord('q') in keys_down or ord('Q') in keys_down:
                break

            keys_down.clear()

            # Spawn apples and enemies
            spawn_apple()
            spawn_enemy()

            # Move enemies
            for e in enemies:
                e[0] += 1

            # Collision detection: apples
            new_apples = []
            for a in apples:
                if [player_y, player_x] == a:
                    score += 1
                    if score % 10 == 0 and level > 10:
                        level -= 1
                        color_index = min(color_index + 1, len(COLORS))
                else:
                    new_apples.append(a)
            apples = new_apples

            # Collision detection: enemies
            for e in enemies:
                if [player_y, player_x] == e:
                    stdscr.addstr(height // 2, width // 2 - 5, "💀 GAME OVER 💀")
                    stdscr.refresh()
                    time.sleep(2)
                    return

            # Remove enemies off-screen
            enemies = [e for e in enemies if e[0] < height - 1]

            # Draw everything
            draw()

        # Pause toggle
        key = stdscr.getch()
        if key in [27, 10]:  # Esc or Enter
            loop_on = not loop_on
            if not loop_on:
                stdscr.addstr(height // 2, width // 2 - 3, "⏸ PAUSE ⏸")
                stdscr.refresh()
            time.sleep(0.1)

        # Maintain fixed FPS
        elapsed = time.time() * 1000 - start_time
        curses.napms(max(0, frame_delay - int(elapsed)))

curses.wrapper(main)
