from datetime import datetime


# 获取当前时间
def get_format_time():
    now = datetime.now()
    format_time = now.strftime('%Y-%m-%d %H:%M:%S')
    return format_time


# 获取当前日期
def get_format_time_YYYY_mm_dd():
    now = datetime.now()
    return now.strftime('%Y-%m-%d')
