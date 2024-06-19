from genaipf.bot.tg.utils import i18n_util, keyboard_util
from genaipf.conf import tg_bot_conf
from genaipf.bot.tg import bot_cache


def price_predict_button(message):
    return {
        'one': [
            [i18n_util.get_text(message)('BTC/bitcoin'), {'callback_data': 'btc'}],
            [i18n_util.get_text(message)('ETH/ethereum'), {'callback_data': 'eth'}],
        ],
        "two": [
            [i18n_util.get_text(message)('BNB/binance-coin'), {'callback_data': 'bnb'}],
            [i18n_util.get_text(message)('DOGE/dogecoin'), {'callback_data': 'doge'}],
        ],
        "three": [
            [i18n_util.get_text(message)('TRX/tron'), {'callback_data': 'tron'}],
            [i18n_util.get_text(message)('MATIC/matictoken'), {'callback_data': 'matic'}],
        ],
        "four": [
            [i18n_util.get_text(message)('XRP/ripple'), {'callback_data': 'xrp'}],
            [i18n_util.get_text(message)('ADA/cardano'), {'callback_data': 'ada'}],
        ],
        "five": [
            [i18n_util.get_text(message)('ARB/arbitrum'), {'callback_data': 'arb'}],
            [i18n_util.get_text(message)('SOL/solana'), {'callback_data': 'sol'}],
        ]
    }


url_param = {
    "btc": ("BTC", "bitcoin"),
    "eth": ("ETH", "ethereum"),
    "bnb": ("BNB", "binance-coin"),
    "doge": ("DOGE", "dogecoin"),
    "tron": ("TRX", "tron"),
    "matic": ("MATIC", "matictoken"),
    "xrp": ("XRP", "ripple"),
    "ada": ("ADA", "cardano"),
    "arb": ("ARB", "arbitrum"),
    "sol": ("SOL", "solana"),
}


class PricePredictClient:

    def __init__(self, bot):
        self.bot = bot
        self.__init_handlers()

    def __init_handlers(self):
        # https://test1.mountainlion.ai/#/?isBot=true&question=BTC每日预测&type=preset4&code=bitcoin
        @self.bot.callback_query_handler(func=lambda c: c.data in ['btc', 'eth', 'bnb', 'doge', 'tron', 'matic', 'xrp', 'ada', 'arb', 'sol'])
        async def price_predict_callback_handler(call):
            base_url = tg_bot_conf.MOUNTAIN_HOST
            coin = url_param.get(call.data)
            text = base_url + f"isBot=true&question={coin[0]}每日预测&type=preset4&code={coin[1]}&lang={bot_cache.get_lang(call.message)}"
            await self.bot.send_message(chat_id=call.message.chat.id, text=text)

    async def price_predict_info(self, message):
        price_predict_keyboard = keyboard_util.quick_markup_title(price_predict_button(message))
        text = i18n_util.get_text(message)("选择一个币种")
        await self.bot.send_message(chat_id=message.chat.id, text=text, reply_markup=price_predict_keyboard)
