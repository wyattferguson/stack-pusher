from dataclasses import dataclass

import pyxel as px


@dataclass
class Pt:
    x: int = 0
    y: int = 0

    def __eq__(self, other: object) -> bool:
        return self.x == other.x and self.y == other.y


# Gameplay Settings
FPS = 15
GAME_SCALE = 2
GRID_SIZE = 8 * GAME_SCALE
BOARD_HEIGHT = 10
BOARD_WIDTH = 12
STARTING_COLS = 5
BLOCK_SCORE = 20
GOAL_SCORE = 1000

# Graphics Settings
ANIMATION_DELAY = 4
SCREEN_WIDTH = (BOARD_WIDTH + 4) * GRID_SIZE
SCREEN_HEIGHT = (BOARD_HEIGHT + 2) * GRID_SIZE
GRID_X_OFFSET = 5 * GRID_SIZE
GRID_Y_OFFSET = 1 * GRID_SIZE
DISPLAY_SCALE = 4
IMAGE_SHEET = 0
TILE_SIZE = 8
NAV_Y_OFFSET = 7

# Colors
COL_NAV = px.COLOR_RED
TRANSPARENCY = 0

# Game States
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAMEOVER = 3

# Sprites
SPRITE_SIZE = 8
SPRITE_OFFSET = 4
CURSOR_SPRITE = Pt(0, 0)
BLOCK_BOMB = Pt(0, 8)
BLOCK_PINK = Pt(16, 0)
BLOCK_YELLOW = Pt(24, 0)
BLOCK_GREEN = Pt(16, 8)
BLOCK_PURPLE = Pt(24, 8)
