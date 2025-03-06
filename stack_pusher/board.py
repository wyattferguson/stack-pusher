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
    SPRITE_OFFSET,
    STARTING_COLS,
    TILE_SIZE,
    TILEMAP_GAME,
    TIMER_LENGTH,
    TRANSPARENCY,
    Pt,
)
from cursor import Cursor
from timer import Timer


class Board:
    def __init__(self) -> None:
        self.game_over: bool = False
        self.cursor = Cursor()
        self.score: int = 0
        self.goal_score: int = 0
        self.timer = Timer(TIMER_LENGTH)
        self.level: int = 0
        self.board: list[list[Pt | bool]] = []
        self.block_types: list[Pt] = [BLOCK_PINK, BLOCK_GREEN, BLOCK_YELLOW, BLOCK_PURPLE]
        self.next_level()

    def next_level(self) -> None:
        """Increase game difficulty and reset board"""
        self.level += 1
        self.score = 0
        self.goal_score = int(GOAL_SCORE * (1 + self.level / 10))
        self.board = [[False] * BOARD_WIDTH for i in range(BOARD_HEIGHT + 1)]
        self.timer.reset()

        # increase number of starting columns every 5 levels
        starting_cols: int = STARTING_COLS + (self.level // 5)
        if starting_cols > 10:
            starting_cols = 10

        for i in range(starting_cols):
            self.gen_next_column()

        px.play(1, px.sounds[SND_NEW_LEVEL])

    def update(self) -> None:
        """Update game state every frame"""
        self.cursor.update()
        self.timer.update()

        if self.cursor.selected:
            if self.board[self.cursor.y][self.cursor.x] == BLOCK_BOMB:
                self.trigger_bomb(self.cursor.x)
            else:
                self.clear_block_group(self.cursor.x, self.cursor.y)
                self.shift_blocks_down()

        if self.timer.is_action():
            self.gen_next_column()

        self.input()

    def draw(self) -> None:
        """Draw game state every frame"""
        px.bltm(0, 0, TILEMAP_GAME, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        # draw all board pieces
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x]:
                    self.draw_tile(x, y, self.board[y][x])

        self.draw_tile(self.cursor.x, self.cursor.y, self.cursor.sprite)
        self.draw_nav()

    def draw_nav(self) -> None:
        """Draw topbar with timer and level progress"""
        self.timer.draw()

        # draw current level
        px.text(
            px.width - (3 * GRID_SIZE),
            NAV_Y_OFFSET,
            f"LEVEL {self.level}",
            COL_NAV,
            font=None,
        )

        px.text(
            GRID_SIZE // 2,
            NAV_Y_OFFSET,
            "NEXT",
            COL_NAV,
            font=None,
        )

        # draw next level progress bar
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

    def input(self) -> None:
        """Get Keyboard / Gamepad Input"""
        # trigger next wave of blocks
        if px.btnr(px.KEY_F):
            self.gen_next_column()
            self.timer.reset()

    def trigger_bomb(self, bomb_x: int) -> None:
        """Clear out columns surrounding triggered bomb"""
        for x in range(-1, 2):
            if bomb_x + x >= 0:
                for y in range(BOARD_HEIGHT):
                    self.board[y][bomb_x + x] = False

    def clear_block_group(self, grid_x: int = 0, grid_y: int = 0) -> None:
        """Delete touching blocks of same selected color"""
        offset_x = grid_x
        if not self.board[grid_y][offset_x]:
            return

        selected_block: Pt | bool = self.board[grid_y][offset_x]

        found = self.connected_blocks(
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

    def connected_blocks(self, x: int, y: int, block_color: Pt | bool) -> int:
        """Recursively search around given block for matching blocks

        Args:
            x (int): Current block x position
            y (int): Current block y position
            block_color (Pt): Color of the block to match

        Returns:
            int: number of connected blocks found
        """
        cur_block = self.board[y][x]
        # has the search hit a wall or a different color block
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
        # recursively search all 4 directions around current block
        found = (
            1
            + self.connected_blocks(x + 1, y, block_color)
            + self.connected_blocks(x - 1, y, block_color)
            + self.connected_blocks(x, y + 1, block_color)
            + self.connected_blocks(x, y - 1, block_color)
        )

        return found

    def draw_tile(self, x: int, y: int, sprite: Pt | bool) -> None:
        """Draw single tile sprite onto game board"""
        if not isinstance(sprite, Pt):
            return

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

    def shift_blocks_down(self) -> None:
        """Move all blocks down to fill empty space"""
        for x in range(BOARD_WIDTH):
            moved: bool = True
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

    def gen_next_column(self) -> None:
        """Generate a new column of blocks"""
        for y in range(BOARD_HEIGHT):
            # every level decrease the odds of a bomb spawning
            self.board[y][BOARD_WIDTH - 1] = (
                BLOCK_BOMB
                if random.randint(0, 70 + self.level) == 3
                else random.choice(self.block_types)
            )

        self.shift_blocks_left()

    def shift_blocks_left(self) -> None:
        """Shift every column left 1 grid space"""

        # find furthest right empty column
        last_empty_col: int = 0
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

    def is_game_over(self) -> bool:
        return self.game_over
