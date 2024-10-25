import pyxel as px


def center_text_horz(text: str = "") -> int:
    text_width = len(text) * px.FONT_WIDTH
    return (px.width - text_width) // 2


def center_text_vert() -> int:
    return (px.height - px.FONT_HEIGHT) // 2
