from genaipf.tools.search.utils.apikey_manager import get_api_key_by_type, set_api_key_unavaiable
from metaphor_python import Metaphor
from genaipf.utils.common_utils import sync_to_async
from genaipf.utils.log_utils import logger

CLIENT_TYPE = 'exa'
include_domains_zh = ['https://www.chaincatcher.com/', 'https://www.techflowpost.com/', 'https://www.odaily.news/', 'https://www.theblockbeats.info/', 'https://coinmarketcap.com/', 'https://www.mytoken.io/', 'https://www.feixiaohao.com/']
include_domains_en = ['https://defillama.com/', 'https://www.coindesk.com/', 'https://www.cryptoslate.com/', 'http://cointelegraph.com/', 'https://blockonomi.com/',
                      'https://bitcoinmagazine.com/', 'https://www.theblockcrypto.com/', 'https://decrypt.co/', 'https://www.newsbtc.com/', ' https://cryptobriefing.com/',
                      'https://www.blockchain.com/', 'https://nulltx.com/', 'https://bravenewcoin.com/', 'https://cn.cryptonews.com/', 'https://www.bloomberg.com/', 'https://www.ft.com/',
                      'https://www.wsj.com/', 'https://www.cnbc.com/', 'https://www.reuters.com/finance', 'https://www.investopedia.com/', 'https://www.marketwatch.com/', ' https://techcrunch.com/',
                      'https://www.wired.com/', 'https://www.reddit.com/', ' https://news.google.com/', 'https://flipboard.com/', 'https://feedly.com/', 'https://www.huffpost.com/', 'https://www.bbc.com/news',
                      'https://www.nytimes.com/', 'https://www.theguardian.com/international', 'https://www.cnn.com/', 'https://www.buzzfeed.com/', 'https://www.vogue.com/', 'https://seekingalpha.com/']
class MetaphorClient:
    _api_key = None
    _instance = None
    _client = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MetaphorClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._api_key = get_api_key_by_type(CLIENT_TYPE)
        self._client = Metaphor(api_key=self._api_key)
        search_of_metaphor = sync_to_async(self._client.search)
        aget_contents_of_metaphor = sync_to_async(self._client.get_contents)

    def get_current_api_key(self):
        return self._api_key

    def get_client(self):
        if self._client is not None:
            return self._client
        else:
            self._api_key = get_api_key_by_type(CLIENT_TYPE)
            self._client = Metaphor(api_key=self._api_key)
            return self._client


    async def exa_search(self, question, num_results=5, use_autoprompt=True, include_domains=[] ,type='neural'):
        search_of_metaphor = sync_to_async(self._client.search)
        search_result = []
        try:
            search_result = await search_of_metaphor(question, num_results=num_results, use_autoprompt=use_autoprompt, include_domains=include_domains, type=type)
        except Exception as e:
            set_api_key_unavaiable(self._api_key, CLIENT_TYPE)
            logger.error(f'metaphor search error: {str(e)}')
        return search_result

    async def exa_get_contents(self, ids):
        aget_contents_of_metaphor = sync_to_async(self._client.get_contents)
        content = ''
        try:
            search_contents = await aget_contents_of_metaphor(ids)
            content = self.format_contents(search_contents.contents)
        except Exception as e:
            set_api_key_unavaiable(self._api_key, CLIENT_TYPE)
            logger.error(f'metaphor get content error: {str(e)}')
        return content

    def format_contents(self, contents):
        formatted_string = ''
        for index, news_item in enumerate(contents):
            formatted_string += f"{news_item.extract}\n引用地址: {news_item.url}\n"
        return formatted_string