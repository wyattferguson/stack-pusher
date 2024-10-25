import pyxel as px
from config import (
    ANIMATION_DELAY,
    GAME_SCALE,
    GRID_SIZE,
    GRID_X_OFFSET,
    GRID_Y_OFFSET,
    IMAGE_SHEET,
    SPRITE_OFFSET,
    SPRITE_SIZE,
    TILE_SIZE,
    TRANSPARENCY,
    Pt,
)


class Tile:
    """Generic Tile for all animated and moving board sprites"""

    def __init__(
        self, x: int = 0, y: int = 0, sprite: Pt = Pt(0, 0), animated: bool = False
    ):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.frame = 0
        self.animated = animated

    def update(self):
        self.animate()

    def animate(self):
        """Animate sprite on delay timer"""
        if self.animated and px.frame_count % ANIMATION_DELAY == 0:
            self.frame = SPRITE_SIZE if self.frame == 0 else 0

    def draw(
        self,
    ):
        """Draw tile sprite onto game board"""
        px.blt(
            self.convert_grid_to_px(self.x) + GRID_X_OFFSET,
            self.convert_grid_to_px(self.y) + GRID_Y_OFFSET,
            IMAGE_SHEET,
            self.sprite.x + self.frame,
            self.sprite.y,
            TILE_SIZE,
            TILE_SIZE,
            scale=GAME_SCALE,
            colkey=TRANSPARENCY,
        )
        # print(self.x, self.y, BOARD_WIDTH, BOARD_HEIGHT)

    def convert_grid_to_px(self, grid_pos: int = 0) -> int:
        """Convert grid coordinates to world pixels"""
        return (grid_pos * GRID_SIZE) + SPRITE_OFFSET

    def __repr__(self) -> str:
        return f"TILE({self.x},{self.y})"
