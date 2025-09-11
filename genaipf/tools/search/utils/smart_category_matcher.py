import re
from typing import List, Dict, Tuple, Optional
from genaipf.utils.log_utils import logger
from .project_type_loader import get_project_type_loader


class SmartCategoryMatcher:
    """智能分类匹配器，用于快速准确地匹配Web3项目分类"""
    
    def __init__(self):
        self.loader = get_project_type_loader()
        self._build_keyword_mapping()
        self._build_synonym_mapping()
    
    def _build_keyword_mapping(self):
        """构建关键词到项目类型的映射"""
        self.keyword_mapping = {}
        
        # 定义关键词映射规则
        keyword_rules = {
            # 基础设施类
            'infra': ['infra', 'infrastructure', '基础设施', '基础架构'],
            'layer1': ['layer1', 'layer 1', 'l1', '公链', '主链', '基础链', 'base chain'],
            'layer2': ['layer2', 'layer 2', 'l2', '二层', '扩容', 'scaling', 'rollup'],
            'cloud computing': ['cloud computing', '云计算', '存储', 'storage', 'filecoin', 'arweave'],
            
            # 应用层
            'defi': ['defi', 'decentralized finance', '去中心化金融', '去中心化金融'],
            'cex': ['cex', 'centralized exchange', '中心化交易所', '中心化交易'],
            'dex': ['dex', 'decentralized exchange', '去中心化交易所', '去中心化交易'],
            'wallet': ['wallet', '钱包', '数字钱包', 'crypto wallet'],
            'ai': ['ai', 'artificial intelligence', '人工智能', '机器学习', 'machine learning'],
            'lending': ['lending', '借贷', '借代', 'loan', 'borrow'],
            'bridge': ['bridge', '跨链桥', '跨链', 'cross-chain'],
            'gaming': ['gaming', 'game', '游戏', 'gamefi', '链游'],
            'nft': ['nft', 'non-fungible token', '非同质化代币', '数字艺术品'],
            'social': ['social', '社交', 'social media', '社交媒体'],
            'creator economy': ['creator economy', '创作者经济', '内容变现', 'creator'],
            
            # 专业领域
            'depin': ['depin', 'decentralized physical infrastructure', '去中心化物理基础设施'],
            'desci': ['desci', 'decentralized science', '去中心化科学'],
            'rwa': ['rwa', 'real world asset', '现实世界资产', '实物资产'],
            'lsd': ['lsd', 'liquid staking', '流动性质押', '质押衍生品'],
            'derivatives': ['derivatives', '衍生品', '期货', 'futures'],
            'perp': ['perp', 'perpetual', '永续合约', '永续'],
            'zk': ['zk', 'zero knowledge', '零知识证明', 'zk proof'],
            
            # 代币与资产类
            'meme': ['meme', 'memecoin', '迷因币', '社区代币', 'community token'],
            'stablecoin issuer': ['stablecoin issuer', '稳定币发行商', '稳定币发行', 'usdt', 'usdc', 'dai'],
            'crypto stocks': ['crypto stocks', '币股', '股票', '上市公司', 'public company'],
            'etf': ['etf', 'exchange traded fund', '交易所交易基金', '基金'],
            
            # 社交金融
            'socialfi': ['socialfi', 'social finance', '社交金融', '社交交易'],
            
            # 服务与工具
            'tools': ['tools', '工具', '开发工具', 'dev tools'],
            'security solutions': ['security solutions', '安全解决方案', '安全审计', 'audit'],
            'did': ['did', 'decentralized identity', '去中心化身份', '身份认证'],
            'privacy': ['privacy', '隐私', '隐私保护', 'privacy protection'],
            
            # 组织与数据
            'dao': ['dao', 'decentralized autonomous organization', '去中心化自治组织'],
            'data & analysis': ['data & analysis', '数据分析', '链上数据', 'on-chain data'],
            'environmental solutions': ['environmental solutions', '环保解决方案', '碳信用', 'carbon credit'],
        }
        
        # 构建反向映射
        for project_type, keywords in keyword_rules.items():
            for keyword in keywords:
                self.keyword_mapping[keyword.lower()] = project_type
    
    def _build_synonym_mapping(self):
        """构建同义词映射"""
        self.synonym_mapping = {
            # 中文同义词
            '去中心化金融': 'defi',
            '中心化交易所': 'cex',
            '去中心化交易所': 'dex',
            '数字钱包': 'wallet',
            '人工智能': 'ai',
            '借贷平台': 'lending',
            '跨链桥': 'bridge',
            '区块链游戏': 'gaming',
            '非同质化代币': 'nft',
            '社交平台': 'social',
            '创作者经济': 'creator economy',
            '去中心化物理基础设施': 'depin',
            '去中心化科学': 'desci',
            '现实世界资产': 'rwa',
            '流动性质押': 'lsd',
            '衍生品交易': 'derivatives',
            '永续合约': 'perp',
            '零知识证明': 'zk',
            '迷因币': 'meme',
            '稳定币发行商': 'stablecoin issuer',
            '加密货币股票': 'crypto stocks',
            '交易所交易基金': 'etf',
            '社交金融': 'socialfi',
            '开发工具': 'tools',
            '安全解决方案': 'security solutions',
            '去中心化身份': 'did',
            '隐私保护': 'privacy',
            '去中心化自治组织': 'dao',
            '数据分析': 'data & analysis',
            '环保解决方案': 'environmental solutions',
            
            # 英文同义词
            'decentralized finance': 'defi',
            'centralized exchange': 'cex',
            'decentralized exchange': 'dex',
            'crypto wallet': 'wallet',
            'artificial intelligence': 'ai',
            'lending platform': 'lending',
            'cross-chain bridge': 'bridge',
            'blockchain game': 'gaming',
            'non-fungible token': 'nft',
            'social platform': 'social',
            'creator economy platform': 'creator economy',
            'decentralized physical infrastructure': 'depin',
            'decentralized science': 'desci',
            'real world asset': 'rwa',
            'liquid staking derivative': 'lsd',
            'derivative trading': 'derivatives',
            'perpetual contract': 'perp',
            'zero-knowledge proof': 'zk',
            'memecoin': 'meme',
            'stablecoin issuer': 'stablecoin issuer',
            'cryptocurrency stock': 'crypto stocks',
            'exchange-traded fund': 'etf',
            'social finance': 'socialfi',
            'development tool': 'tools',
            'security solution': 'security solutions',
            'decentralized identity': 'did',
            'privacy protection': 'privacy',
            'decentralized autonomous organization': 'dao',
            'data analytics': 'data & analysis',
            'environmental solution': 'environmental solutions',
        }
    
    def extract_keywords_from_text(self, text: str) -> List[str]:
        """从文本中提取关键词"""
        # 转换为小写
        text_lower = text.lower()
        
        # 提取关键词
        keywords = []
        
        # 直接匹配关键词
        for keyword in self.keyword_mapping.keys():
            if keyword in text_lower:
                keywords.append(keyword)
        
        # 同义词替换
        for synonym, target in self.synonym_mapping.items():
            if synonym.lower() in text_lower:
                keywords.append(target)
        
        # 使用正则表达式提取可能的项目类型
        # 匹配 "xxx项目"、"xxx平台"、"xxx协议" 等模式
        patterns = [
            r'(\w+)(?:项目|平台|协议|产品|服务|工具|应用|系统)',
            r'(\w+)(?:project|platform|protocol|product|service|tool|app|system)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            keywords.extend(matches)
        
        return list(set(keywords))  # 去重
    
    def match_categories(self, text: str, max_matches: int = 3) -> List[Tuple[str, float]]:
        """
        匹配项目分类
        
        Args:
            text: 输入文本
            max_matches: 最大匹配数量
            
        Returns:
            匹配结果列表，格式为 [(项目类型, 置信度), ...]
        """
        keywords = self.extract_keywords_from_text(text)
        logger.info(f"提取的关键词: {keywords}")
        
        matched_categories = []
        
        # 直接关键词匹配
        for keyword in keywords:
            if keyword in self.keyword_mapping:
                project_type = self.keyword_mapping[keyword]
                if self.loader.is_valid_type(project_type):
                    matched_categories.append((project_type, 1.0))
        
        # 模糊匹配
        if not matched_categories:
            for project_type in self.loader.get_all_types():
                similarity = self._calculate_similarity(text, project_type)
                if similarity > 0.3:  # 相似度阈值
                    matched_categories.append((project_type, similarity))
        
        # 按置信度排序并限制数量
        matched_categories.sort(key=lambda x: x[1], reverse=True)
        return matched_categories[:max_matches]
    
    def _calculate_similarity(self, text: str, project_type: str) -> float:
        """计算文本与项目类型的相似度"""
        from difflib import SequenceMatcher
        
        text_lower = text.lower()
        project_type_lower = project_type.lower()
        
        # 直接字符串相似度
        direct_similarity = SequenceMatcher(None, text_lower, project_type_lower).ratio()
        
        # 关键词包含相似度
        keyword_similarity = 0.0
        if project_type_lower in text_lower:
            keyword_similarity = 1.0
        elif any(word in project_type_lower for word in text_lower.split()):
            keyword_similarity = 0.8
        
        # 组合相似度
        return max(direct_similarity, keyword_similarity)
    
    def get_best_match(self, text: str) -> Optional[str]:
        """获取最佳匹配的项目类型"""
        matches = self.match_categories(text, max_matches=1)
        if matches and matches[0][1] > 0.5:  # 置信度阈值
            return matches[0][0]
        return None
    
    def get_multiple_matches(self, text: str, max_matches: int = 3) -> List[str]:
        """获取多个匹配的项目类型"""
        matches = self.match_categories(text, max_matches)
        return [match[0] for match in matches if match[1] > 0.3]


# 全局实例
_category_matcher = None

def get_category_matcher() -> SmartCategoryMatcher:
    """获取全局分类匹配器实例"""
    global _category_matcher
    if _category_matcher is None:
        _category_matcher = SmartCategoryMatcher()
    return _category_matcher
