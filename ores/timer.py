import pyxel as px
from config import COL_TIMER, FPS
from text import center_text_horz


class Timer(object):
    """Board action timer"""

    def __init__(self, start_time: int = 10):
        self.start_time = start_time
        self.cur_time = start_time
        self.delay = 0

    def update(self):
        # reset timer when it hits 0
        if self.cur_time == 0:
            self.cur_time = self.start_time + self.delay

        # every second count down the timer
        if px.frame_count % FPS == 0:
            if self.cur_time > 0:
                self.cur_time -= 1

    def is_action(self) -> bool:
        """Has game entered the action phase"""
        return self.cur_time == 0

    def draw(self):
        # draw time left in the center of the screen
        if self.cur_time > 0 and self.cur_time <= self.start_time:
            timer_text = f"{self.cur_time}"
            self.delay = 0
        else:
            timer_text = "ATTACK!"
            if self.cur_time < self.start_time:
                self.delay = 1

        px.text(
            center_text_horz(timer_text),
            7,
            timer_text,
            COL_TIMER,
        )

        # draw count down bars
        time_per = self.cur_time / self.start_time
        screen_middle = px.width // 2
        bar_size = screen_middle * time_per
        px.rect(0, 0, px.width, 4, 1)
        if not self.delay:
            px.rect(0, 0, bar_size, 4, COL_TIMER)
            px.rect(px.width - bar_size, 0, px.width, 4, COL_TIMER)
