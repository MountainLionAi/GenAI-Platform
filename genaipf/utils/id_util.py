import time

DATA_CENTER_ID = 1
MACH_INE_ID = 1
SEQUENCE = 0
# 雪花算法的参数
timestamp_bits = 41
datacenter_id_bits = 5
machine_id_bits = 5
sequence_bits = 12

# 最大值
max_datacenter_id = -1 ^ (-1 << datacenter_id_bits)
max_machine_id = -1 ^ (-1 << machine_id_bits)
max_sequence = -1 ^ (-1 << sequence_bits)

# 初始时间戳（毫秒级）
start_timestamp = int(time.mktime(time.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')))


# 当前时间戳
def current_timestamp_ms():
    return int((time.time() - start_timestamp) * 1000)

# 上一次生成ID的时间戳
last_timestamp = -1

# 当前序列号
sequence = 0


# 生成雪花算法的ID
def generate_snowflake_id():
    global last_timestamp

    timestamp = current_timestamp_ms()

    if timestamp < last_timestamp:
        # 发生时钟回拨，等待时钟追赶
        timestamp = last_timestamp

    if timestamp == last_timestamp:
        sequence = (SEQUENCE + 1) & max_sequence
        if sequence == 0:
            # 序列号溢出，等待下一毫秒
            timestamp += 1
    else:
        sequence = 0

    last_timestamp = timestamp

    snowflake_id = (
            ((timestamp - start_timestamp) << (datacenter_id_bits + machine_id_bits + sequence_bits)) |
            ((DATA_CENTER_ID & max_datacenter_id) << (machine_id_bits + sequence_bits)) |
            ((MACH_INE_ID & max_machine_id) << sequence_bits) |
            (sequence & max_sequence)
    )

    return snowflake_id