from genaipf.dispatcher.utils import (
    qa_coll_name,
    gpt_func_coll_name,
    pd,
    qdrant_url,
    openai,
    client,
    models,
    get_embedding,
    get_local_embedding
)
import tqdm


# # collection_name in [qa_coll_name, gpt_func_coll_name]

# # collection_name = qa_coll_name
# collection_name = gpt_func_coll_name
dimension = 1536

def update_vdb(collection_name, embedding_func):
    if collection_name == qa_coll_name:
        from genaipf.dispatcher.vdb_pairs.qa import vdb_map
    elif collection_name == gpt_func_coll_name:
        from genaipf.dispatcher.vdb_pairs.gpt_func import vdb_map

    colls = client.get_collections()
    if collection_name not in [x.name for x in colls.collections]:
        if 'backup' in collection_name:
            dimension = 4096
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=dimension, distance=models.Distance.COSINE
            ),
        )

    # ======= 把 vdb_map 新增的内容加到向量数据库 START =======
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
    print(f'>>>>> inc_texts {inc_texts[:1]} ... {inc_texts[-1:]}')
    # print(f'>>>>> tobe_vectors {tobe_vectors[:1]} ... {tobe_vectors[-1:]}')
    # ======= 把 vdb_map 新增的内容加到向量数据库 END =======

def update_all_vdb():
    for collection_name in [qa_coll_name, gpt_func_coll_name]:
        print(f'>>>>> update vdb {collection_name} start.')
        if 'backup' in collection_name:
            update_vdb(collection_name, get_local_embedding)
        else:
            update_vdb(collection_name, get_embedding)
        print(f'>>>>> update vdb {collection_name} end.')