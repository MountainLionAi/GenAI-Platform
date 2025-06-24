#!/usr/bin/env python3
"""
智能搜索研究助手
功能：基于聊天记录生成研究问题，并使用OpenAI Responses API的Web Search功能进行并发搜索
优化版本：提升性能、简洁性和搜索质量
"""

import os
import json
import asyncio
import concurrent.futures
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import anthropic
from openai import OpenAI
import logging
from datetime import datetime, timezone
from genaipf.dispatcher.utils import ANTHROPIC_API_KEY, OPENAI_API_KEY
import time

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Question:
    """问题数据结构"""
    main_question: str
    sub_questions: List[str] = field(default_factory=list)
    time_requirement: str = "最新"
    full_question: str = ""
    search_context_size: str = "high"  # high, medium, low
    
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

class ResearchAssistant:
    """研究助手主类 - 优化版"""
    
    def __init__(self, max_workers: int = 5):
        """
        初始化API客户端
        
        Args:
            max_workers: 并发搜索的最大线程数
        """
        # 获取API密钥
        self.anthropic_api_key = ANTHROPIC_API_KEY
        self.openai_api_key = OPENAI_API_KEY
        
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY未在环境变量中找到")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY未在环境变量中找到")
        
        # 初始化客户端
        self.claude_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        # 并发控制
        self.max_workers = max_workers
        
        # 设置时区（可以通过环境变量配置）
        # self.timezone = os.getenv('TIMEZONE', 'UTC+8')
        self.timezone = os.getenv('TIMEZONE', 'UTC')
        
        logger.info("研究助手初始化成功")
    
    def get_current_time(self) -> Dict[str, str]:
        """
        获取当前时间信息
        
        Returns:
            包含各种时间格式的字典
        """
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
    
    def generate_research_questions(self, chat_history: str) -> List[Question]:
        """
        使用Claude生成需要研究的问题（增强版）
        
        Args:
            chat_history: 用户和chatbot的完整聊天记录
            
        Returns:
            List[Question]: 生成的问题列表
        """
        current_time = self.get_current_time()
        
        prompt = f"""
当前时间：{current_time['datetime']} 时区为：{self.timezone}（请基于这个时间生成问题）
今天是：{current_time['year']}年{current_time['month']}月{current_time['day']}日 {current_time['weekday']}

基于以下用户和chatbot的聊天记录，请生成需要通过网络搜索才能精准回答的研究问题。

聊天记录：
{chat_history}

重要提示：
1. 所有问题必须基于当前时间：{current_time['datetime']}，时区为：{self.timezone}来生成
2. 如果用户询问"最近"、"当前"、"现在"等信息，要查询当前时间：{current_time['datetime']}，时区为：{self.timezone}下的最新情况，根据情况增强实效性
3. 不要生成关于过去年份的问题，除非用户明确要求历史数据对比
4. 对于投资、市场、技术等快速变化的领域，只关注最近1个月内的信息

要求：
1. 智能分析用户需求的复杂度（根据问题难度判断需要搜索的主题数量）：
   - 简单查询（如天气、股价、币价）：生成1个精准问题主题
   - 中等复杂度（如产品比较、新闻事件）：生成2-3个相关问题主题
   - 高复杂度（如市场分析、技术研究）：生成3-5个深度问题主题

2. 问题设计原则：
   - 每个问题主题必须明确包含时间范围（如：2025年6月、本周、过去7天、本日、一小时内、实时等）
   - 避免过于宽泛或哲学性的问题
   - 确保全部问题主题以及具体子问题之间有逻辑关联但不重复
   - 对于复杂问题主题，可将大问题拆分成1-3个具体子问题

3. 时效性要求分类：
   - 实时数据：股价、汇率、天气等（标记为"实时"）
   - 近期信息：新闻、事件、趋势等（标记为"24小时内"、"本周"或"本月"）
   - 相对稳定：技术文档、历史事件等（标记为"最新"）

4. 搜索深度建议：
   - 简单事实查询：low
   - 需要对比分析：medium
   - 需要深度研究：high

请以以下JSON格式输出：
```json
[
    {{
        "main_question": "核心问题主题（必须包含明确的时间范围以及标出当前时间）",
        "sub_questions": ["具体子问题1", "具体子问题2"],
        "time_requirement": "时效性要求（如：实时、24小时内、本周、本月）",
        "search_context_size": "搜索深度（high/medium/low）",
        "full_question": "包含所有细节和时间范围的完整问题描述"
    }}
]
```

"""
        
        try:
            response = self.claude_client.messages.create(
                model="claude-sonnet-4-20250514",  # 使用Sonnet模型
                max_tokens=2000,
                temperature=0.3,  # 降低随机性
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
                    question = Question(
                        main_question=q_data['main_question'],
                        sub_questions=q_data.get('sub_questions', []),
                        time_requirement=q_data.get('time_requirement', '最新'),
                        search_context_size=q_data.get('search_context_size', 'high'),
                        full_question=q_data.get('full_question', '')
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
        
    def search_single_question(self, question: Question) -> SearchResult:
        """
        使用OpenAI Responses API的Web Search功能搜索单个问题
        
        Args:
            question: 要搜索的问题
            
        Returns:
            SearchResult: 搜索结果
        """
        start_time = time.time()
        current_time = self.get_current_time()
        
        try:
            # 计算上个月（修复类型错误）
            current_month_int = int(current_time['month'])
            current_year_int = int(current_time['year'])
            previous_month = current_month_int - 1 if current_month_int > 1 else 12
            previous_year = current_year_int if current_month_int > 1 else current_year_int - 1
            
            # 构建增强的搜索查询 - 优化时效性版本
            search_prompt = f"""
当前精确时间：{current_time['datetime']} UTC
今天是：{current_time['year']}年{current_time['month']}月{current_time['day']}日 {current_time['weekday']} {current_time['hour']}时{current_time['minute']}分

请搜索以下问题的答案：

{question.full_question}

⏰ 时效性要求：{question.time_requirement}

🔍 搜索及时性要求（重要）：
1. **实时数据类**（股价、币价、汇率、指数）：
   - 必须是{current_time['year']}年{current_time['month']}月{current_time['day']}日{current_time['hour']}时{current_time['minute']}分前后10分钟内的数据
   - 优先查找主要交易所/官方数据源的实时报价（https://coinmarketcap.com/）
   - 如果数据超过30分钟，明确标注"数据可能已过时"
   - 避免使用新闻媒体的二手价格信息

2. **突发新闻类**（新闻事件、公告、突发消息）：
   - 优先搜索{current_time['year']}年{current_time['month']}月{current_time['day']}日{current_time['hour']}时后发布的信息
   - 如果是{current_time['day']}日之前的消息，必须明确标注发布时间
   - 使用"最新"、"刚刚"、"今日"、"本小时"等关键词强化搜索

3. **市场分析类**（行情分析、预测、观点）：
   - 必须是{current_time['year']}年{current_time['month']}月份内发布的分析
   - 优先使用本周（{current_time['day']}日前后3天）内的分析师观点
   - 拒绝{previous_year}年{previous_month}月之前的过时分析

4. **技术数据类**（技术指标、链上数据、统计数据）：
   - 搜索{current_time['year']}年{current_time['month']}月{current_time['day']}日的最新技术指标
   - 对于24小时周期数据，确保数据截止时间不早于昨日同一时间

🎯 搜索策略优化：
- 在搜索查询中添加时间限定词："2025年6月23日"、"今日"、"实时"、"live"、"current"、"latest"
- 对于价格查询，使用"real-time price"、"current quote"、"live data"
- 验证数据时间戳，优先选择带有明确更新时间的数据源
- 交叉验证：对比2-3个不同来源的数据确保准确性

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
- 对于快速变化的数据（如加密货币），严格执行10分钟时效性要求
- 遇到冲突数据时，选择更新时间最近且来源更权威的版本
- 必须在答案开头标注数据获取的具体时间点

请严格按照以上时效性要求进行搜索和信息筛选。
"""
            
            # 使用OpenAI Responses API进行搜索 - 添加用户位置优化
            response = self.openai_client.responses.create(
                model="gpt-4.1",
                tools=[{
                    "type": "web_search_preview",
                    "search_context_size": question.search_context_size,
                    "user_location": {
                        "type": "approximate", 
                        # "timezone": "UTC+8"  # 明确设置UTC时区
                        "timezone": "UTC"  # 明确设置UTC时区
                    }
                }],
                input=search_prompt,
                temperature=0.1  # 进一步降低随机性以获得更准确和一致的结果
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
    
    def search_questions_concurrently(self, questions: List[Question]) -> List[SearchResult]:
        """
        并发搜索所有问题（优化版）
        
        Args:
            questions: 要搜索的问题列表
            
        Returns:
            List[SearchResult]: 搜索结果列表
        """
        results = []
        
        # 使用ThreadPoolExecutor进行并发搜索
        with ThreadPoolExecutor(max_workers=min(len(questions), self.max_workers)) as executor:
            # 提交所有搜索任务
            future_to_question = {
                executor.submit(self.search_single_question, question): question 
                for question in questions
            }
            
            # 处理完成的任务
            for future in as_completed(future_to_question):
                question = future_to_question[future]
                try:
                    result = future.result()
                    results.append(result)
                    logger.info(f"完成搜索: {question.main_question[:50]}...")
                except Exception as e:
                    logger.error(f"搜索任务失败: {str(e)}")
                    results.append(SearchResult(
                        question=question,
                        success=False,
                        error=str(e)
                    ))
        
        # 按原始顺序排序结果
        ordered_results = []
        for question in questions:
            for result in results:
                if result.question == question:
                    ordered_results.append(result)
                    break
        
        return ordered_results
    
    def format_results(self, results: List[SearchResult], total_time: float = 0) -> str:
        """
        格式化输出结果（增强版）
        
        Args:
            results: 搜索结果列表
            total_time: 总耗时
            
        Returns:
            str: 格式化的结果字符串
        """
        output = []
        output.append("=" * 80)
        output.append(f"📅 搜索时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append("=" * 80)
        output.append("")
        
        # 统计信息
        success_count = sum(1 for r in results if r.success)
        output.append(f"📊 搜索相关主题用于回答用户问题：成功 {success_count}/{len(results)} 个问题")
        output.append("")
        
        # 详细结果
        for i, result in enumerate(results, 1):
            output.append(f"【问题 {i}】{result.question.main_question}")
            output.append("-" * 70)
            
            # 显示子问题
            if result.question.sub_questions:
                output.append("📌 具体方面：")
                for j, sub_q in enumerate(result.question.sub_questions, 1):
                    output.append(f"   {j}. {sub_q}")
                output.append("")
            
            # 显示搜索参数
            # output.append(f"⚙️  搜索参数：")
            # # output.append(f"   • 时效性要求：{result.question.time_requirement}")
            # output.append(f"   • 搜索深度：{result.question.search_context_size}")
            # output.append(f"   • 搜索耗时：{result.search_time:.2f}秒")
            # output.append("")
            
            # 显示搜索结果
            if result.success:
                output.append("📄 搜索结果：")
                # 对长文本进行适当的格式化
                answer_lines = result.answer.split('\n')
                for line in answer_lines:
                    if line.strip():
                        output.append(f"   {line}")
            else:
                output.append(f"❌ 搜索失败：{result.error}")
            
            output.append("")
            output.append("=" * 80)
            output.append("")
        
        return "\n".join(output)
    
    def research(self, chat_history: str) -> str:
        """
        执行完整的研究流程（优化版）
        
        Args:
            chat_history: 用户和chatbot的完整聊天记录
            
        Returns:
            str: 格式化的研究结果
        """
        total_start_time = time.time()
        
        try:
            # 显示当前时间
            current_time = self.get_current_time()
            logger.info(f"当前时间：{current_time['datetime']}，时区为：{self.timezone}")
            
            # 第一步：生成问题
            logger.info("开始生成研究问题...")
            questions = self.generate_research_questions(chat_history)
            logger.info(f"已生成 {len(questions)} 个研究问题")
            
            # 记录生成的问题（用于调试）
            for i, q in enumerate(questions, 1):
                logger.debug(f"问题{i}: {q.main_question}")
            
            # 第二步：并发搜索
            logger.info("开始并发搜索...")
            results = self.search_questions_concurrently(questions)
            logger.info("搜索完成")
            
            # 计算总耗时
            total_time = time.time() - total_start_time
            
            # 格式化并返回结果
            return self.format_results(results, total_time)
            
        except Exception as e:
            logger.error(f"研究过程出错: {str(e)}")
            return f"研究过程中发生错误：{str(e)}"
        
    async def research_async(self, chat_history: str) -> str:
        """
        异步执行研究流程
        
        Args:
            chat_history: 用户和chatbot的完整聊天记录
            
        Returns:
            str: 格式化的研究结果
        """
        loop = asyncio.get_event_loop()
        
        # 在线程池中运行同步的研究方法
        with concurrent.futures.ThreadPoolExecutor() as executor:
            result = await loop.run_in_executor(
                executor, 
                self.research, 
                chat_history
            )
        
        return result
    
    @staticmethod
    async def research_multiple_async(chat_histories: List[str], max_workers: int = 3, log_level: str = "INFO") -> List[str]:
        """
        批量异步执行多个研究任务
        
        Args:
            chat_histories: 多个聊天记录列表
            max_workers: 最大并发数
            log_level: 日志级别
            
        Returns:
            List[str]: 研究结果列表
        """
        async def single_research(chat_history: str, task_id: int) -> str:
            assistant = ResearchAssistant(max_workers=2, log_level=log_level)
            result = await assistant.research_async(chat_history)
            return result
        
        # 使用信号量控制并发数
        semaphore = asyncio.Semaphore(max_workers)
        
        async def controlled_research(chat_history: str, task_id: int) -> str:
            async with semaphore:
                return await single_research(chat_history, task_id)
        
        # 并发执行所有任务
        tasks = [
            controlled_research(chat_history, i+1) 
            for i, chat_history in enumerate(chat_histories)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理异常结果
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(f"任务 {i+1} 执行失败: {str(result)}")
            else:
                processed_results.append(result)
        
        return processed_results
    
    @staticmethod
    async def research_single_static_async(chat_history: str, max_workers: int = 5, log_level: str = "INFO") -> str:
        """
        静态方法：异步执行单个研究任务（便于外部直接调用）
        
        Args:
            chat_history: 聊天记录
            max_workers: 并发搜索的最大线程数
            log_level: 日志级别
            
        Returns:
            str: 研究结果
        """
        assistant = ResearchAssistant(max_workers=max_workers, log_level=log_level)
        return await assistant.research_async(chat_history)

def main():
    """主函数示例"""
    # 示例聊天记录
    sample_chat_histories = [
        # 简单查询
        "用户：今天上海的天气怎么样？",
        
        # 中等复杂度 - 加密货币市场
        "用户：BTC最近发展近况如何？适合投资入场吗？",
        
        # 股票市场查询
        "用户：科技股最近的表现如何？有哪些值得关注的公司？",
        
        # 高复杂度 - 行业分析
        """用户：我正在考虑投资新能源汽车行业，能帮我分析一下这个行业的现状和未来趋势吗？
特别是想了解：
1. 主要的市场玩家和他们的市场份额
2. 最新的技术发展
3. 政策支持情况
4. 投资风险和机会"""
    ]
    
    try:
        # 创建研究助手实例
        assistant = ResearchAssistant(max_workers=5)
        
        # 显示当前时间
        current_time = assistant.get_current_time()
        print(f"⏰ 系统当前时间：{current_time['datetime']}")
        print(f"📅 日期：{current_time['year']}年{current_time['month']}月{current_time['day']}日 {current_time['weekday']}")
        print("="*80 + "\n")
        
        # 选择一个示例进行测试
        chat_history = sample_chat_histories[1]  # 使用加密货币的例子
        
        print("📝 聊天记录：")
        print(chat_history)
        print("\n" + "="*80 + "\n")
        
        # 执行研究
        result = assistant.research(chat_history)
        
        # 输出结果
        print(result)
        
    except ValueError as e:
        print(f"❌ 配置错误: {str(e)}")
        print("请检查.env文件中的API密钥配置")
    except Exception as e:
        print(f"❌ 程序执行出错: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()