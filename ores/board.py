import pyxel as px
from config import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    GRID_SIZE,
    GRID_X_OFFSET,
    GRID_Y_OFFSET,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from cursor import Cursor
from text import center_text_horz, center_text_vert
from timer import Timer


class Board(object):
    """docstring for Board."""

    def __init__(self, level: int = 0):
        self.running = True
        self.game_over = False
        self.cursor = Cursor()
        self.timer = Timer(4)
        self.level = level
        self.board = []

    def update(self):
        if self.running and not self.game_over:
            self.cursor.update()

            self.timer.update()

        self.keyboard()

    def draw(self):
        px.rect(
            GRID_X_OFFSET,
            GRID_Y_OFFSET,
            BOARD_WIDTH * GRID_SIZE,
            BOARD_HEIGHT * GRID_SIZE,
            5,
        )
        if not self.game_over:
            # draw background tile map
            # px.bltm(0, 0, 0, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

            self.cursor.draw()

            self.timer.draw()

            if not self.running:
                self.pause()
        else:
            self.game_over_screen()

    def keyboard(self):
        # pause / unpause game
        if px.btn(px.KEY_P) or px.btn(px.GAMEPAD1_BUTTON_START):
            self.running = not self.running

        # kill game
        elif px.btn(px.KEY_K):
            self.game_over = True

        if self.running:
            self.cursor.move()

    def game_over_screen(self):
        self.display_notice("GAME OVER")

    def pause(self):
        self.display_notice("PAUSED")

    def display_notice(self, text: str = ""):
        """Display text box in the center of the board"""

        x_center = center_text_horz(text)
        y_center = center_text_vert()
        px.rect(
            center_text_horz(text) - 10,
            y_center - 5,
            len(text) * 5 + 10,
            14,
            7,
        )
        px.text(x_center, y_center, text, 8)

    def delete_tile(self, piece):
        pass

    def remove_dead(self):
        """Delete any dead pieces from the board"""
        for piece in self.pieces[:]:
            if not piece.alive:
                self.delete_piece(piece)

    def add_piece(self):
        pass
