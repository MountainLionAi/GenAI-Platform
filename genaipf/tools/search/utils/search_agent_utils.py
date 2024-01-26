import ast
from genaipf.tools.search.metaphor import metaphor_search_agent
from llama_index.llms import ChatMessage
from genaipf.agent.llama_index import LlamaIndexAgent
from genaipf.tools.search.metaphor.llamaindex_tools import tools
from genaipf.utils.log_utils import logger
from genaipf.utils.time_utils import get_format_time_YYYY_mm_dd
from openai import OpenAI
client = OpenAI()

# system_prompt = f"""
# 今天是 {get_format_time_YYYY_mm_dd()}，你是个工具人，你既能联网，也能给用户推荐其他感兴趣的问题，必须调用工具 function，有 2 种情况 SCENE_1 和 SCENE_2：
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


# dict sources: [{'title': '', 'url': ''}]
# str content
async def other_search(question: str, related_qa=[], language=None):
    # -------- metaphor --------
    sources, metaphor_result = await metaphor_search_agent.metaphor_search2(question)
    if len(sources) > 0:
        related_qa.append(question + ' : ' + metaphor_result)

    # -------- other --------
    return sources, related_qa


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
        model="gpt-4-1106-preview",
        messages=messages
    )
    try:
        python_object = ast.literal_eval(completion.choices[0].message.content)
        return python_object
    except (SyntaxError, ValueError) as e:
        return []
