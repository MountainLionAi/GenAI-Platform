from genaipf.utils.redis_utils import (x_get,
    x_set,
    x_is_key_in,
    x_scratch_keys_of_prefix,
    x_delete,
    x_delete_keys_of_prefix,
    manual_cache
)

# await x_scratch_keys_of_prefix("")
prefix = "test:address:"
k = f'{prefix}0x001'
await x_set(k, 1)
# await x_scratch_keys_of_prefix(prefix)
await x_get(k)
await x_is_key_in(k)
await x_delete(k)