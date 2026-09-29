# NFT

本模块 4 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| GET | [`/v2/api/getNftsList`](#get-v2-api-getnftslist-1) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getNftsCollection`](#get-v2-api-getnftscollection-2) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getNftsDetail`](#get-v2-api-getnftsdetail-3) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/getNftsAsset`](#post-v2-api-getnftsasset-4) | 需要 x-api-key，免登录 |

## 详情

### GET `/v2/api/getNftsList`

<a id="get-v2-api-getnftslist-1"></a>

- 路由键：`getNftsList`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getNftsList`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/nfts.py:168` `ml4gp.controller.nfts.get_nfts_list`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/getNftsCollection`

<a id="get-v2-api-getnftscollection-2"></a>

- 路由键：`getNftsCollection`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getNftsCollection`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/nfts.py:186` `ml4gp.controller.nfts.get_nfts_collection`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `collectionId` | `.get` | 无 |
| `msggroup` | `.get` | 无 |
| `language` | `.get` | 无 |
| `mainnet` | `.get` | 无 |

### GET `/v2/api/getNftsDetail`

<a id="get-v2-api-getnftsdetail-3"></a>

- 路由键：`getNftsDetail`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getNftsDetail`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/nfts.py:251` `ml4gp.controller.nfts.get_nfts_detail`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `nftId` | `.get` | 无 |
| `msggroup` | `.get` | 无 |
| `language` | `.get` | 无 |
| `tokenId` | `.get` | 无 |
| `contractAddress` | `.get` | 无 |
| `collectionId` | `.get` | 无 |
| `mainnet` | `.get` | 无 |
| `paymentContract` | `.get` | `0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee` |
| `marketplaces` | `.get` | `` |

### POST `/v2/api/getNftsAsset`

<a id="post-v2-api-getnftsasset-4"></a>

- 路由键：`getNftsAsset`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/getNftsAsset`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/nfts.py:408` `ml4gp.controller.nfts.get_nfts_asset`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `msggroup` | `.get` | 无 |

**JSON Body**

读取整包 `request.json`，字段在下游服务里拆，调用时按业务传 JSON 对象。
