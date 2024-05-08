import time
import threading


class SnowflakeIdWorker:
    # 初始化
    def __init__(self, datacenter_id, worker_id, sequence=0):
        # 起始的时间戳，从2020-01-01 00:00:00开始
        self.start_timestamp = int(time.mktime(time.strptime('2020-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')))

        # 机器ID与数据中心ID的位数
        self.worker_id_bits = 5
        self.datacenter_id_bits = 5

        # 支持的最大机器id和数据中心id数量
        self.max_worker_id = -1 ^ (-1 << self.worker_id_bits)
        self.max_datacenter_id = -1 ^ (-1 << self.datacenter_id_bits)

        # 序列号占的位数
        self.sequence_bits = 12

        # 机器ID左移位数
        self.worker_id_shift = self.sequence_bits
        # 数据中心ID左移位数
        self.datacenter_id_shift = self.sequence_bits + self.worker_id_bits
        # 时间戳左移位数
        self.timestamp_left_shift = self.sequence_bits + self.worker_id_bits + self.datacenter_id_bits

        # 序列掩码，用于限制序列最大值不超过4095
        self.sequence_mask = -1 ^ (-1 << self.sequence_bits)

        # 检查数据中心ID和机器ID是否超出上限
        if not (0 <= datacenter_id <= self.max_datacenter_id):
            raise ValueError(f"datacenter_id超出范围 (应该在0和{self.max_datacenter_id}之间)")
        if not (0 <= worker_id <= self.max_worker_id):
            raise ValueError(f"worker_id超出范围 (应该在0和{self.max_worker_id}之间)")

        # 实例变量赋值
        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.sequence = sequence
        self.last_timestamp = -1

        # 添加锁
        self.lock = threading.Lock()

    # 生成ID
    def get_id(self):
        with self.lock:
            timestamp = int(time.time() * 1000)

            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.sequence_mask
                if self.sequence == 0:
                    timestamp = self._wait_for_next_millis(timestamp)
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            new_id = ((timestamp - self.start_timestamp) << self.timestamp_left_shift) | \
                     (self.datacenter_id << self.datacenter_id_shift) | \
                     (self.worker_id << self.worker_id_shift) | \
                     self.sequence
            return new_id

    # 等待下一个毫秒级时间戳
    def _wait_for_next_millis(self, last_timestamp):
        timestamp = int(time.time() * 1000)
        while timestamp <= last_timestamp:
            timestamp = int(time.time() * 1000)
        return timestamp
