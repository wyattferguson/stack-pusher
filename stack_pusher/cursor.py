import pyxel as px

from config import (
    ANIMATION_DELAY,
    BOARD_HEIGHT,
    BOARD_WIDTH,
    CURSOR_SPRITE,
    SPRITE_SIZE,
    Pt,
)


class Cursor:
    """Cursor class for selecting tiles on the board"""

    def __init__(
        self,
        x: int = 0,
        y: int = 0,
    ) -> None:
        self.x: int = x
        self.y: int = y
        self._sprite: Pt = CURSOR_SPRITE
        self.frame: int = 0
        self.selected: bool | Pt = False

    @property
    def sprite(self) -> Pt:
        """Convert Cursor to Pt object"""
        return Pt(self._sprite.x + self.frame, self._sprite.y)

    def update(self) -> None:
        """Update cursor animation every frame"""
        if px.frame_count % ANIMATION_DELAY == 0:
            self.frame = SPRITE_SIZE if self.frame == 0 else 0
        self.input()

    def input(self) -> None:
        """Read Keyboard / Gamepad Input"""
        if px.btn(px.KEY_W) or px.btn(px.GAMEPAD1_BUTTON_DPAD_UP):
            if self.y > 0:
                self.y -= 1
        elif px.btn(px.KEY_S) or px.btn(px.GAMEPAD1_BUTTON_DPAD_DOWN):
            if self.y < BOARD_HEIGHT - 1:
                self.y += 1
        elif px.btn(px.KEY_A) or px.btn(px.GAMEPAD1_BUTTON_DPAD_LEFT):
            if self.x > 0:
                self.x -= 1
        elif px.btn(px.KEY_D) or px.btn(px.GAMEPAD1_BUTTON_DPAD_RIGHT):
            if self.x < BOARD_WIDTH - 2:
                self.x += 1

        if px.btnr(px.KEY_SPACE) or px.btnr(px.GAMEPAD1_BUTTON_A):
            self.selected = Pt(self.x, self.y)
        else:
            self.selected = False
