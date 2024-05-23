from pyppeteer import launch
from genaipf.utils.log_utils import logger
import traceback
from genaipf.conf.rag_conf import CHROMIUM_EXECUTABLEPATH
import time
import asyncio
from playwright.async_api import async_playwright
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


async def get_rendered_html(url):
    get_rendered_html_start_time = time.perf_counter() # a
    try:
        if CHROMIUM_EXECUTABLEPATH:
            browser = await launch(executablePath=CHROMIUM_EXECUTABLEPATH, timeout=2000, headless=True)
        else:
            browser = await launch(headless=True, timeout=2000)
        page = await browser.newPage()
        page.goto(url)
        #await asyncio.wait_for(page.goto(url), timeout=20)
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



async def get_rendered_html_by_playwright(url):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)
            html = await page.content()
            return html
    except Exception as e:
        logger.error(f"get_rendered_html_by_playwright error, url={url}, {e}")
        logger.error(traceback.format_exc())
        return None
    finally:
        if browser is not None:
            await browser.close()
            
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver_path = '/usr/bin/chromedriver'  # ChromeDriver 路径

            
async def get_rendered_html_by_selenium(url):
    try:
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(10)
        driver.get(url)
        driver.implicitly_wait(10)
        html = driver.page_source
        return html
    except Exception as e:
        logger.error(f"get_rendered_html_by_driver_chrome error, url={url}, {e}")
        logger.error(traceback.format_exc())
        return None
    finally:
        if driver:
            driver.quit()
    