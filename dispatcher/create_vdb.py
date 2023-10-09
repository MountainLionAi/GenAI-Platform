from dispatcher.utils import (
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


# collection_name in ["filtered_qa", "gpt_func"]

# collection_name = qa_coll_name
collection_name = gpt_func_coll_name
dimension = 1536


if collection_name == "filtered_qa":
    from dispatcher.vdb_pairs.qa import vdb_map
elif collection_name == "gpt_func":
    from dispatcher.vdb_pairs.gpt_func import vdb_map

colls = client.get_collections()
if collection_name not in [x.name for x in colls.collections]:
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
    emb_v = get_embedding(text)
    vector_dict = {
        "id": id_cur,
        "vector": emb_v,
        "payload": {"q": text, "a": vdb_map[text]},
    }
    tobe_vectors.append(vector_dict)
    id_cur += 1
if tobe_vectors:
    client.upsert(collection_name, tobe_vectors)
# ======= 把 vdb_map 新增的内容加到向量数据库 END =======
