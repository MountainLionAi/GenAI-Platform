from genaipf.dispatcher.utils import (
    qa_coll_name,
    gpt_func_coll_name,
    pd,
    qdrant_url,
    openai,
    client,
    models,
    get_embedding,
)
import tqdm
import os


dimension = 1536
DEFAULT_EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")


def _load_vdb_map(collection_name):
    if collection_name == qa_coll_name:
        from genaipf.dispatcher.vdb_pairs.qa import vdb_map

        return vdb_map
    if collection_name == gpt_func_coll_name:
        from genaipf.dispatcher.vdb_pairs.gpt_func import vdb_map

        return vdb_map
    raise ValueError(f"unknown collection: {collection_name}")


def _ensure_collection(collection_name, vector_size=dimension):
    colls = client.get_collections()
    names = [x.name for x in colls.collections]
    if collection_name not in names:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size, distance=models.Distance.COSINE
            ),
        )


def update_vdb(collection_name, embedding_func):
    """增量：只写入 vdb_map 里尚未入库的 q。"""
    vdb_map = _load_vdb_map(collection_name)
    _ensure_collection(collection_name)

    all_data = client.scroll(collection_name, limit=10000)
    ids = [record.id for record in all_data[0]]
    max_id = 0 if not ids else max(ids)
    id_cur = max_id + 1
    existing_texts = [record.payload["q"] for record in all_data[0]]
    inc_texts = [x for x in vdb_map.keys() if x not in existing_texts]
    tobe_vectors = []
    for text in tqdm.tqdm(inc_texts):
        emb_v = embedding_func(text)
        vector_dict = {
            "id": id_cur,
            "vector": emb_v,
            "payload": {"q": text, "a": vdb_map[text]},
        }
        tobe_vectors.append(vector_dict)
        id_cur += 1
    if tobe_vectors:
        client.upsert(collection_name, tobe_vectors)
    print(f">>>>> inc_texts {inc_texts[:1]} ... {inc_texts[-1:]} count={len(inc_texts)}")


def rebuild_vdb(
    collection_name, embedding_func=None, embedding_model=None, vector_size=dimension
):
    """
    全量重建：删集合 → 建集合 → 用当前 embedding 模型重写全部 vdb_map。
    换 embedding 模型时必须走这条路径，增量不够。
    """
    from genaipf.dispatcher.utils import get_embedding as _get_embedding

    model = embedding_model or DEFAULT_EMBEDDING_MODEL
    if embedding_func is None:

        def embedding_func(text):
            return _get_embedding(text, model=model)

    vdb_map = _load_vdb_map(collection_name)
    print(
        f">>>>> rebuild_vdb collection={collection_name} "
        f"keys={len(vdb_map)} model={model} qdrant={qdrant_url}"
    )

    colls = client.get_collections()
    names = [x.name for x in colls.collections]
    if collection_name in names:
        client.delete_collection(collection_name)
        print(f">>>>> deleted collection {collection_name}")

    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=vector_size, distance=models.Distance.COSINE
        ),
    )
    print(f">>>>> created collection {collection_name} dim={vector_size}")

    tobe_vectors = []
    for i, text in enumerate(tqdm.tqdm(list(vdb_map.keys())), start=1):
        emb_v = embedding_func(text)
        tobe_vectors.append(
            {
                "id": i,
                "vector": emb_v,
                "payload": {"q": text, "a": vdb_map[text]},
            }
        )
        if len(tobe_vectors) >= 64:
            client.upsert(collection_name, tobe_vectors)
            tobe_vectors = []
    if tobe_vectors:
        client.upsert(collection_name, tobe_vectors)
    print(f">>>>> rebuild_vdb done {collection_name} points={len(vdb_map)}")


def update_all_vdb():
    for collection_name in [qa_coll_name, gpt_func_coll_name]:
        print(f">>>>> update vdb {collection_name} start.")
        update_vdb(collection_name, get_embedding)
        print(f">>>>> update vdb {collection_name} end.")


def rebuild_all_vdb(embedding_model=None):
    """全量重建 QA + Function Call 两个主集合。"""
    model = embedding_model or DEFAULT_EMBEDDING_MODEL
    for collection_name in [qa_coll_name, gpt_func_coll_name]:
        print(f">>>>> rebuild vdb {collection_name} start.")
        rebuild_vdb(collection_name, embedding_model=model)
        print(f">>>>> rebuild vdb {collection_name} end.")
