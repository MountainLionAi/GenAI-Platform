from genaipf.bot.tg.utils import i18n_util, keyboard_util
from genaipf.conf import tg_bot_conf
from genaipf.bot.tg import bot_cache
import urllib.parse


def research_report_button(message):
    return {
        'one': [
            [i18n_util.get_text(message)('BTC/bitcoin'), {'callback_data': 'rr_btc'}],
            [i18n_util.get_text(message)('ETH/ethereum'), {'callback_data': 'rr_eth'}],
        ],
        "two": [
            [i18n_util.get_text(message)('BNB/binance-coin'), {'callback_data': 'rr_bnb'}],
            [i18n_util.get_text(message)('DOGE/dogecoin'), {'callback_data': 'rr_doge'}],
        ],
        "three": [
            [i18n_util.get_text(message)('TRX/tron'), {'callback_data': 'rr_tron'}],
            [i18n_util.get_text(message)('MATIC/matictoken'), {'callback_data': 'rr_matic'}],
        ],
        "four": [
            [i18n_util.get_text(message)('XRP/ripple'), {'callback_data': 'rr_xrp'}],
            [i18n_util.get_text(message)('ADA/cardano'), {'callback_data': 'rr_ada'}],
        ],
        "five": [
            [i18n_util.get_text(message)('ARB/arbitrum'), {'callback_data': 'rr_arb'}],
            [i18n_util.get_text(message)('SOL/solana'), {'callback_data': 'rr_sol'}],
        ]
    }


url_param = {
    "rr_btc": ("BTC", "bitcoin"),
    "rr_eth": ("ETH", "ethereum"),
    "rr_bnb": ("BNB", "binance-coin"),
    "rr_doge": ("DOGE", "dogecoin"),
    "rr_tron": ("TRX", "tron"),
    "rr_matic": ("MATIC", "matictoken"),
    "rr_xrp": ("XRP", "ripple"),
    "rr_ada": ("ADA", "cardano"),
    "rr_arb": ("ARB", "arbitrum"),
    "rr_sol": ("SOL", "solana"),
}


class ResearchReportClient:

    def __init__(self, bot):
        self.bot = bot
        self.__init_handlers()

    def __init_handlers(self):
        # https://test1.mountainlion.ai/#/?isBot=true&question=BTC的研报
        @self.bot.callback_query_handler(
            func=lambda c: c.data in ['rr_btc', 'rr_eth', 'rr_bnb', 'rr_doge', 'rr_tron', 'rr_matic', 'rr_xrp', 'rr_ada', 'rr_arb', 'rr_sol'])
        async def price_predict_callback_handler(call):
            base_url = tg_bot_conf.MOUNTAIN_HOST
            coin = url_param.get(call.data)
            question_text = i18n_util.get_text(call.message)("每日预测")
            params = {
                'isBot': 'true',
                'question': f'{coin[0]}{question_text}',
                'lang': f'{bot_cache.get_lang(call.message)}'
            }
            # text = base_url + f"isBot=true&question={coin[0]}{question_text}&lang={bot_cache.get_lang(call.message)}"
            text = base_url + urllib.parse.urlencode(params)
            await self.bot.send_message(chat_id=call.message.chat.id, text=text)

    async def research_report_info(self, message):
        price_predict_keyboard = keyboard_util.quick_markup_title(research_report_button(message))
        text = i18n_util.get_text(message)("选择一个币种")
        await self.bot.send_message(chat_id=message.chat.id, text=text, reply_markup=price_predict_keyboard)
