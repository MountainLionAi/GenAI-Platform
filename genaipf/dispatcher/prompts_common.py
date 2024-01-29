from genaipf.dispatcher.prompt_templates_common.enrich_question import _get_enrich_question_prompted_messages
from genaipf.dispatcher.prompt_templates_common.if_need_search import _get_if_need_search_prompted_messages
from genaipf.dispatcher.prompt_templates_common.related_question import _get_related_question_prompted_messages


_default_lang = "en"
class LionPromptCommon:
    default_lang = _default_lang

    @classmethod
    def get_prompted_messages(cls, language=_default_lang, preset_name=None, picked_content="", related_qa=[], model='', data={}):
        if preset_name=="enrich_question":
            return _get_enrich_question_prompted_messages(language, picked_content, related_qa, model, data)
        elif preset_name=="if_need_search":
            return _get_if_need_search_prompted_messages(language, picked_content, related_qa, model, data)
        elif preset_name=="related_question":
            return _get_related_question_prompted_messages(language, picked_content, related_qa, model, data)
        else:
            raise Exception("has not")

