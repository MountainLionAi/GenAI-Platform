from telebot.async_telebot import AsyncTeleBot
# from telebot import asyncio_helper
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.apihelper import ApiException, ApiTelegramException
from genaipf.utils.log_utils import logger
from genaipf.bot.tg.utils import i18n_util
from genaipf.bot.tg.utils.keyboard_util import quick_markup_title
from genaipf.bot.tg.client.price_predict_client import PricePredictClient
from genaipf.bot.tg.client.research_report_client import ResearchReportClient
from genaipf.bot.tg import bot_cache
from genaipf.conf import tg_bot_conf
from genaipf.controller.gptstream import getAnswerAndCallGpt
import time
import json
import asyncio
import re

# asyncio_helper.proxy = 'http://127.0.0.1:7890'


def reply_keyboards(message):
    return [
        KeyboardButton(i18n_util.get_text(message)('币价预测')),
        KeyboardButton(i18n_util.get_text(message)('研究报告')),
        KeyboardButton(i18n_util.get_text(message)('切换语言')),
    ]


def select_lang_button(msg):
    return {
        'page_button': [['🇨🇳简体中文', {'callback_data': 'select_zh_cn'}],
                        ['🇬🇧English', {'callback_data': 'select_en'}]]
    }
    
    
def escape_markdown(text):
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

class TgAiBot:
    def __init__(self):
        self.__bot = AsyncTeleBot(tg_bot_conf.BOT_TOKEN)
        self.__started = False  # 添加一个状态变量来跟踪是否已经启动
        self.__initialize_handlers()
        self.price_predict_client = PricePredictClient(self.__bot)
        self.research_report_client = ResearchReportClient(self.__bot)

    def __initialize_handlers(self):

        @self.__bot.callback_query_handler(func=lambda c: c.data in ['select_zh_cn', 'select_en'])
        async def select_items_handler(call):
            if call.data == 'select_zh_cn':
                i18n_util.set_text(call.message, 'zh_CN')
                await send_start(call.message)
                bot_cache.set_lang(call.message, 'zh')
            elif call.data == 'select_en':
                i18n_util.set_text(call.message, 'en')
                await send_start(call.message)
                bot_cache.set_lang(call.message, 'en')
        

        @self.__bot.message_handler(commands=['start'])
        async def send_start(message):
            language_code = 'en' if message.from_user.language_code is None else message.from_user.language_code.lower()
            lang = 'zh_CN' if 'zh' in language_code else 'en'
            i18n_util.get_text(message, lang)
            bot_cache.set_lang(message, 'zh' if lang == 'zh_CN' else lang)
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
            markup.add(*reply_keyboards(message))
            await self.__bot.send_message(message.chat.id, i18n_util.get_text(message)("请选择下方菜单"),
                                          reply_markup=markup)


        @self.__bot.callback_query_handler(func=lambda c: c.data in ['releated_question_one', 'releated_question_two', 'releated_question_three'])
        async def releated_question_handler(call):
            await self.send_message(call.message.text, call.message)
        

        @self.__bot.message_handler(func=lambda message: True)
        async def echo_all(message):
            chat_id = message.chat.id
            logger.info(f'receive message={message.text}, chat_id={chat_id}')
            if message.text == i18n_util.get_text(message)("币价预测"):
                await self.price_predict_client.price_predict_info(message)
            elif message.text == i18n_util.get_text(message)("研究报告"):
                await self.research_report_client.research_report_info(message)
            elif message.text == i18n_util.get_text(message)("切换语言"):
                select_lang_keyboard = quick_markup_title(select_lang_button(message))
                param = i18n_util.get_text(message)("请选择语言")
                await self.__bot.send_message(message.chat.id, param, reply_markup=select_lang_keyboard)
            else:
                await self.send_message(None,message)
                
                

    async def send_message(self, to_ask_gpt_question, message):
        chat_id = message.chat.id
        logger.info(f"message.chat.type={message.chat.type}")
        need_answer = False
        group_talk = False
        if not to_ask_gpt_question:
            to_ask_gpt_question = message.text
        if message.chat.type == "private":
            need_answer = True
        elif message.chat.type in ["group", "supergroup", "channel"]:
            if f"@{tg_bot_conf.BOT_USER_NAME}" in to_ask_gpt_question:
                need_answer = True
                group_talk = True
                to_ask_gpt_question = to_ask_gpt_question.replace(f"@{tg_bot_conf.BOT_USER_NAME}", "")
        if not need_answer:
            return
        text = ""
        message_count = 0
        batch_size = 25
        text_parts = []
        sent_msg = None
        releated_question_keyboard = None
        
        _question = to_ask_gpt_question
        _userid = None
        _msggroup = None,
        _language = bot_cache.get_lang(message)
        _front_messages = [{"role": "user", "content": to_ask_gpt_question}]
        _device_no = None
        _question_code = None
        _model = "ml-plus"
        _output_type = "text"
        _source = "v203"
        _owner = "tgbot"
        _agent_id = None
        _chain_id = None
        _llm_model = "openai"
        _wallet_type = None
        _regenerate_response = None
        async for str in getAnswerAndCallGpt(_question, _userid, _msggroup, _language, _front_messages, _device_no, _question_code, _model, _output_type, _source, _owner, _agent_id, _chain_id, _llm_model, _wallet_type, _regenerate_response):
            _msg_json = json.loads(str)
            _type = _msg_json.get("role")
            _content = _msg_json.get("content")
            if _type == 'gpt':
                if _content != "llm_yielding" and _content != "":
                    _content = escape_markdown(_content)
                    if _content == ' ':
                        _content = _content + '\u200b'
                    text_parts.append(_content)
                    message_count += 1
                    if message_count >= batch_size:
                        final_text = ''.join(text_parts)
                        text += final_text
                        if sent_msg is None:
                            if group_talk:
                                sent_msg = await self.__bot.send_message(chat_id, text, parse_mode="MarkdownV2", reply_to_message_id=message.message_id)
                            else:
                                sent_msg = await self.__bot.send_message(chat_id, text, parse_mode="MarkdownV2")
                        else:
                            await self.retry_send_message(chat_id, sent_msg.message_id, text, releated_question_keyboard)
                        text_parts = []
                        message_count = 0
                        time.sleep(0.7)
            elif _type == 'step':
                if _content == 'done':
                    if text_parts:
                        final_text = ''.join(text_parts)
                        text += final_text
                        if sent_msg is None:
                            if group_talk:
                                sent_msg = await self.__bot.send_message(chat_id, text, parse_mode="MarkdownV2", reply_to_message_id=message.message_id)
                            else:
                                sent_msg = await self.__bot.send_message(chat_id, text, parse_mode="MarkdownV2")
                        else:
                            await self.retry_send_message(chat_id, sent_msg.message_id, text, releated_question_keyboard)
                    logger.info("输出结束")
            elif _type == 'chatRelatedResults':
                contents = _msg_json.get("content")
                if contents and len(contents) > 0:
                    button = {
                        'one': [
                            [contents[0]["title"], {'callback_data': 'releated_question_one'}],
                        ],
                        "two": [
                            [contents[1]["title"], {'callback_data': 'releated_question_two'}],
                        ],
                        "three": [
                            [contents[2]["title"], {'callback_data': 'releated_question_three'}],
                        ],
                    }
                    releated_question_keyboard = quick_markup_title(button)
        logger.info(f"text=\n{text}")

    
    async def retry_send_message(self, chat_id, message_id, text, releated_question_keyboard):
        while True:
            try:
                if releated_question_keyboard:
                    await self.__bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, parse_mode="MarkdownV2", reply_markup=releated_question_keyboard)
                else:
                    await self.__bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, parse_mode="MarkdownV2")
                break
            except Exception as e:
                if e.error_code == 429:
                    retry_after = int(e.result.json().get('parameters', {}).get('retry_after', 1))
                    logger.warning(f"Rate limited by Telegram API, retrying in {retry_after} seconds")
                    await asyncio.sleep(retry_after)
                else:
                    logger.error(f"Failed to send message: {e}")
                    break

    
    def get_bot(self):
        return self.__bot

    async def startup(self):
        if not self.__started:
            logger.info('start zgc_ai_bot')
            self.__started = True  # 标记为已启动
            await self.__bot.polling()
        else:
            logger.info("zgc_ai_bot is already running.")


tgAiBot = TgAiBot()
