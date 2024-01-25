from genaipf.tools.search.bing.bing import Bing
from typing import List
from genaipf.utils.common_utils import sync_to_async
import os

BING_SUBSCRIPTION_KEY = os.getenv("BING_SUBSCRIPTION_KEY")

bing = Bing(subscription_key=BING_SUBSCRIPTION_KEY)

search_of_bing = sync_to_async(bing.search)


# 利用bing搜索并检索相关内容
async def search(self, one_line_user_question: str) -> List[str]:
    """Search for a webpage based on the one_line_user_question."""
    self.metaphor_query = one_line_user_question
    print(f'>>>>>search query: {one_line_user_question}')
    res = await search_of_bing(f"{one_line_user_question}")
    results = res.get_contents()
    self.metaphor_results = results
    # self.is_stopped = True
    titles = [x.title for x in self.metaphor_results]
    return titles


# 将相关联的问题同步赋值给related_questions
async def show_related_questions(self, related_questions: List[str]) -> List[str]:
    """Based on the user's latest question and chat history,
    display 5 questions that the user might be interested in."""
    self.related_questions = related_questions
    print(f'>>>>>show_related_questions related_questions: {related_questions}')
    self.is_stopped = True
    return []


tools = [search, show_related_questions]