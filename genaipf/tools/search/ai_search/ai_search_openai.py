#!/usr/bin/env python3
"""
智能搜索研究助手 - 高并发优化版（增强版）
功能：基于聊天记录生成研究问题，并使用OpenAI Responses API的Web Search功能进行并发搜索
增强：添加专门的虚拟货币实时价格查询功能
优化：全异步实现、连接池复用、速率限制、并发控制
"""

import os
import json
import asyncio
from typing import List, Dict, Any, Optional, ClassVar, Set
from dataclasses import dataclass, field
from dotenv import load_dotenv
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI
import logging
from datetime import datetime, timezone
# from genaipf.dispatcher.utils import ANTHROPIC_API_KEY, OPENAI_API_KEY
import time
from aiolimiter import AsyncLimiter
from contextlib import asynccontextmanager
import aiohttp
import re
import genaipf.utils.common_utils as common_utils

# 加载环境变量
load_dotenv()
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 加密货币配置
CRYPTO_PRICE_API_URL = "https://api.coingecko.com/api/v3"
# 常见加密货币映射（符号到CoinGecko ID）
CRYPTO_MAPPING = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'BNB': 'binancecoin',
    'XRP': 'ripple',
    'ADA': 'cardano',
    'DOGE': 'dogecoin',
    'SOL': 'solana',
    'DOT': 'polkadot',
    'MATIC': 'matic-network',
    'SHIB': 'shiba-inu',
    'TRX': 'tron',
    'AVAX': 'avalanche-2',
    'ATOM': 'cosmos',
    'LTC': 'litecoin',
    'LINK': 'chainlink',
    'BCH': 'bitcoin-cash',
    'NEAR': 'near',
    'UNI': 'uniswap',
    'XLM': 'stellar',
    'ALGO': 'algorand',
    'ICP': 'internet-computer',
    'VET': 'vechain',
    'FIL': 'filecoin',
    'HBAR': 'hedera-hashgraph',
    'MANA': 'decentraland',
    'SAND': 'the-sandbox',
    'AXS': 'axie-infinity',
    'THETA': 'theta-token',
    'EGLD': 'elrond-erd-2',
    'XTZ': 'tezos',
    'FLOW': 'flow',
    'GALA': 'gala',
    'CHZ': 'chiliz',
    'KCS': 'kucoin-shares',
    'CAKE': 'pancakeswap-token',
    'HNT': 'helium',
    'MINA': 'mina-protocol',
    'KLAY': 'klay-token',
    'FTM': 'fantom',
    'ZEC': 'zcash',
    'NEO': 'neo',
    'ENJ': 'enjincoin',
    'BAT': 'basic-attention-token',
    'DASH': 'dash',
    'WAVES': 'waves',
    'XEM': 'nem',
    'HOT': 'holotoken',
    'ZIL': 'zilliqa',
    'COMP': 'compound-governance-token',
    'YFI': 'yearn-finance',
    'SUSHI': 'sushi',
    'SNX': 'synthetix-network-token',
    'QTUM': 'qtum',
    'OMG': 'omisego',
    'ANKR': 'ankr',
    'BNT': 'bancor',
    'ICX': 'icon',
    'SC': 'siacoin',
    'ONT': 'ontology',
    'ZRX': '0x',
    'NANO': 'nano',
    'DGB': 'digibyte',
    'RVN': 'ravencoin',
    'WAN': 'wanchain',
    'STORJ': 'storj',
    'SRM': 'serum',
    'KNC': 'kyber-network-crystal',
    'LRC': 'loopring',
    'BAND': 'band-protocol',
    'REN': 'republic-protocol',
    'OCEAN': 'ocean-protocol',
    'NMR': 'numeraire',
    'BAL': 'balancer',
    'CVC': 'civic',
    'ALPHA': 'alpha-finance',
    'DYDX': 'dydx',
    'GNO': 'gnosis',
    'NU': 'nucypher',
    'FET': 'fetch-ai',
    'CELR': 'celer-network',
    'OGN': 'origin-protocol',
    'NKN': 'nkn',
    'UMA': 'uma',
    'BADGER': 'badger-dao',
    'RARI': 'rarible',
    'MLN': 'melon',
    'PERP': 'perpetual-protocol',
    'SUPER': 'superfarm',
    'ALCX': 'alchemix',
    'TRIBE': 'tribe-2',
    'API3': 'api3',
    'POND': 'marlin',
    'MASK': 'mask-network',
    'LPT': 'livepeer',
    'POLY': 'polymath',
    'INJ': 'injective-protocol',
    'REQ': 'request-network',
    'TRB': 'tellor',
    'PLA': 'playdapp',
    'CTSI': 'cartesi',
    'QUICK': 'quickswap',
    'AMP': 'amp-token',
    'ACH': 'alchemy-pay',
    'CLV': 'clover-finance',
    'GTC': 'gitcoin',
    'FORTH': 'ampleforth-governance-token',
    'RAD': 'radicle',
    'RARE': 'superrare',
    'XYO': 'xyo-network',
    'DIA': 'dia-data',
    'FARM': 'harvest-finance',
    'RLY': 'rally-2',
    'AUCTION': 'auction',
    'WAXP': 'wax',
    'BICO': 'biconomy',
    'GODS': 'gods-unchained',
    'IMX': 'immutable-x',
    'MCO2': 'moss-carbon-credit',
    'GYEN': 'gyen',
    'POWR': 'power-ledger',
    'JASMY': 'jasmycoin',
    'ATA': 'automata',
    'SPELL': 'spell-token',
    'ENS': 'ethereum-name-service',
    'DDX': 'derivadao',
    'FX': 'fx-coin',
    'UNFI': 'unifi-protocol-dao',
    'RAI': 'rai',
    'IDEX': 'aurora-dao',
    'LCX': 'lcx',
    'RGT': 'rari-governance-token',
    'XNO': 'nano',
    'AGLD': 'adventure-gold',
    'FIS': 'stafi',
    'SYN': 'synapse-2',
    'AIOZ': 'aioz-network',
    'AUDIO': 'audius',
    'C98': 'coin98',
    'DESO': 'decentralized-social',
    'HIGH': 'highstreet',
    'RNDR': 'render-token',
    'VOXEL': 'voxies',
    'POLS': 'polkastarter',
    'LOKA': 'league-of-kingdoms',
    'AERGO': 'aergo',
    'INDEX': 'index-cooperative',
    'ASM': 'assemble-protocol',
    'ALICE': 'my-neighbor-alice',
    'BOBA': 'boba-network',
    'SPA': 'sperax',
    'COTI': 'coti',
    'GAL': 'project-galaxy',
    'OOKI': 'ooki',
    'TIME': 'chronobank',
    'AURORA': 'aurora-near',
    'MAGIC': 'magic',
    'HIFI': 'hifi-finance',
    'OP': 'optimism',
    'GMT': 'stepn',
    'GST': 'green-satoshi-token',
    'APE': 'apecoin',
    'STG': 'stargate-finance',
    'LIDO': 'lido-dao',
    'PEOPLE': 'constitutiondao',
    'PSG': 'paris-saint-germain-fan-token',
    'PORTO': 'fc-porto-fan-token',
    'LAZIO': 'lazio-fan-token',
    'SANTOS': 'santos-fc-fan-token',
    'ALPINE': 'alpine-f1-team-fan-token',
    'ACM': 'ac-milan-fan-token',
    'INTER': 'inter-milan-fan-token',
    'CITY': 'manchester-city-fan-token',
    'OG': 'og-fan-token',
    'ARG': 'argentine-football-association-fan-token',
    'BAR': 'fc-barcelona-fan-token',
    'GAL': 'galatasaray-fan-token',
    'ROSE': 'rose-finance',
    'JUV': 'juventus-fan-token',
    'ASR': 'as-roma-fan-token',
    'ATM': 'atletico-madrid-fan-token',
    'APT': 'aptos',
    'QNT': 'quant-network',
    'OSMO': 'osmosis',
    'JUNO': 'juno-network',
    'EVMOS': 'evmos',
    'KAVA': 'kava',
    'KDA': 'kadena',
    'KSM': 'kusama',
    'ZEN': 'horizen',
    'FLUX': 'zelcash',
    'XDC': 'xdce-crowd-sale',
    'METIS': 'metis-token',
    'CVX': 'convex-finance',
    'SUKU': 'suku',
    'MULTI': 'multichain',
    'JOE': 'joe',
    'RPL': 'rocket-pool',
    'NYM': 'nym',
    'VELO': 'velo',
    'DUSK': 'dusk-network',
    'EPX': 'ellipsis-x',
    'PUNDIX': 'pundi-x-2',
    'MX': 'mx-token',
    'DHX': 'datahighway',
    'NEXO': 'nexo',
    'CEL': 'celsius-degree-token',
    'FIDA': 'bonfida',
    'MAPS': 'maps',
    'BETA': 'beta-finance',
    'TROY': 'troy',
    'QI': 'benqi',
    'KP3R': 'keep3rv1',
    'ADX': 'adex',
    'GHST': 'aavegotchi',
    'XPRT': 'persistence',
    'ALPACA': 'alpaca-finance',
    'DODO': 'dodo',
    'TORN': 'tornado-cash',
    'BEL': 'bella-protocol',
    'RUNE': 'thorchain',
    'WING': 'wing-finance',
    'CREAM': 'cream-finance',
    'RSR': 'reserve-rights-token',
    'PAXG': 'pax-gold',
    'EWT': 'energy-web-token',
    'ALEPH': 'aleph-im',
    'ARDR': 'ardor',
    'STRAX': 'stratis',
    'ARK': 'ark',
    'DREP': 'drep-new',
    'PHALA': 'pha',
    'LIT': 'litentry',
    'MDA': 'moeda-loyalty-points',
    'MOB': 'mobilecoin',
    'GLMR': 'moonbeam',
    'MOVR': 'moonriver',
    'REI': 'rei-network',
    'CELO': 'celo',
    'CUSD': 'celo-dollar',
    'REEF': 'reef-finance',
    'GNT': 'golem',
    'ACA': 'acala',
    'ASTR': 'astar',
    'BTTC': 'bittorrent-chain',
    'KLV': 'klever',
    'SYS': 'syscoin',
    'MC': 'merit-circle',
    'LOOKS': 'looksrare',
    'UOS': 'ultra',
    'DVI': 'dvision-network',
    'XMON': 'xmon',
    'TWT': 'trust-wallet-token',
    'IOTX': 'iotex',
    'TFUEL': 'theta-fuel',
    'NXM': 'nxm',
    'GXS': 'gxchain',
    'REV': 'revain',
    'FOR': 'force-protocol',
    'RAMP': 'ramp',
    'AKRO': 'akropolis',
    'PHA': 'pha',
    'DATA': 'streamr',
    'XPLA': 'xpla',
    'MBL': 'moviebloc',
    'BLOK': 'bloktopia',
    'UFO': 'ufo-gaming',
    'MBOX': 'mobox',
    'VRA': 'verasity',
    'DEGO': 'dego-finance',
    'IRIS': 'iris-network',
    'LSS': 'lossless',
    'FRONT': 'frontier-token',
    'PROM': 'prometeus',
    'VGX': 'voyager-token',
    'WOZX': 'wozx',
    'NULS': 'nuls',
    'HARD': 'hard-protocol',
    'STEEM': 'steem',
    'PHB': 'phoenix-global',
    'TKO': 'tokocrypto',
    'GTO': 'gifto',
    'EPS': 'ellipsis',
    'ARPA': 'arpa-chain',
    'WNXM': 'wrapped-nxm',
    'MTL': 'metal',
    'OAX': 'oax',
    'SUN': 'sun-token',
    'LON': 'tokenlon',
    'JST': 'just',
    'WRX': 'wazirx',
    'BLZ': 'bluzelle',
    'IRIS': 'iris-network',
    'ORN': 'orion-protocol',
    'UTK': 'utrust',
    'ALPHA': 'alpha-venture-dao',
    'VIDT': 'vidt-datalink',
    'AION': 'aion',
    'COS': 'contentos',
    'CTXC': 'cortex',
    'STPT': 'standard-tokenization-protocol',
    'MFT': 'mainframe',
    'KEY': 'selfkey',
    'PERL': 'perlin',
    'NBS': 'new-bitshares',
    'FIO': 'fio-protocol',
    'DENT': 'dent',
    'AGIX': 'singularitynet',
    'OCEAN': 'ocean-protocol',
    'NMRKR': 'newmaker',
    'TCT': 'tokenclub',
    'BEAM': 'beam',
    'PIVX': 'pivx',
    'XVG': 'verge',
    'MAID': 'maidsafecoin',
    'STRAT': 'stratis',
    'PAX': 'paxos-standard',
    'FUNFAIR': 'funfair',
    'GRS': 'groestlcoin',
    'LSK': 'lisk',
    'ADK': 'aidos-kuneen',
    'DMD': 'diamond',
    'OK': 'okcash',
    'PART': 'particl',
    'ARQ': 'arqma',
    'GBYTE': 'byteball',
    'PPC': 'peercoin',
    'VTC': 'vertcoin',
    'NAV': 'nav-coin',
    'SMART': 'smartcash',
    'XZC': 'zcoin',
    'BLOCK': 'blocknet',
    'DCR': 'decred',
    'SAFEMOON': 'safemoon',
    'VLX': 'velas',
    'HEX': 'hex',
    'XVS': 'venus',
    'NRV': 'nerve-finance',
    'BDO': 'bdollar',
    'MIR': 'mirror-protocol',
    'LDO': 'lido-dao',
    'PAXG': 'pax-gold',
    'HUSD': 'husd',
    'FXS': 'frax-share',
    'TRIBE': 'tribe-2',
    'RAY': 'raydium',
    'MINA': 'mina-protocol',
    'COPE': 'cope',
    'FTT': 'ftx-token',
    'SBR': 'saber',
    'KIN': 'kin',
    'FIDA': 'bonfida',
    'STEP': 'step-finance',
    'MEDIA': 'media-network',
    'LIKE': 'only1',
    'ORCA': 'orca',
    'MNGO': 'mango-markets',
    'OXY': 'oxygen',
}

@dataclass
class Question:
    """问题数据结构"""
    main_question: str
    sub_questions: List[str] = field(default_factory=list)
    time_requirement: str = "最新"
    full_question: str = ""
    search_context_size: str = "high"  # high, medium, low
    is_crypto_price: bool = False  # 新增：标识是否为加密货币价格查询
    crypto_symbols: List[str] = field(default_factory=list)  # 新增：需要查询的加密货币符号
    
    def __post_init__(self):
        if not self.full_question:
            self.full_question = self._generate_full_question()
    
    def _generate_full_question(self) -> str:
        """生成完整的问题描述"""
        parts = [self.main_question]
        if self.sub_questions:
            parts.append("\n具体包括：")
            parts.extend(f"- {sq}" for sq in self.sub_questions)
        return "\n".join(parts)

@dataclass
class SearchResult:
    """搜索结果数据结构"""
    question: Question
    answer: str = ""
    success: bool = True
    error: Optional[str] = None
    search_time: float = 0.0

class CryptoPriceService:
    """加密货币价格服务 - 高并发优化版"""
    
    def __init__(self):
        """初始化价格服务"""
        self.base_url = CRYPTO_PRICE_API_URL
        self._session: Optional[aiohttp.ClientSession] = None
        self._session_lock = asyncio.Lock()
        self._limiter = AsyncLimiter(10, 60)  # CoinGecko免费版限制：10次/分钟
        
        # 缓存配置
        self._price_cache: Dict[str, Dict[str, Any]] = {}
        self._cache_ttl = 30  # 缓存30秒
        
        # 批量查询优化
        self._pending_queries: Dict[str, asyncio.Future] = {}
        self._batch_lock = asyncio.Lock()
        
        # 连接池配置
        self._connector = None
        self._max_connections = 10
        
        logger.info("加密货币价格服务初始化（高并发版）")
    
    async def _ensure_session(self):
        """确保会话存在（线程安全）"""
        if self._session is None or self._session.closed:
            async with self._session_lock:
                # 双重检查锁定
                if self._session is None or self._session.closed:
                    # 配置连接池
                    if self._connector is None:
                        self._connector = aiohttp.TCPConnector(
                            limit=self._max_connections,
                            limit_per_host=self._max_connections,
                            ttl_dns_cache=300
                        )
                    
                    timeout = aiohttp.ClientTimeout(total=30, connect=10)
                    self._session = aiohttp.ClientSession(
                        connector=self._connector,
                        timeout=timeout
                    )
    
    async def close(self):
        """关闭会话和连接器"""
        if self._session and not self._session.closed:
            await self._session.close()
        if self._connector:
            await self._connector.close()
    
    def _normalize_symbol(self, symbol: str) -> Optional[str]:
        """标准化加密货币符号"""
        symbol = symbol.upper().strip()
        # 移除常见的后缀
        for suffix in ['USDT', 'USD', 'BUSD', 'USDC']:
            if symbol.endswith(suffix) and len(symbol) > len(suffix):
                symbol = symbol[:-len(suffix)]
        
        return CRYPTO_MAPPING.get(symbol)
    
    def _is_cache_valid(self, cache_entry: Dict[str, Any]) -> bool:
        """检查缓存是否有效"""
        if not cache_entry:
            return False
        
        cache_time = cache_entry.get('cache_time', 0)
        return (time.time() - cache_time) < self._cache_ttl
    
    async def get_price(self, symbols: List[str]) -> Dict[str, Any]:
        """获取加密货币价格（支持缓存和批量优化）"""
        await self._ensure_session()
        
        # 标准化并过滤符号
        coin_ids = []
        symbol_to_id = {}
        cached_results = {}
        symbols_to_fetch = []
        
        for symbol in symbols:
            symbol_upper = symbol.upper()
            coin_id = self._normalize_symbol(symbol)
            
            if not coin_id:
                logger.warning(f"未找到加密货币符号映射: {symbol}")
                continue
            
            # 检查缓存
            cache_key = f"{coin_id}_price"
            if cache_key in self._price_cache and self._is_cache_valid(self._price_cache[cache_key]):
                cached_results[symbol_upper] = self._price_cache[cache_key]['data']
                logger.info(f"使用缓存价格: {symbol_upper}")
            else:
                coin_ids.append(coin_id)
                symbol_to_id[symbol_upper] = coin_id
                symbols_to_fetch.append(symbol_upper)
        
        # 如果所有数据都在缓存中，直接返回
        if not coin_ids:
            if cached_results:
                return cached_results
            else:
                return {"error": "没有找到有效的加密货币符号"}
        
        # 去重
        coin_ids = list(set(coin_ids))
        
        # 批量查询优化：合并同时发生的相同查询
        query_key = ','.join(sorted(coin_ids))
        
        async with self._batch_lock:
            # 检查是否有相同的查询正在进行
            if query_key in self._pending_queries:
                logger.info(f"等待已有的批量查询: {query_key[:50]}...")
                try:
                    result = await self._pending_queries[query_key]
                    # 合并缓存结果
                    for symbol_upper in symbols_to_fetch:
                        if symbol_upper in result:
                            cached_results[symbol_upper] = result[symbol_upper]
                    return cached_results
                except Exception:
                    # 如果等待的查询失败，继续执行新查询
                    pass
            
            # 创建新的查询Future
            future = asyncio.Future()
            self._pending_queries[query_key] = future
        
        try:
            # 使用重试机制
            max_retries = 3
            retry_delay = 1
            
            for attempt in range(max_retries):
                try:
                    async with self._limiter:
                        params = {
                            'ids': ','.join(coin_ids),
                            'vs_currencies': 'usd,cny',
                            'include_24hr_vol': 'true',
                            'include_24hr_change': 'true',
                            'include_last_updated_at': 'true'
                        }
                        
                        async with self._session.get(
                            f"{self.base_url}/simple/price",
                            params=params
                        ) as response:
                            if response.status == 200:
                                data = await response.json()
                                
                                # 转换回符号格式并更新缓存
                                result = {}
                                current_time = time.time()
                                
                                for symbol, coin_id in symbol_to_id.items():
                                    if coin_id in data:
                                        result[symbol] = data[coin_id]
                                        # 更新缓存
                                        cache_key = f"{coin_id}_price"
                                        self._price_cache[cache_key] = {
                                            'data': data[coin_id],
                                            'cache_time': current_time
                                        }
                                
                                # 合并缓存结果
                                result.update(cached_results)
                                
                                # 通知等待的请求
                                future.set_result(result)
                                return result
                                
                            elif response.status == 429:  # Rate limit
                                if attempt < max_retries - 1:
                                    await asyncio.sleep(retry_delay * (attempt + 1))
                                    continue
                                else:
                                    error = "API速率限制，请稍后重试"
                            else:
                                error_text = await response.text()
                                error = f"API错误: {response.status} - {error_text}"
                            
                            future.set_exception(Exception(error))
                            return {"error": error}
                                
                except asyncio.TimeoutError:
                    if attempt < max_retries - 1:
                        await asyncio.sleep(retry_delay)
                        continue
                    error = "请求超时"
                    future.set_exception(Exception(error))
                    return {"error": error}
                except aiohttp.ClientError as e:
                    if attempt < max_retries - 1:
                        await asyncio.sleep(retry_delay)
                        continue
                    error = f"网络错误: {str(e)}"
                    future.set_exception(Exception(error))
                    return {"error": error}
                    
        except Exception as e:
            logger.error(f"获取价格时出错: {str(e)}")
            future.set_exception(e)
            return {"error": str(e)}
        finally:
            # 清理pending查询
            async with self._batch_lock:
                self._pending_queries.pop(query_key, None)
    
    def format_price_result(self, prices: Dict[str, Any], symbols: List[str]) -> str:
        """格式化价格结果"""
        if "error" in prices:
            return f"❌ 获取价格失败: {prices['error']}"
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        lines = [f"💰 加密货币实时价格（更新时间: {current_time}）\n"]
        
        for symbol in symbols:
            symbol_upper = symbol.upper()
            if symbol_upper in prices:
                price_data = prices[symbol_upper]
                usd_price = price_data.get('usd', 0)
                cny_price = price_data.get('cny', 0)
                change_24h = price_data.get('usd_24h_change', 0)
                volume_24h = price_data.get('usd_24h_vol', 0)
                
                # 价格变化指示器
                change_indicator = "📈" if change_24h > 0 else "📉" if change_24h < 0 else "➡️"
                
                lines.append(f"\n{symbol_upper}:")
                lines.append(f"  💵 USD: ${usd_price:,.2f}")
                lines.append(f"  💴 CNY: ¥{cny_price:,.2f}")
                lines.append(f"  {change_indicator} 24h变化: {change_24h:+.2f}%")
                lines.append(f"  📊 24h交易量: ${volume_24h:,.0f}")
                
                # 更新时间
                last_updated = price_data.get('last_updated_at', 0)
                if last_updated:
                    update_time = datetime.fromtimestamp(last_updated).strftime('%H:%M:%S')
                    lines.append(f"  🕐 最后更新: {update_time}")
            else:
                lines.append(f"\n{symbol_upper}: ⚠️ 未找到价格数据")
        
        lines.append("\n✅ 数据来源: CoinGecko API (实时数据)")
        return '\n'.join(lines)

class APIClientManager:
    """全局API客户端管理器 - 单例模式（高并发优化）"""
    _instance: ClassVar[Optional['APIClientManager']] = None
    _lock: ClassVar[asyncio.Lock] = asyncio.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._claude_client: Optional[AsyncAnthropic] = None
            self._openai_client: Optional[AsyncOpenAI] = None
            self._crypto_service: Optional[CryptoPriceService] = None
            
            # 速率限制器
            # Claude: 根据官方限制，假设每分钟50个请求
            self._claude_limiter = AsyncLimiter(50, 60)
            # OpenAI: 根据官方限制，假设每分钟100个请求
            self._openai_limiter = AsyncLimiter(100, 60)
            
            # 并发控制信号量
            self._claude_semaphore = asyncio.Semaphore(10)  # 最多10个并发Claude请求
            self._openai_semaphore = asyncio.Semaphore(20)  # 最多20个并发OpenAI请求
            
            # 服务创建锁
            self._service_locks = {
                'claude': asyncio.Lock(),
                'openai': asyncio.Lock(),
                'crypto': asyncio.Lock()
            }
    
    async def get_claude_client(self) -> AsyncAnthropic:
        """获取Claude客户端（异步版本）"""
        if self._claude_client is None:
            async with self._service_locks['claude']:
                if self._claude_client is None:
                    api_key = ANTHROPIC_API_KEY
                    if not api_key:
                        raise ValueError("ANTHROPIC_API_KEY未在环境变量中找到")
                    self._claude_client = AsyncAnthropic(api_key=api_key)
        return self._claude_client
    
    async def get_openai_client(self) -> AsyncOpenAI:
        """获取OpenAI客户端（异步版本）"""
        if self._openai_client is None:
            async with self._service_locks['openai']:
                if self._openai_client is None:
                    api_key = OPENAI_API_KEY
                    if not api_key:
                        raise ValueError("OPENAI_API_KEY未在环境变量中找到")
                    self._openai_client = AsyncOpenAI(api_key=api_key)
        return self._openai_client
    
    async def get_crypto_service(self) -> CryptoPriceService:
        """获取加密货币价格服务（异步版本）"""
        if self._crypto_service is None:
            async with self._service_locks['crypto']:
                if self._crypto_service is None:
                    self._crypto_service = CryptoPriceService()
        return self._crypto_service
    
    # 保留同步property以便向后兼容，但建议使用异步方法
    @property
    def claude_client(self) -> AsyncAnthropic:
        """获取Claude客户端（同步版本，不推荐）"""
        if self._claude_client is None:
            api_key = ANTHROPIC_API_KEY
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY未在环境变量中找到")
            self._claude_client = AsyncAnthropic(api_key=api_key)
        return self._claude_client
    
    @property
    def openai_client(self) -> AsyncOpenAI:
        """获取OpenAI客户端（同步版本，不推荐）"""
        if self._openai_client is None:
            api_key = OPENAI_API_KEY
            if not api_key:
                raise ValueError("OPENAI_API_KEY未在环境变量中找到")
            self._openai_client = AsyncOpenAI(api_key=api_key)
        return self._openai_client
    
    @property
    def crypto_service(self) -> CryptoPriceService:
        """获取加密货币价格服务（同步版本，不推荐）"""
        if self._crypto_service is None:
            self._crypto_service = CryptoPriceService()
        return self._crypto_service
    
    @asynccontextmanager
    async def claude_rate_limit(self):
        """Claude API速率限制上下文管理器"""
        async with self._claude_semaphore:
            async with self._claude_limiter:
                yield
    
    @asynccontextmanager
    async def openai_rate_limit(self):
        """OpenAI API速率限制上下文管理器"""
        async with self._openai_semaphore:
            async with self._openai_limiter:
                yield
    
    async def close(self):
        """关闭所有客户端连接"""
        if self._claude_client:
            await self._claude_client.close()
        if self._openai_client:
            await self._openai_client.close()
        if self._crypto_service:
            await self._crypto_service.close()

class ResearchAssistant:
    """研究助手主类 - 高并发优化版"""
    
    def __init__(self):
        """初始化研究助手"""
        # 使用全局客户端管理器
        self.client_manager = APIClientManager()
        
        # 确保设置全局管理器引用
        global _global_client_manager
        _global_client_manager = self.client_manager
        
        # 设置时区
        self.timezone = os.getenv('TIMEZONE', 'UTC')
        
        # 用于控制整体并发的信号量（避免同时处理过多用户请求）
        self._user_request_semaphore = asyncio.Semaphore(30)  # 最多同时处理30个用户请求
        
        logger.info("研究助手初始化成功（高并发版）")
    
    def get_current_time(self) -> Dict[str, str]:
        """获取当前时间信息"""
        now = datetime.now()
        return {
            'datetime': now.strftime('%Y-%m-%d %H:%M:%S'),
            'date': now.strftime('%Y-%m-%d'),
            'year': str(now.year),
            'month': str(now.month),
            'day': str(now.day),
            'hour': str(now.hour),
            'minute': str(now.minute),
            'month_name': now.strftime('%B'),
            'weekday': now.strftime('%A'),
            'timestamp': int(time.time())
        }
    
    def _extract_crypto_symbols(self, text: str) -> List[str]:
        """从文本中提取加密货币符号"""
        # 常见的加密货币模式
        patterns = [
            r'\b([A-Z]{2,10})(?:/USDT?|/USD|/BUSD|/USDC)?\b',  # BTC/USDT, ETH/USD等
            r'\$([A-Z]{2,10})\b',  # $BTC, $ETH等
            r'\b([A-Z]{2,10})(?=\s*(?:价格|price|币|coin|token))',  # BTC价格，ETH币等
        ]
        
        symbols = set()
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                symbol = match.upper()
                if symbol in CRYPTO_MAPPING:
                    symbols.add(symbol)
        
        # 特殊处理一些中文名称
        chinese_names = {
            '比特币': 'BTC',
            '以太坊': 'ETH',
            '币安币': 'BNB',
            '瑞波币': 'XRP',
            '狗狗币': 'DOGE',
            '柴犬币': 'SHIB',
            '波卡': 'DOT',
            '艾达币': 'ADA',
            'Solana': 'SOL',
            '雪崩': 'AVAX',
            '马蒂克': 'MATIC',
        }
        
        for chinese, symbol in chinese_names.items():
            if chinese in text:
                symbols.add(symbol)
        
        return list(symbols)
    
    def _is_price_query(self, question: str) -> bool:
        """判断是否为价格查询"""
        price_keywords = [
            '价格', 'price', '多少钱', '报价', '实时价', '现价',
            '最新价', '当前价', '市价', 'quote', '行情',
            '涨跌', '涨幅', '跌幅', '变化', 'change',
            '值多少', 'worth', 'value', '估值'
        ]
        
        return any(keyword in question.lower() for keyword in price_keywords)
    
    async def generate_research_questions(self, chat_history: str) -> List[Question]:
        """使用Claude生成需要研究的问题（异步版）"""
        current_time = self.get_current_time()
        
        prompt = f"""
当前时间：{current_time['datetime']} 时区为：{self.timezone}（请基于当前时间对问题的时效性作出明确要求）

基于以下用户和chatbot的聊天记录，把用户根本需求拆解，分成子问题并通过网络搜索解决子问题，从而能精准解决用户需求。

聊天记录：
{chat_history}

重要提示：
1. 所有问题必须基于当前时间：{current_time['datetime']}，时区为：{self.timezone}来生成
2. 如果用户询问"最近"、"当前"、"现在"等信息，要查询当前时间：{current_time['datetime']}，时区为：{self.timezone}下的最新情况，根据情况增强实效性
3. 不要生成关于过去年份的问题，除非用户明确要求历史数据对比
4. 对于投资、市场、技术等快速变化的领域，只关注最近的信息
5. **重要**：如果用户询问任何加密货币的价格、行情、涨跌等信息，必须设置 is_crypto_price 为 true，并在 crypto_symbols 中列出需要查询的货币符号

要求：
1. 智能分析用户需求的复杂度（根据问题难度判断需要搜索的主题数量）：
   - 简单查询（如天气、股价、币价）：生成1个精准问题主题
   - 中等复杂度（如产品比较、新闻事件）：生成2-3个相关问题主题
   - 高复杂度（如市场分析、技术研究）：生成3-5个深度问题主题

2. 问题设计原则：
   - 每个问题主题必须明确包含时间范围（如：2025年6月、本周、过去7天、本日、一小时内、实时等）
   - 避免过于宽泛或抽象的问题
   - 确保全部问题主题以及具体子问题之间有逻辑关联但查询内容不重复。
   - **关键**：对于任何涉及虚拟币价格、行情、涨跌的查询，必须设置为专门的价格查询问题，并标记 is_crypto_price 为 true
   - 对于复杂问题主题，可将大问题进一步细化为1-3个具体子问题

3. 时效性要求分类：
   - 实时数据：股价、汇率、天气等（标记为"实时"）
   - 近期信息：新闻、事件、趋势等（标记为"24小时内"、"本周"或"本月"）
   - 相对稳定：技术文档、历史事件等（标记为"最新"）

4. 搜索深度建议：
   - 简单事实查询：low
   - 需要对比分析：medium
   - 需要深度研究：high

5. **加密货币价格识别**：
   - 如果问题涉及任何加密货币的价格、行情、涨跌等，必须设置 is_crypto_price: true
   - 在 crypto_symbols 中列出所有需要查询的货币符号（如 ["BTC", "ETH"]）
   - 价格查询应该作为独立的问题，不要与其他分析混合

请以以下JSON格式输出：
```json
[
    {{
        "main_question": "核心问题主题（必须包含明确的时间范围以及标出当前时间）",
        "sub_questions": ["具体子问题1", "具体子问题2"],
        "time_requirement": "时效性要求（如：实时、24小时内、本周、本月）",
        "search_context_size": "搜索深度（high/medium/low）",
        "full_question": "包含所有细节和时间范围的完整问题描述",
        "is_crypto_price": false,  // 是否为加密货币价格查询
        "crypto_symbols": []  // 需要查询的加密货币符号，如 ["BTC", "ETH"]
    }}
]
```

"""
        
        try:
            # 使用速率限制
            async with self.client_manager.claude_rate_limit():
                claude_client = await self.client_manager.get_claude_client()
                response = await claude_client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=2000,
                    temperature=0.3,
                    messages=[{"role": "user", "content": prompt}]
                )
            
            content = response.content[0].text
            
            # 提取JSON
            start_idx = content.find('[')
            end_idx = content.rfind(']') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                questions_data = json.loads(json_str)
                
                questions = []
                for q_data in questions_data:
                    # 额外检查是否为价格查询（双重保险）
                    is_crypto_price = q_data.get('is_crypto_price', False)
                    crypto_symbols = q_data.get('crypto_symbols', [])
                    
                    # 如果Claude没有正确识别，我们再次检查
                    if not is_crypto_price and self._is_price_query(q_data['main_question']):
                        extracted_symbols = self._extract_crypto_symbols(q_data['main_question'])
                        if extracted_symbols:
                            is_crypto_price = True
                            crypto_symbols = extracted_symbols
                    
                    question = Question(
                        main_question=q_data['main_question'],
                        sub_questions=q_data.get('sub_questions', []),
                        time_requirement=q_data.get('time_requirement', '最新'),
                        search_context_size=q_data.get('search_context_size', 'high'),
                        full_question=q_data.get('full_question', ''),
                        is_crypto_price=is_crypto_price,
                        crypto_symbols=crypto_symbols
                    )
                    questions.append(question)
                
                logger.info(f"成功生成{len(questions)}个研究问题")
                return questions
            else:
                raise ValueError("无法解析Claude响应中的JSON")
                
        except Exception as e:
            logger.error(f"生成问题时出错: {str(e)}")
            # 返回默认问题
            return [Question(
                main_question="基于聊天记录的相关信息查询",
                time_requirement="最新",
                search_context_size="medium"
            )]
    
    async def search_single_question(self, question: Question) -> SearchResult:
        """使用OpenAI Responses API的Web Search功能搜索单个问题（异步版）"""
        start_time = time.time()
        
        try:
            # 如果是加密货币价格查询，使用专门的价格服务
            if question.is_crypto_price and question.crypto_symbols:
                logger.info(f"使用加密货币价格服务查询: {question.crypto_symbols}")
                
                # 获取价格
                crypto_service = await self.client_manager.get_crypto_service()
                prices = await crypto_service.get_price(question.crypto_symbols)
                
                # 格式化结果
                answer = crypto_service.format_price_result(
                    prices, 
                    question.crypto_symbols
                )
                
                search_time = time.time() - start_time
                logger.info(f"价格查询完成，耗时: {search_time:.2f}秒")
                
                return SearchResult(
                    question=question,
                    answer=answer,
                    success=True,
                    search_time=search_time
                )
            
            # 否则使用原有的OpenAI搜索
            current_time = self.get_current_time()
            
            # 计算上个月
            current_month_int = int(current_time['month'])
            current_year_int = int(current_time['year'])
            previous_month = current_month_int - 1 if current_month_int > 1 else 12
            previous_year = current_year_int if current_month_int > 1 else current_year_int - 1
            
            # 构建增强的搜索查询
            search_prompt = f"""
当前精确时间：{current_time['datetime']} {self.timezone}
今天是：{current_time['year']}年{current_time['month']}月{current_time['day']}日 {current_time['weekday']} {current_time['hour']}时{current_time['minute']}分

请搜索以下问题的答案：

{question.full_question}

⏰ 时效性要求：{question.time_requirement}

🔍 搜索及时性要求（重要）：
1. **实时数据类**（股价、汇率、指数）：
   - 必须是{current_time['year']}年{current_time['month']}月{current_time['day']}日{current_time['hour']}时{current_time['minute']}分前后10分钟内的数据
   - 优先查找主要交易所/官方数据源的实时报价
   - 如果数据超过30分钟，明确标注"数据可能已过时"
   - 不要采用新闻媒体文章内包含的过时价格信息

2. **突发新闻类**（新闻事件、公告、突发消息）：
   - 优先搜索{current_time['year']}年{current_time['month']}月{current_time['day']}日发布的信息
   - 如果是{current_time['day']}日之前的消息，必须明确标注发布时间
   - 使用"最新"、"刚刚"、"今日"、"本小时"等关键词强化搜索

3. **技术数据类**（技术指标、链上数据、统计数据）：
   - 搜索{current_time['year']}年{current_time['month']}月{current_time['day']}日的最新技术指标
   - 对于24小时周期数据，确保数据截止时间不早于昨日同一时间

🎯 搜索策略优化：
- 在搜索查询中添加时间限定词："2025年6月23日"、"今日"、"实时"、"live"、"current"、"latest"
- 对于价格查询，使用"real-time price"、"current quote"、"live data"
- 验证数据时间戳，优先选择带有明确更新时间的数据源
- 交叉验证：对比3-4个不同来源的数据确保准确性

📋 答案格式要求：
1. **必须包含数据时间**：明确标注"截至{current_time['year']}年{current_time['month']}月{current_time['day']}日{current_time['hour']}:{current_time['minute']}"
2. **数据新鲜度标识**：
   - 10分钟内：✅ 实时数据
   - 30分钟内：⚡ 较新数据  
   - 1小时内：⏰ 一般数据
   - 超过1小时：⚠️ 可能过时
3. **来源可靠性**：优先引用官方/主流平台数据
4. **简洁精准**：200-300字，聚焦核心问题，避免无关信息延伸

⚠️ 数据质量控制：
- 如果找到的最新数据超过预期时间范围，明确说明时间差距
- 遇到冲突数据时，选择更新时间最近且来源更权威的版本
- 必须在答案开头标注数据获取的具体时间点

请严格按照以上时效性要求进行搜索和信息筛选。
"""
            
            # 使用速率限制
            async with self.client_manager.openai_rate_limit():
                openai_client = await self.client_manager.get_openai_client()
                response = await openai_client.responses.create(
                    model="gpt-5.2",
                    tools=[{
                        "type": "web_search_preview",
                        "search_context_size": question.search_context_size,
                        "user_location": {
                            "type": "approximate", 
                            "timezone": self.timezone
                        }
                    }],
                    input=search_prompt,
                    temperature=0.1
                )
            
            # 提取答案
            answer = response.output_text.strip() if hasattr(response, 'output_text') else str(response)
            
            search_time = time.time() - start_time
            logger.info(f"问题搜索完成，耗时: {search_time:.2f}秒")
            
            return SearchResult(
                question=question,
                answer=answer,
                success=True,
                search_time=search_time
            )
            
        except Exception as e:
            search_time = time.time() - start_time
            logger.error(f"搜索失败: {str(e)}")
            return SearchResult(
                question=question,
                answer="",
                success=False,
                error=str(e),
                search_time=search_time
            )
    
    async def search_questions_concurrently(self, questions: List[Question]) -> List[SearchResult]:
        """并发搜索所有问题（全异步版，带批量价格查询优化）"""
        # 分离价格查询和普通查询，同时记录原始索引
        price_questions_with_idx = []
        regular_questions_with_idx = []
        all_crypto_symbols = set()
        
        for idx, question in enumerate(questions):
            if question.is_crypto_price and question.crypto_symbols:
                price_questions_with_idx.append((idx, question))
                all_crypto_symbols.update(question.crypto_symbols)
            else:
                regular_questions_with_idx.append((idx, question))
        
        # 创建结果数组，预分配空间
        results = [None] * len(questions)
        
        # 如果有价格查询，批量获取所有价格
        if price_questions_with_idx:
            try:
                logger.info(f"批量查询 {len(all_crypto_symbols)} 个加密货币价格")
                crypto_service = await self.client_manager.get_crypto_service()
                batch_prices = await crypto_service.get_price(list(all_crypto_symbols))
                
                # 处理每个价格查询问题
                for idx, question in price_questions_with_idx:
                    # 筛选该问题需要的价格
                    question_prices = {
                        symbol: batch_prices[symbol] 
                        for symbol in question.crypto_symbols 
                        if symbol in batch_prices
                    }
                    
                    # 格式化结果
                    answer = crypto_service.format_price_result(
                        question_prices, 
                        question.crypto_symbols
                    )
                    
                    results[idx] = SearchResult(
                        question=question,
                        answer=answer,
                        success=True,
                        search_time=0.1  # 批量查询，单个时间很短
                    )
            except Exception as e:
                logger.error(f"批量价格查询失败: {str(e)}")
                # 失败时回退到单个查询
                for idx, question in price_questions_with_idx:
                    results[idx] = await self.search_single_question(question)
        
        # 并发处理普通查询
        if regular_questions_with_idx:
            regular_questions = [q for _, q in regular_questions_with_idx]
            regular_tasks = [self.search_single_question(question) for question in regular_questions]
            regular_results = await asyncio.gather(*regular_tasks, return_exceptions=True)
            
            # 将结果放回正确的位置
            for (idx, _), result in zip(regular_questions_with_idx, regular_results):
                if isinstance(result, Exception):
                    logger.error(f"搜索任务失败: {str(result)}")
                    results[idx] = SearchResult(
                        question=questions[idx],
                        success=False,
                        error=str(result)
                    )
                else:
                    results[idx] = result
        
        # 确保所有位置都有结果
        for idx, result in enumerate(results):
            if result is None:
                results[idx] = SearchResult(
                    question=questions[idx],
                    success=False,
                    error="未找到搜索结果"
                )
        
        return results
    
    def format_results(self, results: List[SearchResult], total_time: float = 0) -> str:
        """格式化输出结果"""
        output = []
        output.append("=" * 80)
        output.append(f"📅 搜索时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("=" * 80)
        output.append("")
        
        # 统计信息
        success_count = sum(1 for r in results if r.success)
        output.append(f"📊 搜索相关主题用于回答用户问题：成功 {success_count}/{len(results)} 个问题")
        output.append("")
        ai_source = []
        # 详细结果
        for i, result in enumerate(results, 1):
            output.append(f"【问题 {i}】{result.question.main_question}")
            output.append("-" * 70)
            temp_ai_source = {
                'title': common_utils.filter_brackets(result.question.main_question),
                'href': 'https://www.chatgpt.com/',
                'body': result.answer
            }
            ai_source.append(temp_ai_source)
            # 显示子问题
            if result.question.sub_questions:
                output.append("📌 具体方面：")
                for j, sub_q in enumerate(result.question.sub_questions, 1):
                    output.append(f"   {j}. {sub_q}")
                output.append("")
            
            # 如果是加密货币价格查询，特别标注
            if result.question.is_crypto_price:
                output.append("💰 查询类型：加密货币实时价格")
                output.append("")
            
            # 显示搜索结果
            if result.success:
                output.append("📄 搜索结果：")
                answer_lines = result.answer.split('\n')
                for line in answer_lines:
                    if line.strip():
                        output.append(f"   {line}")
            else:
                output.append(f"❌ 搜索失败：{result.error}")
            
            output.append("")
            output.append("=" * 80)
            output.append("")
        
        return "\n".join(output), ai_source
    
    async def research_async(self, chat_history: str) -> str:
        """异步执行研究流程（核心方法）"""
        # 使用信号量控制并发用户请求数
        async with self._user_request_semaphore:
            total_start_time = time.time()
            
            try:
                # 显示当前时间
                current_time = self.get_current_time()
                logger.info(f"当前时间：{current_time['datetime']}，时区为：{self.timezone}")
                
                # 第一步：生成问题（异步）
                logger.info("开始生成研究问题...")
                questions = await self.generate_research_questions(chat_history)
                logger.info(f"已生成 {len(questions)} 个研究问题")
                
                # 输出识别到的加密货币价格查询
                price_queries = [q for q in questions if q.is_crypto_price]
                if price_queries:
                    logger.info(f"识别到 {len(price_queries)} 个加密货币价格查询")
                    for q in price_queries:
                        logger.info(f"  - 查询货币: {q.crypto_symbols}")
                
                # 第二步：并发搜索（全异步）
                logger.info("开始并发搜索...")
                results = await self.search_questions_concurrently(questions)
                logger.info("搜索完成")
                
                # 计算总耗时
                total_time = time.time() - total_start_time
                
                # 格式化并返回结果
                return self.format_results(results, total_time)
                
            except Exception as e:
                logger.error(f"研究过程出错: {str(e)}")
                return f"研究过程中发生错误：{str(e)}"

# 全局客户端管理器实例（用于清理）
_global_client_manager: Optional[APIClientManager] = None

async def cleanup_clients():
    """清理全局客户端连接"""
    global _global_client_manager
    if _global_client_manager:
        await _global_client_manager.close()

async def ensure_global_manager():
    """确保全局管理器存在"""
    global _global_client_manager
    if _global_client_manager is None:
        _global_client_manager = APIClientManager()
    return _global_client_manager

def main():
    """主函数示例"""
    # 示例聊天记录
    sample_chat_histories = [
        # 简单查询
        "用户：今天有什么币可以买？",
        
        # 中等复杂度 - 加密货币市场（价格查询）
        "用户：BTC和ETH现在的价格是多少？最近涨跌如何？",
        
        # 混合查询 - 包含价格和其他信息
        "用户：我想了解一下Solana生态系统的发展情况，SOL币现在多少钱？有哪些主要的DeFi项目？",
        
        # 股票市场查询
        "用户：科技股最近的表现如何？有哪些值得关注的公司？",
        
        # 高复杂度 - 行业分析
        """用户：我正在考虑投资加密货币，能帮我分析一下：
1. BTC、ETH、BNB的当前价格
2. DeFi领域的最新发展趋势
3. Layer2解决方案的对比
4. 监管政策的最新动态""",
        
        # 纯价格查询 - 测试批量优化
        "用户：查一下BTC、ETH、BNB、ADA、SOL、DOGE、SHIB、MATIC的实时价格",
        
        # 压力测试 - 多个价格查询和普通查询混合
        """用户：请帮我分析：
1. BTC、ETH、SOL的价格和24小时涨跌
2. 最近有什么重要的加密货币新闻
3. DOT、AVAX、NEAR的价格
4. DeFi总锁仓量的变化趋势
5. ATOM、ALGO的价格表现""",
    ]
    
    async def async_main():
        try:
            # 创建研究助手实例
            assistant = ResearchAssistant()
            
            # 显示当前时间
            current_time = assistant.get_current_time()
            print(f"⏰ 系统当前时间：{current_time['datetime']}")
            print(f"📅 日期：{current_time['year']}年{current_time['month']}月{current_time['day']}日 {current_time['weekday']}")
            print("="*80 + "\n")
            
            # 选择一个示例进行测试
            chat_history = sample_chat_histories[0]  # 使用压力测试例子，测试并发性能
            
            print("📝 聊天记录：")
            print(chat_history)
            print("\n" + "="*80 + "\n")
            
            # 执行研究
            result = await assistant.research_async(chat_history)
            
            # 输出结果
            print(result)
            
        except ValueError as e:
            print(f"❌ 配置错误: {str(e)}")
            print("请检查.env文件中的API密钥配置")
        except Exception as e:
            print(f"❌ 程序执行出错: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            # 清理资源
            await cleanup_clients()
    
    # 运行异步主函数
    asyncio.run(async_main())

if __name__ == "__main__":
    main()