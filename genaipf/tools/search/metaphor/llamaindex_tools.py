import os
from typing import List
from genaipf.utils.common_utils import sync_to_async
from metaphor_python import Metaphor

METAPHOR_API_KEY = os.getenv("METAPHOR_API_KEY")

metaphor = Metaphor(api_key=METAPHOR_API_KEY)

search_of_metaphor = sync_to_async(metaphor.search)
aget_contents_of_metaphor = sync_to_async(metaphor.get_contents)


# 利用metaphor搜索并检索相关内容
async def metaphor_search(self, one_line_user_question: str) -> List[str]:
    """Search for a webpage based on the one_line_user_question."""
    self.metaphor_query = one_line_user_question
    print(f'>>>>>search query: {one_line_user_question}')
    res = await search_of_metaphor(f"{one_line_user_question}", num_results=5, type='keyword')
    ids = [x.id for x in res.results]
    results = await aget_contents_of_metaphor(ids)
    self.metaphor_results = results
    # self.is_stopped = True
    titles = [x.title for x in self.metaphor_results.contents]
    return titles


# 将相关联的问题同步赋值给related_questions
async def show_related_questions(self, related_questions: List[str]) -> List[str]:
    """Based on the user's latest question and chat history,
    display 5 questions that the user might be interested in."""
    self.related_questions = related_questions
    print(f'>>>>>show_related_questions related_questions: {related_questions}')
    self.is_stopped = True
    return []


tools = [metaphor_search, show_related_questions]
