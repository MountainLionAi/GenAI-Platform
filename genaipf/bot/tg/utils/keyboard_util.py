from typing import Dict, Any
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def _gen_inline_btn(btn_info: Dict[str, Dict[str, Any]]):
    return [InlineKeyboardButton(text=text, **kwargs) for text, kwargs in btn_info]


def quick_markup_title(button):
    swap_face_keyboard = InlineKeyboardMarkup()
    for item, cont in button.items():
        swap_face_keyboard.row(*_gen_inline_btn(cont))
    return swap_face_keyboard


