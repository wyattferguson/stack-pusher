import random

import pyxel as px
from config import (
    BLOCK_GREEN,
    BLOCK_PINK,
    BLOCK_PURPLE,
    BLOCK_YELLOW,
    BOARD_HEIGHT,
    BOARD_WIDTH,
    GRID_SIZE,
    GRID_X_OFFSET,
    GRID_Y_OFFSET,
)
from cursor import Cursor
from text import center_text_horz, center_text_vert
from tile import Tile
from timer import Timer


class Board(object):
    """docstring for Board."""

    def __init__(self, level: int = 0):
        self.running = True
        self.game_over = False
        self.cursor = Cursor()
        self.timer = Timer(2)
        self.level = level
        self.board = [[False] * BOARD_WIDTH for i in range(BOARD_HEIGHT + 1)]
        self.block_types = [BLOCK_PINK, BLOCK_GREEN, BLOCK_YELLOW, BLOCK_PURPLE]

    def update(self):
        if self.running and not self.game_over:
            self.cursor.update()
            self.timer.update()

            if self.timer.is_action():
                self.gen_next_column()
                self.shift_column()

        self.input()

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
            for block_row in self.board:
                for block in block_row:
                    if block:
                        block.draw()

            self.cursor.draw()
            self.timer.draw()

            if not self.running:
                self.pause_screen()
        else:
            self.game_over_screen()

    def input(self):
        """Keyboard / Gamepad Input"""
        # pause / unpause game
        if px.btn(px.KEY_P) or px.btn(px.GAMEPAD1_BUTTON_START):
            self.running = not self.running

        # kill game
        elif px.btn(px.KEY_K):
            self.game_over = True

        elif px.btn(px.KEY_F):
            self.gen_next_column()
            self.shift_column()

    def game_over_screen(self):
        self.display_notice("GAME OVER")

    def pause_screen(self):
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

    def gen_next_column(self):
        """Generate a new column of blocks"""
        for y in range(BOARD_HEIGHT):
            next_block_sprite = random.choice(self.block_types)
            self.board[y][BOARD_WIDTH - 1] = Tile(BOARD_WIDTH, y, next_block_sprite)

    def shift_column(self):
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH - 1):
                # End game if a block is being shifted to the end of the board
                if x == 0 and self.board[y][x]:
                    self.game_over = True
                    return

                shift_block = self.board[y][x + 1]
                self.board[y][x] = shift_block
                if shift_block:
                    self.board[y][x].x -= 1
                self.board[y][x + 1] = False
