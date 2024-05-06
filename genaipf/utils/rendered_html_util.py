from pyppeteer import launch
from genaipf.utils.log_utils import logger
import traceback
from genaipf.conf.rag_conf import CHROMIUM_EXECUTABLEPATH
import time
import asyncio


async def get_rendered_html(url):
    get_rendered_html_start_time = time.perf_counter()
    try:
        if CHROMIUM_EXECUTABLEPATH:
            browser = await launch(executablePath=CHROMIUM_EXECUTABLEPATH, timeout=2000, headless=True)
        else:
            browser = await launch(timeout=2000, headless=True)
        page = await browser.newPage()
        await asyncio.wait_for(page.goto(url), timeout=9)
        rendered_html = await page.content()  # 获取页面内容
        return rendered_html
    except Exception as e:
        logger.error(f'call get_rendered_html error, url={url}, {e}')
        logger.error(traceback.format_exc())
        return None
    finally:
        if browser is not None:
            await browser.close()
            logger.info('browser closed')
        get_rendered_html_end_time = time.perf_counter()
        elapsed_get_rendered_html_time = (get_rendered_html_end_time - get_rendered_html_start_time) * 1000
        logger.info(f'=====================>get_rendered_html耗时：{elapsed_get_rendered_html_time:.3f}毫秒')    
