#!/usr/bin/env python3
"""
全量重建 GenAI Qdrant 向量库（QA + Function Call）。

换 embedding 模型后（如 text-embedding-ada-002 → text-embedding-3-small）必须全量重建，
否则 function 路由 / 相关 QA 召回会漂，表现为工具选错、币种卡片错、回答风格塌成「取不到数据」。

用法（在 GenAI-Platform 根目录，已配置 .env）:

  # 测试服 / 生产通用
  python scripts/rebuild_vdb_embeddings.py
  python scripts/rebuild_vdb_embeddings.py --model text-embedding-3-small
  python scripts/rebuild_vdb_embeddings.py --dry-run

环境变量（.env）:
  OPENAI_API_KEY
  PLUGIN_NAME              如 ml4gp
  SUB_VDB_QA_PREFIX        如 TW001
  SUB_VDB_GPT_FUNC_PREFIX  如 TW001
  QDRANT_URL               可选，默认 http://localhost:6333（与代码 qdrant_url 一致时可改 utils）
  EMBEDDING_MODEL          可选，默认 text-embedding-3-small
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def _bootstrap():
    root = Path(__file__).resolve().parents[1]
    os.chdir(root)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    # 插件路径（ml4gp）通常与 GenAI 同级或 PYTHONPATH 已含
    sibling_plugin = root.parent / "ml4gp"
    if sibling_plugin.is_dir() and str(sibling_plugin) not in sys.path:
        sys.path.insert(0, str(sibling_plugin))
    env_path = root / ".env"
    if env_path.exists():
        try:
            from dotenv import load_dotenv

            load_dotenv(env_path)
        except ImportError:
            # 极简 .env 解析
            for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'").split(" #")[0].strip().rstrip('"')
                os.environ.setdefault(k, v)


def main():
    parser = argparse.ArgumentParser(description="Rebuild GenAI Qdrant VDB embeddings")
    parser.add_argument(
        "--model",
        default=os.getenv("EMBEDDING_MODEL", "text-embedding-3-small"),
        help="OpenAI embedding model id",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print target collections / key counts, do not write",
    )
    parser.add_argument(
        "--collection",
        choices=["qa", "gpt_func", "all"],
        default="all",
        help="Which collection to rebuild",
    )
    args = parser.parse_args()
    _bootstrap()

    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY missing", file=sys.stderr)
        sys.exit(1)
    if not os.getenv("PLUGIN_NAME"):
        print("ERROR: PLUGIN_NAME missing", file=sys.stderr)
        sys.exit(1)

    from genaipf.dispatcher.utils import qa_coll_name, gpt_func_coll_name, qdrant_url
    from genaipf.dispatcher.create_vdb import rebuild_vdb, rebuild_all_vdb

    print("=== rebuild_vdb_embeddings ===")
    print(f"PLUGIN_NAME={os.getenv('PLUGIN_NAME')}")
    print(f"SUB_VDB_QA_PREFIX={os.getenv('SUB_VDB_QA_PREFIX')}")
    print(f"SUB_VDB_GPT_FUNC_PREFIX={os.getenv('SUB_VDB_GPT_FUNC_PREFIX')}")
    print(f"qdrant_url={qdrant_url}")
    print(f"qa_coll={qa_coll_name}")
    print(f"gpt_func_coll={gpt_func_coll_name}")
    print(f"embedding_model={args.model}")

    # preview key counts
    from genaipf.dispatcher.vdb_pairs.qa import vdb_map as qa_map
    from genaipf.dispatcher.vdb_pairs.gpt_func import vdb_map as func_map

    print(f"qa_map_keys={len(qa_map)} gpt_func_map_keys={len(func_map)}")

    if args.dry_run:
        print("dry-run: exit without writing")
        return

    if args.collection == "all":
        rebuild_all_vdb(embedding_model=args.model)
    elif args.collection == "qa":
        rebuild_vdb(qa_coll_name, embedding_model=args.model)
    else:
        rebuild_vdb(gpt_func_coll_name, embedding_model=args.model)

    print("=== DONE ===")


if __name__ == "__main__":
    main()
