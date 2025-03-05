import pyxel as px

from config import COL_NAV, FPS, NAV_Y_OFFSET
from text import center_text_horz


class Timer:
    """Board action timer"""

    def __init__(self, start_time: int = 10) -> None:
        self.start_time = start_time
        self.delay = 0
        self.reset()

    def update(self) -> None:
        """Update countdown every frame"""

        # reset timer when it hits 0
        if self.cur_time == 0:
            self.reset()

        # every second count down the timer
        if px.frame_count % FPS == 0:
            if self.cur_time > 0:
                self.cur_time -= 1

    def reset(self) -> None:
        """Reset countdown back to start time"""
        self.cur_time = self.start_time + self.delay

    def is_action(self) -> bool:
        """Has game entered the action phase"""
        return self.cur_time == 0

    def draw(self) -> None:
        """Draw timer text and countdown bars"""

        # draw time left in the center of the screen
        if self.cur_time > 0 and self.cur_time <= self.start_time:
            timer_text = f"{self.cur_time}"
            self.delay = 0
        else:
            timer_text = "PUSH!"
            if self.cur_time < self.start_time:
                self.delay = 1

        px.text(
            center_text_horz(timer_text),
            NAV_Y_OFFSET,
            timer_text,
            COL_NAV,
            font=None,
        )

        # draw count down bars
        time_per = self.cur_time / self.start_time
        screen_middle = px.width // 2
        bar_size = screen_middle * time_per
        px.rect(0, 0, px.width, 4, px.COLOR_DARK_BLUE)
        if not self.delay:
            px.rect(0, 0, bar_size, 4, COL_NAV)
            px.rect(px.width - bar_size, 0, px.width, 4, COL_NAV)
