from genaipf.dispatcher.prompt_templates_common.enrich_question import _get_enrich_question_prompted_messages
from genaipf.dispatcher.prompt_templates_common.if_need_search import _get_if_need_search_prompted_messages
from genaipf.dispatcher.prompt_templates_common.related_question import _get_related_question_prompted_messages
from genaipf.dispatcher.prompt_templates_common.if_web3_related import _get_is_web3_related_prompted_messages
import typing

_default_lang = "en"
class LionPromptCommon:
    default_lang = _default_lang

    @classmethod
    def get_prompted_messages(cls, preset_name: str, data=typing.Mapping[str, typing.Any], language=None):
        if preset_name=="enrich_question":
            return _get_enrich_question_prompted_messages(data)
        elif preset_name=="if_need_search":
            return _get_if_need_search_prompted_messages(data)
        elif preset_name=="related_question":
            return _get_related_question_prompted_messages(data, language)
        elif preset_name=="is_web3_related":
            return _get_is_web3_related_prompted_messages(data)
        else:
            raise Exception("has not")

