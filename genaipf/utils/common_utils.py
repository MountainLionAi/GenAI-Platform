import json
import re
import asyncio
import uuid
from urllib.parse import urlparse
from genaipf.utils.snowflake import SnowflakeIdWorker
import functools
import traceback

def async_exception_handler(decorator_arg=None):
    def inner_function(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                print(f"An error occurred in the function {func.__name__}:")
                traceback.print_exc()
                raise e
        return wrapper
    return inner_function

def safe_float_conversion(value):
    try:
        return float(value)
    except:
        return 0

# 判断一个对象是不是json
def check_is_json(text):
    try:
        json.loads(text)
        return True
    except ValueError:
        return False


# 邮箱返回值增加*mask
def mask_email(email):
    parts = email.split("@")
    if len(parts) != 2:
        return ''

    local = parts[0]
    domain = parts[1]

    # Masking the middle part of the local part
    if len(local) > 2:
        local = local[:2] + '*' * 4 + local[-1]
    else:
        local = '*' * len(local)

    return f"{local}@{domain}"


# 获取两个数字增减的百分比
def percentage_change(initial, final):
    try:
        change = ((final - initial) / initial) * 100
        # 为增长添加"+"前缀，减少则自带"-"符号
        formatted_change = f"+{change:.2f}%" if change > 0 else f"{change:.2f}%"
        return formatted_change
    except ZeroDivisionError:
        return "Undefined"  # 如果起始数字是0，则返回"Undefined"，表示无法计算百分比变化


# 截取钱包地址的前32位作为equipmentNo
def get_equipment_no(address: str) -> str:
    return address.lower()[0: 32]


# 判断是否含有特殊字符
def contains_special_character(s):
    special_characters = '!@#$%^&*()-=_+[]{}|;:\'",.<>?/'
    return any(c in special_characters for c in s)


def check_evm_wallet_format(address):
    pattern = r'^0x[a-fA-F0-9]{40}$'
    if re.match(pattern, address):
        return True
    else:
        return False


def is_valid_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# 将同步方法转换成异步非阻塞的，避免在调用过程中阻塞
def sync_to_async(fn):
    async def _async_wrapped_fn(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: fn(*args, **kwargs))
    return _async_wrapped_fn


# 判断一段话中是否含有中文
def contains_chinese(text):
    if bool(re.search(r'[\u4e00-\u9fff]+', text)):
        return 'cn'
    else:
        return 'en'


async def aget_multi_coro(afunc, args_l, batch_size=10, timeout=None):
    from tqdm.asyncio import tqdm
    pbar = tqdm(total=len(args_l))
    res_l = []
    # 将任务分批处理
    async def _afunc(*args):
        try:
            # 使用 asyncio.wait_for 设置超时
            v = await asyncio.wait_for(afunc(*args), timeout)
            return args, v
        except asyncio.TimeoutError:
            return args, None  # 根据需要处理超时情况
    for i in range(0, len(args_l), batch_size):
        batch = args_l[i:i + batch_size]
        tasks = []
        for args in batch:
            tasks.append(asyncio.create_task(_afunc(*args)))
        # 等待当前批次的所有任务完成
        for t in asyncio.as_completed(tasks):
            res = await t
            res_l.append(res)
            pbar.update(1)
    pbar.close()
    return res_l


def convert_token_amount(amount, decimals, to_standard_unit=True):
    """
    转换代币的数量单位。

    :param amount: 要转换的数量。
    :param decimals: 代币的精度。
    :param to_standard_unit: 如果为True，则将从最小单位转换到标准单位。如果为False，则反之。
    :return: 转换后的数量。
    """
    if to_standard_unit:
        # 从最小单位转换到标准单位
        return amount / (10 ** decimals)
    else:
        # 从标准单位转换到最小单位
        return int(amount * (10 ** decimals))


def complete_url(url: str) -> str:
    """
    This function checks if the passed URL contains the HTTP or HTTPS protocol.
    If not, it prepends 'http://' to the URL.

    Parameters:
    url (str): The URL to check and possibly complete.

    Returns:
    str: The completed URL with the HTTP protocol if it was missing.
    """
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url



def is_valid_url(url: str) -> bool:
    """
    Validates a URL by checking its scheme and netloc.

    Parameters:
    url (str): The URL to validate.

    Returns:
    bool: True if the URL is valid, False otherwise.
    """
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme) and bool(parsed_url.netloc)


def get_uniq_id():
    # 初始化 Snowflake 实例
    worker = SnowflakeIdWorker(datacenter_id=1, worker_id=1)
    return worker.get_id()

# 进行浮点数计算
def process_number(num_str, addition):
    # 将输入字符串转换为浮点数
    num_float = float(num_str)

    # 进行计算
    result_float = num_float + addition

    # 返回格式化后的六位小数字符串
    return format(result_float, ".6f")


# 生成唯一uuid
def get_uuid():
    # 生成一个随机的 UUID
    unique_uuid = uuid.uuid4()

    # 将 UUID 转换为字符串
    uuid_str = str(unique_uuid)
    return uuid_str

# 获取两个整数之间的随机数
def get_random_number(from_num, end_num):
    random_number = random.randint(from_num, end_num)
    return random_number
