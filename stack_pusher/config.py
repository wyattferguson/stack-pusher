from dataclasses import dataclass

import pyxel as px


@dataclass
class Pt:
    """A simple dataclass to make dealing with grid x/y's more readable"""

    x: int = 0
    y: int = 0

    def __eq__(self, other: object) -> bool:
        if not other:
            return False
        return self.x == other.x and self.y == other.y


# Gameplay Settings
FPS = 10
GAME_SCALE = 2
GRID_SIZE = 8 * GAME_SCALE
BOARD_HEIGHT = 9
BOARD_WIDTH = 12
STARTING_COLS = 4
BLOCK_SCORE = 20
GOAL_SCORE = 1000
TIMER_LENGTH = 5

# Graphics Settings
ANIMATION_DELAY = 4
SCREEN_WIDTH = (BOARD_WIDTH - 1) * GRID_SIZE
SCREEN_HEIGHT = (BOARD_HEIGHT + 3) * GRID_SIZE
GRID_X_OFFSET = 0
GRID_Y_OFFSET = 2 * GRID_SIZE
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

# Graphics
SPRITE_SIZE = 8
SPRITE_OFFSET = 4
CURSOR_SPRITE = Pt(0, 0)
BLOCK_BOMB = Pt(0, 8)
BLOCK_PINK = Pt(16, 0)
BLOCK_YELLOW = Pt(24, 0)
BLOCK_GREEN = Pt(16, 8)
BLOCK_PURPLE = Pt(24, 8)
TILEMAP_GAME = 0
TILEMAP_MENU = 1

# Sounds
SND_NEW_LEVEL = 1
SND_PUSH_BLOCKS = 0
SND_THEME = 2
