from datetime import datetime, timedelta, timezone
import pytz


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


def modify_time_diff(start_time, diff_days, period='day'):
    start_date = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    if period == 'minute':
        final_date = start_date + timedelta(minutes=diff_days)
    else:
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


def get_time_delta(delta_num, period='h', format='%Y%m%d%H'):
    # 获取当前时间
    now = datetime.now()

    if period == 'h':
        next_time = now + timedelta(hours=delta_num)
    elif period == 'd':
        next_time = now + timedelta(days=delta_num)
    elif period == 'm':
        next_time = now + timedelta(minutes=delta_num)
    # 格式化为 Ymdh 格式
    formatted_time = next_time.strftime(format)
    return formatted_time


def convert_to_utc_yyyy_MM_dd_HH_mm_ss(time_string: str, timezone: str) -> str:
    """
    将指定时区的时间字符串转换为UTC-0时间字符串。
    参数:
        time_string (str): 输入的时间字符串，格式为 'yyyy-MM-dd HH:mm:ss'。
        timezone (str): 输入时间所属的时区，例如 'Asia/Shanghai'。
        
    返回:
        str: 转换为UTC-0时区的时间字符串，格式为 'yyyy-MM-dd HH:mm:ss'。
    """
    # 定义输入时间的格式
    time_format = "%Y-%m-%d %H:%M:%S"
    # 解析输入的时间字符串为 datetime 对象
    local_tz = pytz.timezone(timezone)
    local_time = datetime.strptime(time_string, time_format)
    # 添加时区信息
    localized_time = local_tz.localize(local_time)
    # 转换为UTC时间
    utc_time = localized_time.astimezone(pytz.utc)
    # 格式化为字符串返回
    return utc_time.strftime(time_format)


def format_datetime_with_timezone_2_yyyy_MM_dd_HH_mm_ss(dt: datetime, time_zone: str) -> str:
    """
    将 datetime 对象按照指定时区格式化为 'yyyy-MM-dd HH:mm:ss'。
    
    参数:
        dt (datetime): 需要转换的 datetime 对象。
        time_zone (str): 目标时区，例如 'Asia/Shanghai'。
        
    返回:
        str: 转换后的时间字符串，格式为 'yyyy-MM-dd HH:mm:ss'。
    """
    # 获取目标时区对象
    target_tz = pytz.timezone(time_zone)
    # 将 datetime 对象转换为目标时区
    localized_time = dt.astimezone(target_tz)
    # 格式化为字符串
    return localized_time.strftime('%Y-%m-%d %H:%M:%S')


def utc_to_shanghai(utc_time_str):
    """
    将UTC时间字符串（格式：%Y-%m-%d %H:%M:%S）转换为上海时间（北京时间）。

    :param utc_time_str: UTC时间字符串，例如 "2025-02-06 09:41:21"
    :return: 上海时间字符串，格式为 "%Y-%m-%d %H:%M:%S"
    """
    # 解析UTC时间字符串
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%d %H:%M:%S")

    # 设置UTC时区
    utc_time = utc_time.replace(tzinfo=pytz.UTC)

    # 转换为上海时间
    shanghai_time = utc_time.astimezone(pytz.timezone('Asia/Shanghai'))

    # 返回格式化后的上海时间
    return shanghai_time.strftime("%Y-%m-%d %H:%M:%S")


def modify_time_diff_utc8(start_time, diff_days, period='day'):
    # 解析输入时间为datetime对象（假设输入是UTC时间）
    start_date = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)

    # 根据周期进行时间加减
    if period == 'minute':
        final_date = start_date + timedelta(minutes=diff_days)
    elif period == 'hour':
        final_date = start_date + timedelta(hours=diff_days)
    else:  # 默认按天处理
        final_date = start_date + timedelta(days=diff_days)

    # 转换为UTC+8时区（上海时间）
    shanghai_tz = timezone(timedelta(hours=8))
    shanghai_time = final_date.astimezone(shanghai_tz)

    return shanghai_time.strftime('%Y-%m-%d %H:%M:%S')


def get_format_time_utc8():
    # 获取当前UTC时间
    utc_now = datetime.now(timezone.utc)

    # 转换为UTC+8时区（上海时间）
    shanghai_tz = timezone(timedelta(hours=8))
    shanghai_time = utc_now.astimezone(shanghai_tz)

    # 格式化输出
    return shanghai_time.strftime('%Y-%m-%d %H:%M:%S')
