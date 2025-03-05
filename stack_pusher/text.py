import pyxel as px


def center_text_horz(text: str = "") -> int:
    """Calculate text position to center it horizontally on screen"""
    text_width = len(text) * px.FONT_WIDTH
    return (px.width - text_width) // 2


def center_text_vert() -> int:
    """Calculate text position to center it vertically on screen"""
    return (px.height - px.FONT_HEIGHT) // 2


def display_notice(text: str = "", x_offset: int = 0, y_offset: int = 0) -> None:
    """Display text box in the center of the board"""
    x_center = center_text_horz(text)
    y_center = center_text_vert()
    px.rect(
        center_text_horz(text) - 10 + x_offset,
        y_center - 5 + y_offset,
        len(text) * px.FONT_WIDTH + 20,
        px.FONT_HEIGHT + 8,
        px.COLOR_WHITE,
    )
    px.text(
        x_center + x_offset,
        y_center + y_offset,
        text,
        8,
        font=None,
    )
