# Color Realm

**Color Realm** is a colorful puzzle-platformer game built with Python and Pygame. Your mission is to bring color back to the world by solving two types of puzzles: color-matching and platform-jumping!

---

## How to Play

### Controls

- **Move Left/Right:** Arrow keys (`←` and `→`)
- **Jump:** Space bar (`Space`)
- **Change Player Color:**  
  - `A` = Previous color  
  - `D` = Next color

### Game Flow

1. **Instructions Screen:**  
   - Read the instructions.
   - Press any key to start.

2. **Color Puzzle:**  
   - A colored circle ("Target Color") appears at the top.
   - Use `A` and `D` to cycle your player’s color.
   - When your player matches the target color, the puzzle is solved.

3. **Time Puzzle (Platform Puzzle):**  
   - Platforms move horizontally.
   - Use arrow keys to move and `Space` to jump.
   - Jump from platform to platform, reaching the top of the screen.

4. **Repeat:**  
   - The game alternates between color and platform puzzles.
   - Complete all puzzles to win!

5. **Restart:**  
   - After winning, press `R` to restart.

---

## Features

- **Color-matching puzzles**
- **Moving platform puzzles**
- **Sound effects** (if `correct.wav`, `incorrect.wav`, and `complete.wav` are present)
- **Beautiful world image** after winning

---

## Requirements

- Python 3.x
- [Pygame](https://www.pygame.org/) (`pip install pygame`)

---

## Setup

1. **Install Pygame:**
   ```
   pip install pygame
   ```

2. **Place your assets:**
   - Place your world image as `world.jpg` in the same folder as the script.
   - (Optional) Add sound files: `correct.wav`, `incorrect.wav`, `complete.wav`.

3. **Run the game:**
   ```
   python trygame3.py
   ```

---

## What You Have in Your Folder

- **trygame3.py**  
  The main Python game file containing all the game logic, puzzles, and rendering code.

- **world.jpg**  
  The image that appears when you win the game, showing a beautiful, colorful world.

- **(Optional) Sound files:**  
  - `correct.wav` — Played when you solve a color puzzle.
  - `incorrect.wav` — Played when you select the wrong color.
  - `complete.wav` — Played when you complete a platform puzzle.

- **Any additional images or sound files** you want to use for customization.

---

## Customization

- **Add more world images:**  
  Replace or add more images and update the code to randomize them if desired.
- **Adjust difficulty:**  
  Change platform numbers, gaps, or jump height in the code for easier or harder gameplay.

---

## Credits

- Game by [Your Name]
- Built with Python and Pygame

---

Enjoy bringing color back to the world!

## I have used "GitHub Copilot" (an AI programming assistant) :

~ Debug and improve the Pygame code
~ Add features like random world images, user-friendly platform puzzles, and color overlays
~ Refactor and explain code sections

----------------------------------------------------------------------------------------------------
