import ast
import json
import time
import os
from genaipf.tools.search.metaphor.metaphor_search_agent import other_search
from genaipf.tools.search.metaphor.llamaindex_tools import tools
from genaipf.utils.log_utils import logger
from genaipf.utils.time_utils import get_format_time_YYYY_mm_dd, get_current_time
from openai import OpenAI
import asyncio
from genaipf.dispatcher.prompts_common import LionPromptCommon
from genaipf.dispatcher.utils import async_simple_chat, async_simple_chat_with_model
from genaipf.tools.search.utils.search_task_manager import get_related_question_task, get_sources_tasks, \
    get_is_need_search_task, multi_sources_task, get_divide_questions, check_ai_ranking
from genaipf.tools.search.google_serper.google_serper_agent import google_serper

client = OpenAI()

fixed_related_question = {
    'zh': {
        'title': '我想要使用费用低廉且便捷的兑换。',
    },
    'cn': {
        'title': '我想要使用费用低廉且便捷的兑换。',
    },
    'en': {
        'title': ' I want to use convenient and low-cost  swap service.',
    }
}

not_need_search = ['generate_report', 'qrcode_address', 'wallet_balance', 'token_transfer', 'coin_swap', 'richer_prompt', 'get_gas', 'check_hash', 'check_address', 'check_order', 'tx_hash_analysis', 'black_address']
not_need_sources = ['generate_report', 'qrcode_address', 'wallet_balance', 'token_transfer', 'coin_swap', 'richer_prompt', 'url_search', 'get_gas', 'check_hash', 'check_address', 'check_order', 'tx_hash_analysis', 'black_address']
need_gpt = ['get_gas', 'check_hash', 'check_address', 'check_order', 'black_address']

# system_prompt = f"""
# 今天是 {get_format_time_YYYY_mm_dd()}，你是个工具人，你既能联网，也能给用户推荐其他感兴趣的问题，必须调t用工具 function，有 2 种情况 SCENE_1 和 SCENE_2：
# ### SCENE_1
# 用户问的问题最好联网搜索才能回答更好，
# 用户问的问题可能是比较简单的表述，直接网络搜索的结果不好，
# 用户的问题是什么语言 你必须根据这个语言扩充丰富一下形成一个全面完整的问题再触发 search 工具 function (完整的问题 query 一定要信息丰富但不要超过100个字符，query里(包括它前后)不要有换行符)
# 调用 show_related_questions，必须根据用户当前问题相同的语言再生成 5 个用户可能感兴趣的问题，如果没有就不回复。
# ### SCENE_2
# 调用 show_related_questions, 必须根据用户当前问题相同的语言直接生成 5 个用户可能感兴趣的问题，如果没有就不回复。
#
# 你在不能直接回答用户问题，在回答用户前必须按情况 SCENE_1 或 SCENE_2 的流程调用 gpt function。
# 不要直接回答问题，即使用户说些无聊的对话也要根据用户的历史对话执行 SCENE_2 的 show_related_questions (而不是回答 "SCENE_2")
# """

async def premise_search(newest_question, message_history, related_qa=None):
    system_prompt = f"""
        今天是 {get_format_time_YYYY_mm_dd()}，你是个工具人，你既能联网，也能给用户推荐其他感兴趣的问题，必须调用工具 function，有 2 种情况 SCENE_1 和 SCENE_2：
        ### SCENE_1
        用户问的问题可能是比较简单的表述，直接网络搜索的结果不好
        你扩充丰富一下生成一个全面完整的问题再调用 metaphor_search (完整的问题 query 不是"SCENE_1"，并且一定要信息丰富但不要超过100个字符，query里(包括它前后)不要有换行符)
        调用 show_related_questions，生成 5 个用户可能感兴趣的问题。
        ### SCENE_2
        调用 show_related_questions，生成 5 个用户可能感兴趣的问题。
    
        你在不能直接回答用户问题，在回答用户前必须按情况 SCENE_1 或 SCENE_2 的流程调用 gpt function
        不要直接回答问题，即使用户说些无聊的对话也要根据用户的历史对话执行 SCENE_2 的 show_related_questions (而不是回答 "SCENE_2")
        """
    if related_qa is None:
        related_qa = []
    chat_history = []
    # if message_history is not None:
    #     for question in message_history:
    #         chat_message = ChatMessage(role="user", content=question)
    #         chat_history.append(chat_message)
    from genaipf.agent.llama_index import LlamaIndexAgent
    agent = LlamaIndexAgent(tools, system_prompt=system_prompt, chat_history=chat_history, verbose=True)
    agent.metaphor_query = ""
    agent.metaphor_results = None
    agent.related_questions = []
    agent.start_chat(newest_question)

    _tmp_text = ""
    async for x in agent.async_response_gen():
        if x["role"] == "gpt":
            _tmp_text += str(x["content"])
        pass
    related_questions = []
    if agent.related_questions is not None:
        for r_question in agent.related_questions:
            r_question = r_question.replace("\n", '', -1)
            if len(r_question) > 0 and r_question != '':
                related_questions.append({"title": r_question})
    sources = []
    if agent.metaphor_results and len(agent.metaphor_results.contents) != 0:
        sources, content = get_contents(agent.metaphor_results.contents)
        related_qa.append(newest_question + ':' + content)
    logger.info(f'>>>>> _tmp_text: {_tmp_text}')
    logger.info(f'>>>>> 扩充后的问题: {agent.metaphor_query}')
    logger.info(f'>>>>> 相关话题推荐: {agent.related_questions}')
    logger.info(f'>>>>> 返回数据: {sources}, {related_questions}')
    return sources, related_qa, related_questions


async def premise_search1(front_messages, related_qa=None, language=None):
    data = {}
    data['messages'] = front_messages
    msgs1 = LionPromptCommon.get_prompted_messages("if_need_search", data)
    msgs2 = LionPromptCommon.get_prompted_messages("enrich_question", data)
    # 相关问题取最新的
    newest_question_arr = {"messages": [data['messages'][-1]]}
    msgs3 = LionPromptCommon.get_prompted_messages("related_question", newest_question_arr, language)
    t1 = asyncio.create_task(async_simple_chat(msgs1))
    t2 = asyncio.create_task(async_simple_chat(msgs2))
    t3 = asyncio.create_task(async_simple_chat(msgs3))
    # t1t2t3 并发运行的；
    # 另外如果不需要搜索（t1 的结果是 False），不用等待 t2 和 网络搜索
    sources = []
    await t1
    need_search = t1.result()
    if need_search in "True":
        print(f"need search: {need_search}")
        await t2
        new_question = t2.result()
        if new_question != "False":
            sources, related_qa = await other_search(t2.result(), related_qa, language)
        print(f"enriched question: {t2.result()}")
    await t3
    questions_result = t3.result()
    related_questions = []
    if questions_result != 'False':
        try:
            for question in json.loads(questions_result):
                related_questions.append({"title": question})
            # AIswap用的少，先去掉
            # related_questions.insert(1, fixed_related_question[language])
        except Exception as e:
            logger.error(e)
    print(f"related_question: {t3.result()}")
    return sources, related_qa, related_questions


async def premise_search2(front_messages, related_qa=None, language=None, source=''):
    data = {'messages': front_messages}
    # 相关问题取最新的
    newest_question_arr = {"messages": [data['messages'][-1]]}
    t2 = asyncio.create_task(get_sources_tasks(data, related_qa, language, source))
    t3 = asyncio.create_task(get_related_question_task(newest_question_arr, fixed_related_question, language, source))
    return t2, t3


async def multi_rag(front_messages, related_qa=None, language=None, source='', enrich_questions=''):
    data = {'messages': front_messages}
    # 相关问题取最新的
    newest_question_arr = {"messages": [data['messages'][-1]]}
    t1 = asyncio.create_task(multi_sources_task(data, related_qa, language, source, enrich_questions))
    t2 = asyncio.create_task(get_related_question_task(newest_question_arr, fixed_related_question, language, source))
    t3 = asyncio.create_task(check_ai_ranking(data, language, source))
    # await t1
    # need_search = t1.result()
    # return need_search, t2, t3
    return t1, t2, t3

async def get_sub_qeustions(enrich_questions, language):
    final_questions = []
    for questions in enrich_questions:
        sub_questions = await generate_questions(questions, language)
        final_questions.extend(sub_questions)
    return final_questions

def is_need_rag_simple(message):
    l = ['hi', 'hello', '你好', '您好', '1 + 1 = ? 1 or 2?']
    if message and len(message) > 1 and not message in l:
        return True
    else:
        return False

async def new_question_question(is_need_search: str, language: str, improve_question_task, related_qa):
    sources = []
    if is_need_search in "True":
        await improve_question_task
        new_question = improve_question_task.result()
        if new_question != "False":
            sources, related_qa = await other_search(new_question, related_qa, language)
    return sources, related_qa


# format content to str
def get_contents(contents):
    sources = []
    formatted_string = ''
    for index, news_item in enumerate(contents):
        if index < 3:
            formatted_string += f"{news_item.extract}\n引用地址: {news_item.url}\n"
        sources.append({"title": news_item.title, "url": news_item.url})
    return sources, formatted_string


async def related_search(question: str, language=None):
    messages = [
        {"role": "system",
         "content": "你是个工具人，直接根据用户的提问，生成 5 个用户可能感兴趣的问题。最后使用[]返回，例如：[{'title': '中国队在最近的亚洲杯对阵卡塔尔的比赛结果如何？'}]"},
        {"role": "user", "content": question}
    ]
    if language == 'en':
        messages = [
            {"role": "system",
             "content": "You are a tool person, directly generating 5 questions of potential interest to users based "
                        "on their inquiries. Finally, return in the format of [], for example: [{'title': 'What is "
                        "the recent result of the match between the Chinese team and Qatar in the Asian Cup?'}]."},
            {"role": "user", "content": question}
        ]
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    try:
        python_object = ast.literal_eval(completion.choices[0].message.content)
        return python_object
    except (SyntaxError, ValueError) as e:
        return []

async def generate_questions(question: str, language=None):
    current_time = get_current_time()
    timezone =  os.getenv('TIMEZONE', 'UTC')
    language_requirement =  f"请使用{language}生成" if language!='en' else "Please use English to generate"
    messages = [
        {"role": "system",
         "content": f"""
        当前时间：{current_time['datetime']} 时区为：{timezone}（请基于当前时间对问题的时效性作出明确要求）

        基于以下用户和chatbot的聊天记录，把用户根本需求拆解，分成子问题并通过网络搜索解决子问题，从而能精准解决用户需求。

        聊天记录：
        {question}

        重要提示：
        1. 所有问题必须基于当前时间：{current_time['datetime']}，时区为：{timezone}来生成
        2. 如果用户询问"最近"、"当前"、"现在"等信息，要查询当前时间：{current_time['datetime']}，时区为：{timezone}下的最新情况，根据情况增强实效性
        3. 不要生成关于过去年份的问题，除非用户明确要求历史数据对比
        4. 对于投资、市场、技术等快速变化的领域，只关注最近的信息

        要求：
        1. 智能分析用户需求的复杂度（根据问题难度判断需要搜索的主题数量）：
        - 简单查询（如天气、股价、币价）：生成1个精准问题主题
        - 中等复杂度（如产品比较、新闻事件）：生成2-3个相关问题主题
        - 高复杂度（如市场分析、技术研究）：生成3-5个深度问题主题

        2. 问题设计原则：
        - 每个问题主题必须明确包含时间范围（如：2025年6月、本周、过去7天、本日、一小时内、实时等）
        - 避免过于宽泛或抽象的问题
        - 确保全部问题主题以及具体子问题之间有逻辑关联但查询内容不重复。
        - 对于复杂问题主题，可将大问题进一步细化为1-3个具体子问题

        3. 时效性要求分类：
        - 实时数据：股价、汇率、天气等（标记为"实时"）
        - 近期信息：新闻、事件、趋势等（标记为"24小时内"、"本周"或"本月"）
        - 相对稳定：技术文档、历史事件等（标记为"最新"）

        请以以下JSON格式输出：
        [
            {{
                "main_question": "核心问题主题（必须包含明确的时间范围以及标出当前时间）",
                "sub_questions": ["具体子问题1", "具体子问题2"],
            }}
        ]

        """},
        {"role": "user", "content": question +language_requirement}
    ]
    
    try:
        _result = await async_simple_chat_with_model(messages, model='claude-sonnet-4-20250514', base_model='claude')
        return _result
    except (SyntaxError, ValueError) as e:
        return []
