
user_lang_set = {}


def set_lang(msg, lang):
    user_lang_set[msg.chat.id] = lang


def get_lang(msg):
    return user_lang_set[msg.chat.id]