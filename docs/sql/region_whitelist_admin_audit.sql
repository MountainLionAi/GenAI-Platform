-- 区域白名单管理审计表（需在业务库执行一次）
CREATE TABLE IF NOT EXISTS `region_whitelist_admin_audit` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `action_type` VARCHAR(48) NOT NULL COMMENT 'query / mutate_append / mutate_replace / mutate_delete / mutate_clear',
  `operator_user_id` VARCHAR(128) NOT NULL,
  `admin_key_sha256` CHAR(64) NOT NULL COMMENT '请求头管理密钥的 SHA256 十六进制',
  `payload_json` TEXT NOT NULL COMMENT '请求体或查询说明的 JSON',
  `client_ip` VARCHAR(128) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `idx_created` (`created_at`),
  KEY `idx_operator` (`operator_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='美国区白名单管理操作审计';
