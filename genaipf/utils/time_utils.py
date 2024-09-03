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


# 获取两个日志之间的差值
def get_days_diff(start_time, end_time):
    start_date = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    difference = (end_date - start_date).days + 1
    return difference


def modify_time_diff(start_time, diff_days):
    start_date = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    final_date = start_date + timedelta(days=diff_days)
    return final_date.strftime('%Y-%m-%d %H:%M:%S')