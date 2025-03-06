# title: Stack Pusher
# author: Wyatt Ferguson
# desc: A python remake of the flash game Ores
# site: https://wyattferguson.github.io/
# license: MIT
# version: 0.1.1


import pyxel as px
from board import Board
from config import (
    COL_NAV,
    DISPLAY_SCALE,
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILEMAP_MENU,
    States,
)
from text import display_notice


class StackPusher:
    """Main game class"""

    def __init__(self) -> None:
        px.init(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            title="Stack Pusher",
            fps=FPS,
            display_scale=DISPLAY_SCALE,
        )
        px.load("assets.pyxres")
        self.board = Board()
        self.state = States.MENU
        px.run(self.update, self.draw)

    def update(self) -> None:
        """Update game state every frame"""
        self.keyboard()

        if self.board.is_game_over():
            self.state = States.GAMEOVER
        elif self.state == States.PLAYING:
            self.board.update()

    def new_game(self) -> None:
        """Full game restart"""
        self.board = Board()
        self.state = States.PLAYING

    def keyboard(self) -> None:
        """Watch keyboard for Enter/Space and R(Reset)"""

        # Start game on (Enter/Space)
        if px.btn(px.KEY_RETURN) or px.btn(px.KEY_SPACE) or px.btn(px.GAMEPAD1_BUTTON_START):
            if self.state == States.MENU:
                self.new_game()

        # Reset game on (R)
        elif px.btn(px.KEY_R):
            self.new_game()

        # pause / unpause game
        elif px.btn(px.KEY_P) or px.btn(px.GAMEPAD1_BUTTON_START):
            self.state = States.PAUSED if self.state == States.PLAYING else States.PLAYING

    def draw(self) -> None:
        """Redraw game board and sprites"""
        px.cls(px.COLOR_BLACK)
        if self.state == States.MENU:
            px.bltm(0, 0, TILEMAP_MENU, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            self.main_menu_screen()
        elif self.state == States.PLAYING:
            self.board.draw()
        elif self.state == States.PAUSED:
            self.pause_screen()
        else:
            self.game_over_screen()

    def main_menu_screen(self) -> None:
        """Display main menu text on start up"""
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
            font=None,
        )

    def pause_screen(self) -> None:
        """Overlay pause message on screen"""
        display_notice("PAUSED")

    def game_over_screen(self) -> None:
        """Overlay game over message on screen"""
        display_notice("GAME OVER")


if __name__ == "__main__":
    StackPusher()
