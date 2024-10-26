import random
import time

import pyxel as px
from config import (
    BLOCK_GREEN,
    BLOCK_PINK,
    BLOCK_PURPLE,
    BLOCK_YELLOW,
    BOARD_HEIGHT,
    BOARD_WIDTH,
    FOUND_SPRITE,
    GRID_SIZE,
    GRID_X_OFFSET,
    GRID_Y_OFFSET,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    Pt,
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
        self.timer = Timer(5)
        self.level = level
        self.tboard = [[0] * BOARD_WIDTH for i in range(BOARD_HEIGHT + 1)]
        self.board = [[False] * BOARD_WIDTH for i in range(BOARD_HEIGHT + 1)]
        self.block_types = [BLOCK_PINK, BLOCK_GREEN, BLOCK_YELLOW, BLOCK_PURPLE]

        for i in range(3):
            self.gen_next_column()

        self.pg()

    def update(self):
        if self.running and not self.game_over:
            self.cursor.update()
            self.timer.update()

            if self.cursor.selected:
                self.clear_block_group(self.cursor.x, self.cursor.y)
                self.shift_blocks_down()

            # if self.timer.is_action():
            #     self.gen_next_column()

        self.input()

    def draw(self):
        px.bltm(0, 0, 0, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        if not self.game_over:
            for y in range(BOARD_HEIGHT):
                for x in range(BOARD_WIDTH):
                    if self.board[y][x]:
                        Tile(x, y, self.board[y][x].sprite).draw()
                        # self.board[y][x].draw()

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

        # trigger next wave of blocks
        elif px.btn(px.KEY_F):
            self.gen_next_column()

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

    def clear_block_group(self, grid_x: int = 0, grid_y: int = 0):
        """Delete touching blocks of same selected color"""
        offset_x = grid_x
        if self.board[grid_y][offset_x]:
            selected_block = self.board[grid_y][offset_x]

            found = self.grid_search(
                offset_x,
                grid_y,
                selected_block.sprite,
            )

            if found <= 1:
                self.board[grid_y][offset_x] = selected_block

        self.pg()

    def grid_search(self, x: int, y: int, block_color: Pt) -> int:
        """Recursively search around given block for matching blocks"""
        cur_block = self.board[y][x]
        if (
            not cur_block
            or cur_block.sprite != block_color
            or x < 0
            or x > BOARD_WIDTH - 1
            or y < 0
            or y > BOARD_HEIGHT - 1
        ):
            return 0

        self.board[y][x] = False
        found = 1
        found += self.grid_search(x + 1, y, block_color)
        found += self.grid_search(x - 1, y, block_color)
        found += self.grid_search(x, y + 1, block_color)
        found += self.grid_search(x, y - 1, block_color)

        return found

    def pg(self):
        print("########################")
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                self.tboard[y][x] = 0
                if self.board[y][x]:
                    self.tboard[y][x] = 1

        for y in range(BOARD_HEIGHT):
            print(self.tboard[y])

    def shift_blocks_down(self):
        """Move all blocks down to fill empty space"""
        for x in range(BOARD_WIDTH):
            moved = 1
            # keep looping until no more swaps have been made
            while moved > 0:
                moved = 0
                for y in range(BOARD_HEIGHT - 1, 0, -1):
                    # is the current block empty and the one above not
                    if not self.board[y][x] and self.board[y - 1][x]:
                        # swap block above
                        self.board[y][x], self.board[y - 1][x] = (
                            self.board[y - 1][x],
                            self.board[y][x],
                        )
                        moved += 1
        self.pg()

    def gen_next_column(self):
        """Generate a new column of blocks"""
        for y in range(BOARD_HEIGHT):
            next_block_sprite = random.choice(self.block_types)
            self.board[y][BOARD_WIDTH - 1] = Tile(BOARD_WIDTH, y, next_block_sprite)

        self.shift_blocks_left()

    def shift_blocks_left(self):
        """Shift every column forward 1 grid space"""
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
