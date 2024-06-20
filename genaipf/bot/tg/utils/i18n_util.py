import gettext
import os
from genaipf.conf.tg_bot_conf import LOCALES_FILE_PATH

user_id_lang = {}


def set_text(msg, lang='en'):
    translation = gettext.translation('tgbot', localedir=LOCALES_FILE_PATH, languages=[lang]).gettext
    user_id_lang[msg.chat.id] = translation


def get_text(msg, lang='en'):
    if msg.chat.id in user_id_lang:
        return user_id_lang[msg.chat.id]
    translation = gettext.translation('tgbot', localedir=LOCALES_FILE_PATH, languages=[lang]).gettext
    user_id_lang[msg.chat.id] = translation
    return translation


def get_text_by_chat_id(chat_id, lang='en'):
    if chat_id in user_id_lang:
        return user_id_lang[chat_id]
    translation = gettext.translation('tgbot', localedir='locales', languages=[lang]).gettext
    user_id_lang[chat_id] = translation
    return translation