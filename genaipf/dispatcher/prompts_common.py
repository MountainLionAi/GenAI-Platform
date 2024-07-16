from genaipf.dispatcher.prompt_templates_common.enrich_question import _get_enrich_question_prompted_messages
from genaipf.dispatcher.prompt_templates_common.if_need_search import _get_if_need_search_prompted_messages
from genaipf.dispatcher.prompt_templates_common.related_question import _get_related_question_prompted_messages
from genaipf.dispatcher.prompt_templates_common.related_url import _get_related_url_prompted_messages
from genaipf.dispatcher.prompt_templates_common.summary_page_by_msg import _get_summary_page_by_msg_prompted_messages
from genaipf.dispatcher.prompt_templates_common.richer_prompt import _get_richer_prompt_prompted_messages
from genaipf.dispatcher.prompt_templates_common.choose_hot_question import _choose_hot_question_prompted_messages
from genaipf.dispatcher.prompt_templates_common.swap_agent_question import _get_swap_agent_question_prompted_messages
from genaipf.dispatcher.prompt_templates_common.nft_agent_question import _get_nft_agent_question_prompted_messages
from genaipf.dispatcher.prompt_templates_common.recent_search import _get_recent_search_prompted_messages
from genaipf.dispatcher.prompt_templates_common.share_summary import _get_share_summary_prompted_messages
import typing

_default_lang = "en"
class LionPromptCommon:
    default_lang = _default_lang

    @classmethod
    def get_prompted_messages(cls, preset_name: str, data=typing.Mapping[str, typing.Any], language=None):
        if preset_name=="enrich_question":
            return _get_enrich_question_prompted_messages(data, language)
        elif preset_name=="if_need_search":
            return _get_if_need_search_prompted_messages(data)
        elif preset_name=="related_question":
            return _get_related_question_prompted_messages(data, language)
        elif preset_name=="related_url":
            return _get_related_url_prompted_messages(data, language)
        elif preset_name=="summary_page_by_msg":
            return _get_summary_page_by_msg_prompted_messages(data, language)
        elif preset_name=="richer_prompt":
            return _get_richer_prompt_prompted_messages(data, language)
        elif preset_name=="choose_hot_question":
            return _choose_hot_question_prompted_messages(language)
        elif preset_name=="swap_agent_question":
            return _get_swap_agent_question_prompted_messages(language)
        elif preset_name=="swap_nft_question":
            return _get_nft_agent_question_prompted_messages(language)
        elif preset_name=="recent_search":
            return _get_recent_search_prompted_messages(data)
        elif preset_name=="share_summary":
            return _get_share_summary_prompted_messages(data, language)
        else:
            raise Exception("has not")

