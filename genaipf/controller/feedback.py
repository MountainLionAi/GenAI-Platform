import json
from genaipf.utils.log_utils import logger
from sanic import Request
from genaipf.exception.customer_exception import CustomerError
from genaipf.services.feedback_service import save_feedback
from genaipf.constant.error_code import ERROR_CODE
from genaipf.interfaces.common_response import success, fail


async def add_feedback(request: Request):
    logger.info("======start add_feedback==========")
    request_params = request.json
    if not request_params or not request_params['seriousness'] or not request_params['type'] or not request_params['content']:
        raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    seriousness = request_params.get('seriousness')
    type = request_params.get('type')
    content = request_params.get('content')
    bug_location = request_params.get('bug_location', '')
    base64_content = request_params.get('base64_content', '')
    userid = request_params.get('userid', 0)
    info = [seriousness, type, bug_location, content, base64_content, userid]
    try: 
        result = await save_feedback(info)
        return success(result)
    except Exception as e:
        logger.error(e)

