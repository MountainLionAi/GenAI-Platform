from pyppeteer import launch
from genaipf.utils.log_utils import logger
import traceback


async def get_rendered_html(url):
    try:
        browser = await launch()
        page = await browser.newPage()
        await page.goto(url)
        rendered_html = await page.content()  # 获取页面内容
        await browser.close()
        return rendered_html
    except Exception as e:
        logger.error(f'call get_rendered_html error, url={url}, {e}')
        logger.error(traceback.format_exc())