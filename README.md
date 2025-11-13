# Terminal Games Collection

A collection of fun terminal-based games built with Python and `curses`. All games use colorful emojis and smooth input.

---

## Games Included

### 1. Maze Escape
- Navigate a randomly generated maze
- Reach the exit `E` to win
- Player: `@`
- Features a timer and score tracking

### 2. Snake
- Classic snake game
- Eat food to grow
- Avoid walls and yourself
- Player: `█`
- Food: `*`
- Score tracking

### 3. Emoji Collect Game
- Collect apples 🍎, avoid falling enemies 🍌
- Player: `🟦`
- Colorful backgrounds that change with levels
- Pause with `Esc` or `Enter`

*(Future games can be added here…)*

---

## Controls (Common)

- **Arrow keys** → Move
- **Q** → Quit
- **Esc / Enter** → Pause / Resume (for games that support it)

---

## Requirements

- Python 3.8+
- `curses` (Unix/Linux/macOS)
- Windows users: `windows-curses` package

Install dependencies (Windows only):

```bash
pip install windows-curses
How to Run

Each game is in its own Python file. For example:

python maze.py
python snake.py
python banana.py
