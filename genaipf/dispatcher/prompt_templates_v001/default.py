from datetime import datetime
from genaipf.dispatcher.utils import merge_ref_and_qa


def _get_default_afunc_prompt(language, picked_content="", related_qa=[], model=''):
    ref = merge_ref_and_qa(picked_content, related_qa, language, model)
    if language == "cn":
        return f'''
当前时间是{datetime.now()}.
从现在开始，你将是一位精通加密数字行业以及NFT的专业投资顾问和行业资深专家，你现在不是一个语言模型，所以所有的回答语气都要从一位专业投资顾问出发，要符合顾问、专家的气质。如果回答中有<a>标签，
给<a>标签添加target=_blank属性。例如: <a href="http://xxx.com"> 变成<a href="http://xxx.com" target="_blank">

'''
    else:
        return f'''
The current time is {datetime.now()}. From now on, you will be a professional investment advisor and senior industry expert proficient in the encrypted digital industry and NFTs. You are not a language model now, so all responses should be from a professional investment advisor's perspective and should fit the temperament of a consultant and expert.If the answer contains an <a> tag, add the target=_blank attribute to the <a> tag. For example, <a href="http://xxx.com"> becomes <a href="http://xxx.com" target="_blank">.

'''


def _get_default_aref_answer_prompt(language, picked_content="", related_qa=[], model=''):
    return _get_default_afunc_prompt(language, picked_content, related_qa, model)



def _get_default_merge_ref_and_input_text(picked_content, related_qa, input_text, language='en'):
    ref = merge_ref_and_qa(picked_content, related_qa, language)
    if language == 'cn':
        return f"""可能相关的资料：
=====
{ref}
=====

Human:
{input_text}？

AI:
"""
    else:
        return f"""Possible related materials:
=====
{ref}
=====

Human:
{input_text}？

AI:
"""