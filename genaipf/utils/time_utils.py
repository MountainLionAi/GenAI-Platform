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


def get_time_diff_seconds(start_time, end_time):
    # 指定的目标日期时间
    target_date = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    start_date = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

    # 计算时间差
    time_difference = target_date - start_date

    # 获取相差的秒数
    seconds_difference = time_difference.total_seconds()
    return int(seconds_difference)

# 根据某个日期计算那个日期或者其前后的某天的开始时间
def get_0time_by_date(days=0, date=''):
    if not date:
        # 获取当前时间
        time_source = datetime.now()
    else:
        time_source = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')


    # 计算days天的日期
    day_after_tomorrow = time_source + timedelta(days=days)

    # 将时间设为0点0分0秒
    day_after_tomorrow_midnight = day_after_tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)

    # 格式化时间为 y-m-d h:i:s
    formatted_time = day_after_tomorrow_midnight.strftime('%Y-%m-%d %H:%M:%S')

    return formatted_time


def get_before_timestamp(date_str, days=0):
    # Define the date and time
    date_format = "%Y-%m-%d %H:%M:%S"

    # Convert string to datetime object
    date_obj = datetime.strptime(date_str, date_format)

    # Subtract 20 days from the given date
    new_date = date_obj + timedelta(days=days)

    # Get the timestamp of the new date
    timestamp = new_date.timestamp()
    return str(round(timestamp * 1000))


def get_time_fraction():
    # 获取当前时间
    current_time = datetime.now()

    # 提取小数秒部分
    return str(current_time.microsecond)


def timestamp_to_str(timestamp, format='%Y-%m-%d %H:%M:%S'):
    # 将时间戳转换为 datetime 对象
    dt_object = datetime.fromtimestamp(timestamp)

    # 将 datetime 对象转换为指定格式的字符串
    formatted_time = dt_object.strftime(format)

    return formatted_time