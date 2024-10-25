import pyxel as px
from config import BOARD_HEIGHT, BOARD_WIDTH, CURSOR_SPRITE, Pt
from tile import Tile


class Cursor(Tile):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
    ):
        super().__init__(x, y, CURSOR_SPRITE, True)
        self.selected = False

    def update(self):
        self.animate()
        self.input()

    def input(self):
        """Keyboard / Gamepad Input"""
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
            if self.x < BOARD_WIDTH - 1:
                self.x += 1

        if px.btn(px.KEY_SPACE) or px.btn(px.GAMEPAD1_BUTTON_A):
            self.selected = Pt(self.x, self.y)
            print(self.selected)
        else:
            self.selected = False
