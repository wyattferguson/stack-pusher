import pyxel as px
from board import Board
from config import (
    DISPLAY_SCALE,
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    STATE_MENU,
    STATE_PLAYING,
)


class Ores:
    def __init__(self):
        px.init(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            title="Ores",
            fps=FPS,
            display_scale=DISPLAY_SCALE,
        )
        px.load("assets.pyxres")

        self.board = Board()
        self.state = STATE_PLAYING
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
        """Watch keyboard for WASD and R(Reset)"""
        if self.state == STATE_MENU:
            if px.btn(px.KEY_RETURN) or px.btn(px.GAMEPAD1_BUTTON_START):
                self.state = STATE_PLAYING

        # Reset game on (R)
        if px.btn(px.KEY_R):
            self.new_game()

    def draw(self):
        """Redraw game board and sprites"""
        px.cls(px.COLOR_BLACK)
        self.board.draw()


if __name__ == "__main__":
    Ores()
