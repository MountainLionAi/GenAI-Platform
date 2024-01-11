import json
import re


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
