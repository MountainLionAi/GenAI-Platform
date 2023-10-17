from genaipf.dispatcher.prompt_templates_v001.default import _get_default_afunc_prompt, _get_default_aref_answer_prompt, _get_default_merge_ref_and_input_text

_default_lang = "en"
class LionPrompt:
    default_lang = _default_lang
    
    @classmethod
    def get_afunc_prompt(cls, language=_default_lang):
        return _get_default_afunc_prompt(language)

    @classmethod
    def get_aref_answer_prompt(cls, language=_default_lang, preset_name=None):
        return _get_default_aref_answer_prompt(language=language)

    @classmethod
    def get_merge_ref_and_input_prompt(cls, ref, related_qa, input_text, language=_default_lang, preset_name=None, data={}):
        return _get_default_merge_ref_and_input_text(ref, related_qa, input_text, language)
            
