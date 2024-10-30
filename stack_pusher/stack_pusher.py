# title: Stack Pusher
# author: Wyatt Ferguson
# desc: A python remake of the flash game Ores
# site: https://github.com/wyattferguson/stack-pusher
# license: MIT
# version: 1.0


import pyxel as px
from board import Board
from config import (
    COL_NAV,
    DISPLAY_SCALE,
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    STATE_MENU,
    STATE_PLAYING,
    TILEMAP_MENU,
)
from text import display_notice


class StackPusher:
    def __init__(self):
        px.init(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            title="Stack Pusher",
            fps=FPS,
            display_scale=DISPLAY_SCALE,
        )
        px.load("assets.pyxres")

        self.board = False
        self.state = STATE_MENU
        px.run(self.update, self.draw)

    def update(self):
        """Update game state every frame"""
        self.keyboard()
        if self.state == STATE_PLAYING:
            self.board.update()

    def new_game(self):
        """Full game restart"""
        self.board = Board()

    def keyboard(self):
        """Watch keyboard for Enter/Space and R(Reset)"""
        if self.state == STATE_MENU:
            if (
                px.btn(px.KEY_RETURN)
                or px.btn(px.KEY_SPACE)
                or px.btn(px.GAMEPAD1_BUTTON_START)
            ):
                self.state = STATE_PLAYING
                self.new_game()

        # Reset game on (R)
        elif px.btn(px.KEY_R):
            self.new_game()

    def draw(self):
        """Redraw game board and sprites"""
        px.cls(px.COLOR_BLACK)
        if self.state == STATE_MENU:
            px.bltm(0, 0, TILEMAP_MENU, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.draw_menu()
        elif self.state == STATE_PLAYING:
            self.board.draw()

    def draw_menu(self):
        display_notice("STACK PUSHER", y_offset=-50)
        px.text(
            5,
            px.height // 3,
            """
            W,A,S,D - Movement \n
            F - Push Stack \n
            Space - Select Block \n
            R - Restart \n
            P - Pause
            """,
            COL_NAV,
        )


if __name__ == "__main__":
    StackPusher()
