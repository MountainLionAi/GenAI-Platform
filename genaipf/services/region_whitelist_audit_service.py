"""区域白名单管理操作审计（MySQL）。"""
from __future__ import annotations

import json
from typing import Any

from genaipf.utils.log_utils import logger
from genaipf.utils.mysql_utils import CollectionPool


async def insert_region_whitelist_audit(
    *,
    action_type: str,
    operator_user_id: str,
    admin_key_sha256: str,
    payload: dict[str, Any],
    client_ip: str,
) -> bool:
    sql = (
        "INSERT INTO `region_whitelist_admin_audit` "
        "(`action_type`, `operator_user_id`, `admin_key_sha256`, `payload_json`, `client_ip`) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    params = (
        action_type,
        operator_user_id,
        admin_key_sha256,
        json.dumps(payload, ensure_ascii=False),
        client_ip or "",
    )
    ok = await CollectionPool().insert(sql, params)
    if not ok:
        logger.error("region_whitelist_audit: insert failed")
    return bool(ok)
