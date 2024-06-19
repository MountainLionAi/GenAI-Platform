from telebot.async_telebot import AsyncTeleBot
from telebot import asyncio_helper
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from genaipf.utils.log_utils import logger
from utils import i18n_util
from genaipf.bot.tg.utils.keyboard_util import quick_markup_title
from genaipf.bot.tg.client.price_predict_client import PricePredictClient
from genaipf.bot.tg.client.research_report_client import ResearchReportClient
from genaipf.bot.tg import bot_cache
from genaipf.conf import tg_bot_conf
import time

asyncio_helper.proxy = 'http://127.0.0.1:7890'


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
            bot_cache.set_lang(message, 'zh')
            markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=2)
            markup.add(*reply_keyboards(message))
            await self.__bot.send_message(message.chat.id, i18n_util.get_text(message)("请选择下方菜单"),
                                          reply_markup=markup)

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
                # messages = [
                #     {
                #         "role": "system",
                #         "content": "你是一个无所不知的聊天助手，你要尽量回答用户提出的问题"
                #     },
                #     {
                #         "role": "user",
                #         "content": message.text
                #     }
                # ]
                # model = "gpt-4o"
                # response = await aref_answer_gpt_generator(messages, model)
                # text = ""
                # sent_msg = None
                # async for chunk in response:
                #     if hasattr(chunk, 'choices') and chunk.choices:
                #         if chunk.choices[0].finish_reason != 'stop':
                #             text += chunk.choices[0].delta.content
                #             if text:
                #                 if sent_msg is None:
                #                     sent_msg = await self.__bot.send_message(chat_id, text)
                #                 else:
                #                     await self.__bot.edit_message_text(text=text, chat_id=chat_id,
                #                                                        message_id=sent_msg.message_id)
                #                     time.sleep(0.05)
                await self.__bot.send_message(chat_id, message.text)

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
