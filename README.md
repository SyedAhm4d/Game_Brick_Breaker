# Brick Breaker Game

A classic Brick Breaker (Breakout-style) game implemented in Python using Turtle graphics. Break colorful bricks with a bouncing ball while controlling a paddle to prevent the ball from falling.

## Features
- Paddle controlled with arrow keys
- Ball physics with realistic collision detection
- 4 rows of colorful bricks (green, orange, red, crimson)
- Lives system with heart-shaped indicators
- Sound effects for brick breaking and game events
- Animated game start and end screens
- Increasing game speed as you progress

## Requirements
- Python 3.8+
- pygame (for sound effects)
- turtle (built-in Python module)

```bash
pip install pygame
```

## Installation

1. Clone or download the repository
2. Install pygame for sound effects:
```bash
pip install pygame
```
3. Ensure you have the required font and sound files:
   - `ARCADE_N.TTF` (font file)
   - `brick_break.mp3` (brick breaking sound)
   - `start.mp3` (game start sound)
   - `end.mp3` (game over sound)

## Run the game

```bash
python main.py
```

## Controls
- **Left Arrow**: Move paddle left
- **Right Arrow**: Move paddle right
- **Space**: Start the game

## Gameplay
- **Objective**: Destroy all bricks on the screen without losing all lives
- **Lives**: Start with 5 lives (shown as red hearts). Lose a life when the ball falls below the paddle
- **Brick Colors**: 4 rows of different colored bricks - green, orange, red, and crimson
- **Speed**: Game speed increases as you break bricks in higher rows
- **Win Condition**: Clear all bricks to win the game

## Project Structure

```
Portfolio_6_Brick_Breaker/
├── main.py              # Main game file with all game logic
├── ARCADE_N.TTF         # Arcade font for game text
├── brick_break.mp3      # Sound effect for breaking bricks
├── start.mp3           # Game start sound
├── end.mp3             # Game over sound
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Configuration
Game settings can be modified in `main.py`:
- `STEP`: Paddle movement speed (default: 150)
- `STEP_BALL_X/Y`: Ball movement speed (default: 5)
- Boundary constants for screen limits
- Brick colors and layout in `create_wall()` method
- Number of lives (hearts) in the `hearts_left` array

## Technical Details
- Built using Python's Turtle graphics module
- Custom heart shape registered for life indicators
- Collision detection using distance calculations
- Threading used for sound effects to prevent game lag
- Dynamic brick sizing to fit screen width

## Known Issues
- Game window opens in fullscreen mode
- Sound effects require pygame installation
- Game speed increases significantly in later stages

## Credits
- Inspired by classic Breakout/Arkanoid games
- Built using Python Turtle graphics and pygame for audio
- Custom arcade font for retro gaming feel

## Contact
Maintained by SyedAhm4d — https://github.com/SyedAhm4d
