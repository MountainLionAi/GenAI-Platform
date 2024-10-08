# 通过环境变量传递（作用于全局，优先级最低）
import os
from genaipf.conf import server
import qianfan


os.environ["QIANFAN_ACCESS_KEY"] = server.QIANFAN_ACCESS_KEY
os.environ["QIANFAN_SECRET_KEY"] = server.QIANFAN_SECRET_KEY

# chat_comp = qianfan.ChatCompletion()

# # 指定特定模型
# resp = chat_comp.do(model="ERNIE-Speed-128K", messages=[{
#     "role": "user",
#     "content": "你好"
# }])

# print(resp["body"])


chat_comp = qianfan.ChatCompletion()

resp = chat_comp.do(model="ERNIE-Speed-128K", messages=[{
    "role": "user",
    "content": "简单介绍下故宫"
}], stream=True)

for r in resp:
    print(r["body"])