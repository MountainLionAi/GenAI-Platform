from genaipf.dispatcher.prompt_templates_common.divide_user_question import _get_question_type_prompted_messages
from genaipf.dispatcher.utils import async_simple_chat
from genaipf.conf.model_selection_conf import MODEL_MAPPING
from genaipf.utils.log_utils import logger
from genaipf.utils.interface_error_notice_tg_bot_util import send_notice_message
async def check_and_pick_model(newest_question, model):
    try:
        prompt = _get_question_type_prompted_messages(newest_question)
        msg_type = await async_simple_chat(prompt)
        logger.info(f"gpt判断类别{msg_type}")
        if msg_type in MODEL_MAPPING:
            model = MODEL_MAPPING[msg_type]
        else:
            model = 'openai'
        return model 
    except Exception as e:
        logger.info("model selection error, use openai as default")
        await send_notice_message('genai_utils', 'model selection', 0, e, 3)
        return 'openai'