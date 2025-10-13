"""
IP黑名单管理脚本
用于添加、移除和查看被封禁的IP地址，以及监控IP请求频率
"""
import asyncio
import sys
sys.path.append('..')

# 优先从user_log_middleware导入，因为它覆盖所有API（v1和v2）
try:
    from genaipf.middlewares.user_log_middleware import (
        add_blocked_ip, remove_blocked_ip, get_blocked_ips,
        get_ip_request_count, reset_ip_request_count, MAX_IP_REQUESTS_PER_MINUTE
    )
except ImportError:
    # 如果导入失败，回退到api_key_middleware
    from genaipf.middlewares.api_key_middleware import (
        add_blocked_ip, remove_blocked_ip, get_blocked_ips,
        get_ip_request_count, reset_ip_request_count, MAX_IP_REQUESTS_PER_MINUTE
    )


async def main():
    """
    主函数 - 演示如何管理IP黑名单和频率监控
    """
    print("=== IP黑名单和频率监控管理工具 ===\n")
    
    # 添加IP到黑名单
    print("1. 添加IP到黑名单...")
    ip_to_block = "103.215.164.218"
    result = await add_blocked_ip(ip_to_block)
    if result:
        print(f"   ✓ 成功添加 {ip_to_block} 到黑名单\n")
    else:
        print(f"   ✗ 添加失败\n")
    
    # 获取当前黑名单
    print("2. 获取当前黑名单...")
    blocked_ips = await get_blocked_ips()
    if blocked_ips:
        print(f"   当前被封禁的IP ({len(blocked_ips)}个):")
        for ip in blocked_ips:
            print(f"   - {ip}")
    else:
        print("   黑名单为空")
    print()
    
    # 检查IP请求频率
    print("3. 检查IP请求频率...")
    test_ip = "192.168.1.100"
    request_count = await get_ip_request_count(test_ip)
    print(f"   IP {test_ip} 当前请求次数: {request_count}")
    print(f"   频率限制: {MAX_IP_REQUESTS_PER_MINUTE} 次/分钟")
    if request_count > MAX_IP_REQUESTS_PER_MINUTE:
        print(f"   ⚠️  该IP已超过频率限制！")
    print()
    
    # 示例：取消封禁（注释掉，需要时可以取消注释）
    # print("4. 从黑名单移除IP...")
    # ip_to_unblock = "103.215.164.218"
    # result = await remove_blocked_ip(ip_to_unblock)
    # if result:
    #     print(f"   ✓ 成功从黑名单移除 {ip_to_unblock}\n")
    # else:
    #     print(f"   ✗ 移除失败\n")
    
    print("=== 操作完成 ===")


async def add_single_ip(ip_address: str):
    """
    添加单个IP到黑名单
    """
    result = await add_blocked_ip(ip_address)
    if result:
        print(f"✓ 成功封禁IP: {ip_address}")
    else:
        print(f"✗ 封禁IP失败: {ip_address}")
    return result


async def remove_single_ip(ip_address: str):
    """
    从黑名单移除单个IP
    """
    result = await remove_blocked_ip(ip_address)
    if result:
        print(f"✓ 成功解封IP: {ip_address}")
    else:
        print(f"✗ 解封IP失败: {ip_address}")
    return result


async def list_blocked_ips():
    """
    列出所有被封禁的IP
    """
    blocked_ips = await get_blocked_ips()
    if blocked_ips:
        print(f"当前被封禁的IP列表 (共{len(blocked_ips)}个):")
        for idx, ip in enumerate(blocked_ips, 1):
            print(f"{idx}. {ip}")
    else:
        print("黑名单为空")
    return blocked_ips


async def check_ip_frequency(ip_address: str):
    """
    检查指定IP的请求频率
    """
    request_count = await get_ip_request_count(ip_address)
    print(f"IP {ip_address} 当前请求次数: {request_count}")
    print(f"频率限制: {MAX_IP_REQUESTS_PER_MINUTE} 次/分钟")
    if request_count > MAX_IP_REQUESTS_PER_MINUTE:
        print(f"⚠️  该IP已超过频率限制！")
    return request_count


async def reset_ip_frequency(ip_address: str):
    """
    重置指定IP的请求计数
    """
    result = await reset_ip_request_count(ip_address)
    if result:
        print(f"✓ 成功重置IP {ip_address} 的请求计数")
    else:
        print(f"✗ 重置IP {ip_address} 的请求计数失败")
    return result


if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main())
    
    # 或者单独执行操作：
    # asyncio.run(add_single_ip("103.215.164.218"))
    # asyncio.run(list_blocked_ips())
    # asyncio.run(remove_single_ip("103.215.164.218"))
    # asyncio.run(check_ip_frequency("192.168.1.100"))
    # asyncio.run(reset_ip_frequency("192.168.1.100"))

