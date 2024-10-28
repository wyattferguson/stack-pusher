import random

import pyxel as px
from config import (
    BLOCK_BOMB,
    BLOCK_GREEN,
    BLOCK_PINK,
    BLOCK_PURPLE,
    BLOCK_SCORE,
    BLOCK_YELLOW,
    BOARD_HEIGHT,
    BOARD_WIDTH,
    COL_NAV,
    GAME_SCALE,
    GOAL_SCORE,
    GRID_SIZE,
    GRID_X_OFFSET,
    GRID_Y_OFFSET,
    IMAGE_SHEET,
    NAV_Y_OFFSET,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SND_NEW_LEVEL,
    SND_PUSH_BLOCKS,
    SPRITE_OFFSET,
    STARTING_COLS,
    TILE_SIZE,
    TIMER_LENGTH,
    TRANSPARENCY,
    Pt,
)
from cursor import Cursor
from text import center_text_horz, center_text_vert
from timer import Timer


class Board(object):
    """docstring for Board."""

    def __init__(self):
        self.running = True
        self.game_over = False
        self.cursor = Cursor()
        self.score = 0
        self.goal_score = 0
        self.timer = Timer(TIMER_LENGTH)
        self.level = 0
        self.board = []
        self.block_types = [BLOCK_PINK, BLOCK_GREEN, BLOCK_YELLOW, BLOCK_PURPLE]
        self.next_level()

    def next_level(self):
        self.level += 1
        self.score = 0
        self.goal_score = GOAL_SCORE * (1 + self.level / 10)
        self.board = [[False] * BOARD_WIDTH for i in range(BOARD_HEIGHT + 1)]
        self.timer.reset()

        # increase number of starting columns every 5 levels
        starting_cols = STARTING_COLS + (self.level // 5)
        if starting_cols > 10:
            starting_cols = 10

        for i in range(starting_cols):
            self.gen_next_column()

        px.play(1, px.sounds[SND_NEW_LEVEL])

    def update(self):
        if self.running and not self.game_over:
            self.cursor.update()
            self.timer.update()

            if self.cursor.selected:
                if self.board[self.cursor.y][self.cursor.x] == BLOCK_BOMB:
                    self.trigger_bomb(self.cursor.y, self.cursor.x)
                else:
                    self.clear_block_group(self.cursor.x, self.cursor.y)
                    self.shift_blocks_down()

            if self.timer.is_action():
                self.gen_next_column()
                # px.play(1, px.sounds[SND_PUSH_BLOCKS])

        self.input()

    def draw(self):
        px.bltm(0, 0, 0, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        if self.game_over:
            self.game_over_screen()
            return

        # draw all board pieces
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x]:
                    self.draw_tile(x, y, self.board[y][x])

        self.draw_tile(self.cursor.x, self.cursor.y, self.cursor.sprite)
        self.draw_nav()

        if not self.running:
            self.pause_screen()

    def draw_nav(self):
        self.timer.draw()

        # draw current level
        px.text(
            px.width - (3 * GRID_SIZE), NAV_Y_OFFSET, f"LEVEL {self.level}", COL_NAV
        )

        # draw next level progress bar
        px.text(GRID_SIZE // 2, NAV_Y_OFFSET, "NEXT", COL_NAV)
        px.rect(
            GRID_SIZE * 1.75,
            NAV_Y_OFFSET,
            GRID_SIZE * 2.5,
            px.FONT_HEIGHT - 1,
            px.COLOR_LIGHT_BLUE,
        )
        px.rect(
            GRID_SIZE * 1.75,
            NAV_Y_OFFSET,
            GRID_SIZE * 2.5 * (self.score / self.goal_score),
            px.FONT_HEIGHT - 1,
            px.COLOR_RED,
        )

    def input(self):
        """Keyboard / Gamepad Input"""
        # pause / unpause game
        if px.btn(px.KEY_P) or px.btn(px.GAMEPAD1_BUTTON_START):
            self.running = not self.running

        # trigger next wave of blocks
        elif px.btnr(px.KEY_F):
            self.gen_next_column()
            self.timer.reset()

    def trigger_bomb(self, bomb_y: int, bomb_x: int):
        """Clear out columns surrounding triggered bomb"""
        for x in range(-1, 2):
            if bomb_x + x >= 0:
                for y in range(BOARD_HEIGHT):
                    self.board[y][bomb_x + x] = False

    def game_over_screen(self):
        px.cls(px.COLOR_BLACK)
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
            px.COLOR_WHITE,
        )
        px.text(x_center, y_center, text, 8)

    def clear_block_group(self, grid_x: int = 0, grid_y: int = 0):
        """Delete touching blocks of same selected color"""
        offset_x = grid_x
        if not self.board[grid_y][offset_x]:
            return

        selected_block = self.board[grid_y][offset_x]

        found = self.grid_search(
            offset_x,
            grid_y,
            selected_block,
        )

        if found <= 1:
            self.board[grid_y][offset_x] = selected_block
        else:
            self.score += int((found * BLOCK_SCORE) * 1.15)
            # start next level once goal score is hit
            if self.score > self.goal_score:
                self.next_level()

    def grid_search(self, x: int, y: int, block_color: Pt) -> int:
        """Recursively search around given block for matching blocks"""
        cur_block = self.board[y][x]
        if (
            not cur_block
            or cur_block != block_color
            or x < 0
            or x > BOARD_WIDTH - 1
            or y < 0
            or y > BOARD_HEIGHT - 1
        ):
            return 0

        self.board[y][x] = False
        found = (
            1
            + self.grid_search(x + 1, y, block_color)
            + self.grid_search(x - 1, y, block_color)
            + self.grid_search(x, y + 1, block_color)
            + self.grid_search(x, y - 1, block_color)
        )

        return found

    def draw_tile(self, x: int, y: int, sprite: Pt):
        """Draw single tile sprite onto game board"""
        px.blt(
            self.convert_grid_to_px(x) + GRID_X_OFFSET,
            self.convert_grid_to_px(y) + GRID_Y_OFFSET,
            IMAGE_SHEET,
            sprite.x,
            sprite.y,
            TILE_SIZE,
            TILE_SIZE,
            scale=GAME_SCALE,
            colkey=TRANSPARENCY,
        )

    def convert_grid_to_px(self, grid_pos: int = 0) -> int:
        """Convert grid coordinates to world pixels"""
        return (grid_pos * GRID_SIZE) + SPRITE_OFFSET

    def shift_blocks_down(self):
        """Move all blocks down to fill empty space"""
        for x in range(BOARD_WIDTH):
            moved = True
            # keep looping until no more swaps have been made
            while moved:
                moved = False
                for y in range(BOARD_HEIGHT - 1, 0, -1):
                    # is the current block empty and the one above not
                    if not self.board[y][x] and self.board[y - 1][x]:
                        # swap block above
                        self.board[y][x], self.board[y - 1][x] = (
                            self.board[y - 1][x],
                            self.board[y][x],
                        )
                        moved = True

    def gen_next_column(self):
        """Generate a new column of blocks"""
        for y in range(BOARD_HEIGHT):
            # every level decrease the odds of a bomb spawning
            self.board[y][BOARD_WIDTH - 1] = (
                BLOCK_BOMB
                if random.randint(0, 70 + self.level) == 3
                else random.choice(self.block_types)
            )

        self.shift_blocks_left()

    def shift_blocks_left(self):
        """Shift every column forward 1 grid space"""
        # find furthest right empty column
        last_empty_col = 0
        for x in range(BOARD_WIDTH - 1, 0, -1):
            if not self.board[BOARD_HEIGHT - 1][x]:
                last_empty_col = x
                break

        # shift all blocks after the empty column left
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH - 1):
                if x + 1 > last_empty_col:
                    # End game if a block is being shifted to the end of the board
                    if x == 0 and self.board[y][x]:
                        self.game_over = True
                        return
                    else:
                        self.board[y][x] = self.board[y][x + 1]
                        self.board[y][x + 1] = False
