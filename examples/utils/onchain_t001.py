from ml4gp.lib.onchain import *

usdt_c_addr = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
tx_hash = "0x3a614cd5bb7400f5371080bfbec23c4623c6d18e998875c14a84cbbd45d0eaf2"

# x = await async_get_ethereum_symbol_info("usdt")
# print(f'async_get_ethereum_symbol_info("usdt") => {x}')

x = await async_get_ethereum_erc20_info([usdt_c_addr])
print(f'async_get_ethereum_erc20_info([usdt_c_addr]) => {x}')
# run 3s
# async_get_ethereum_erc20_info([usdt_c_addr]) => [{"blockchain":"ethereum","contract_address":"0xdac17f958d2ee523a2206206994597c13d831ec7","symbol":"USDT","decimals":6}]


x = await async_top_10_eth_transaction(100000.0)
print(f'async_top_10_eth_transaction(10.0) => {x}')
# run 2min and error
# run 5min and error
# run 59s and error

x = await async_top_10_erc20_transaction(usdt_c_addr, 100000.0)
print(f'async_top_10_erc20_transaction(usdt_c_addr, 10.0) => {x}')
# run 25s
# async_top_10_erc20_transaction(usdt_c_addr, 10.0) => [{"from":"0x5041ed759dd4afc3a72b8192c143f72f4724081a","to":"0xf584f8728b874a6a5c7a8d4d387c9aae9172d621","amount":737256.272,"evt_block_time":"2024-07-08 01:17:47.000 UTC","evt_tx_hash":"0x0a23ae50fe5cdd6346befec98f36caf6f95e2b4a1e2ca11b53b7cb459314f91a"},{"from":"0x5041ed759dd4afc3a72b8192c143f72f4724081a","to":"0xed89da9dd83a0d703991ee833969489278b260e7","amount":162452.362,"evt_block_time":"2024-07-08 01:17:47.000 UTC","evt_tx_hash":"0x4792bea67933dec5117c2b0e3c2adf668f6ec4edef4f7598573fbeace4c5c1e4"},{"from":"0xa6f50af589a411f80dccef6a2ede746c44dedcad","to":"0x5041ed759dd4afc3a72b8192c143f72f4724081a","amount":194201.92,"evt_block_time":"2024-07-08 01:17:35.000 UTC","evt_tx_hash":"0x70cf0f6cf9c64807f8758bbf4ee04ea6e8b57f7aaa32df2208ee40b22de27a4e"},{"from":"0x1111111254eeb25477b68fb85ed929f73a960582","to":"0x9ae79dd8c663b40f16bf45567f74486c9c274c52","amount":172826.128139,"evt_block_time":"2024-07-08 01:16:47.000 UTC","evt_tx_hash":"0xc9c0c9318840c7302ac7381779b877bd943fe246923f1e66b905d3bd8c6bae77"},{"from":"0xe37e799d5077682fa0a244d46e5649f71457bd09","to":"0x1111111254eeb25477b68fb85ed929f73a960582","amount":172826.128139,"evt_block_time":"2024-07-08 01:16:47.000 UTC","evt_tx_hash":"0xc9c0c9318840c7302ac7381779b877bd943fe246923f1e66b905d3bd8c6bae77"},{"from":"0x46340b20830761efd32832a74d7169b29feb9758","to":"0xa6f50af589a411f80dccef6a2ede746c44dedcad","amount":194201.92,"evt_block_time":"2024-07-08 01:16:11.000 UTC","evt_tx_hash":"0x0d0053e06f8825f40f96e50b03ee9e45ddd905ad2301e2d403eda35f323ce2b4"},{"from":"0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43","to":"0xdd04f596569b09bb967ab9f20cdc1b7bc7495afd","amount":475759.260838,"evt_block_time":"2024-07-08 01:16:11.000 UTC","evt_tx_hash":"0xca2544769d4fa66b8a6833ec9c08a4a9a096c1e3737c05605eb862f2ca7ae318"},{"from":"0x11b815efb8f581194ae79006d24e0d814b7697f6","to":"0xa69babef1ca67a37ffaf7a485dfff3382056e78c","amount":134063.966273,"evt_block_time":"2024-07-08 01:15:23.000 UTC","evt_tx_hash":"0x741f0344e6c6fb8596618cc13092049f08bba4e2000a22f1897cc34eabcbd692"},{"from":"0x91db9e27e750c43a96926b2e04d795c24f13f67b","to":"0x1522900b6dafac587d499a862861c0869be6e428","amount":546526.0,"evt_block_time":"2024-07-08 01:15:11.000 UTC","evt_tx_hash":"0xe7fe998a8ddb2563ed13433fed6ee2e14598c02a75f68d77cae2515d1d6acc3f"},{"from":"0xa69babef1ca67a37ffaf7a485dfff3382056e78c","to":"0x9db9e0e53058c89e5b94e29621a205198648425b","amount":1946680.7618829999,"evt_block_time":"2024-07-08 01:14:47.000 UTC","evt_tx_hash":"0x1488402cb1c71f29306f235b2f3c66fdeb87282dabba4af4ff9434fcf31dd188"}]

x = await async_get_address_labels([usdt_c_addr])
print(f'async_get_address_labels([usdt_c_addr]) => {x}')
# run 42s
# async_get_address_labels([usdt_c_addr]) => [{"address":"0xdac17f958d2ee523a2206206994597c13d831ec7","labels":"[Paraswap User less than 1 week old DEX trader Tether: Tether_USD Fiat-backed stablecoin Number of DEXs traded on: 1 pssssssshao.eth <=$400 avg. DEX trade value DEX Aggregator Trader]"}]

x = await async_get_funds_transfer_status_in_transaction(tx_hash)
print(f'async_get_funds_transfer_status_in_transaction(tx_hash) => {x}')
# run 1m21s
# async_get_funds_transfer_status_in_transaction(tx_hash) => {"transaction": {"accessList": [], "blockHash": "0x93421070e7d587c63a37561c93527d06d85bfe6076060fab1c40e74ec4f8736c", "blockNumber": 20238418, "chainId": 1, "from": "0x1f9090aaE28b8a3dCeaDf281B0F12828e676c326", "gas": 21000, "gasPrice": 12660606344, "hash": "0x3a614cd5bb7400f5371080bfbec23c4623c6d18e998875c14a84cbbd45d0eaf2", "input": "0x", "maxFeePerGas": 12660606344, "maxPriorityFeePerGas": 0, "nonce": 660682, "r": "0x262480d422079298f7adba91ecb121329f857f034a6fe3ffd734ef91ab4acff1", "s": "0x37a921081406f158b9c99507984433aaf5391c136c1487d0c3dafe567f03d52f", "to": "0xe688b84b23f322a994A53dbF8E15FA82CDB71127", "transactionIndex": 112, "type": 2, "v": 1, "value": 50621760910869087, "yParity": "0x1"}, "eth_transfer_action": [{"callType": "call", "from": "0x1f9090aaE28b8a3dCeaDf281B0F12828e676c326", "gas": 0, "input": "", "to": "0xe688b84b23f322a994A53dbF8E15FA82CDB71127", "value": "0.050621760910869087"}], "address_info": [{"address": "0x1f9090aaE28b8a3dCeaDf281B0F12828e676c326", "symbol": "", "labels": "[rsync-builder.eth Ethereum Miner]"}, {"address": "0xe688b84b23f322a994A53dbF8E15FA82CDB71127", "symbol": "", "labels": "[Uniswap User Ethereum Miner less than 1 week old DEX trader DEX Trader Number of DEXs traded on: 1 <=$400 avg. DEX trade value]"}]}