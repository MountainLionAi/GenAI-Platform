import json
import re
import asyncio


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
        return 'zh'
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