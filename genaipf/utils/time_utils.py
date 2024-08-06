from datetime import datetime, timedelta


# 获取当前时间
def get_format_time():
    now = datetime.now()
    format_time = now.strftime('%Y-%m-%d %H:%M:%S')
    return format_time


# 获取当前日期
def get_format_time_YYYY_mm_dd():
    now = datetime.now()
    return now.strftime('%Y-%m-%d')


# 获取当前的时间戳
def get_current_timestamp():
    now = datetime.now()
    return int(datetime.timestamp(now))

# 获取当前毫秒级时间戳
def get_current_timestamp_msec():
    return int(datetime.now().timestamp() * 1000)

# 获取变化后的时间天数
def get_days_change_time(days):
    changed_time = datetime.now() + timedelta(days=days)
    return changed_time.strftime('%Y-%m-%d %H:%M:%S')