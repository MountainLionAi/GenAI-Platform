import unittest
import requests
import json
import base64
from pathlib import Path


# 读取本地图片文件并转换为base64
def encode_base64(picPath: str):
    with open(picPath, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    

# 设置 Headers
headers = {
    "Content-Type": "application/json; charset=utf-8",
    'Accept': 'text/event-stream; charset=utf-8'
}

url = "http://127.0.0.1:13801/v1/api/sendStreamChat"


def writeResponse(content):
    with open('/home/ubuntu/users/zgc/GenAI-Platform/genaipf/test/response.txt', 'w') as file:
        file.write(content)


def sendPost(_param, _headers):
    # 发送 POST 请求
    response = requests.post(url, data=json.dumps(_param), headers=_headers)
    response.encoding = "UTF-8"
    # 获取响应
    if response.status_code == 200:
        print("Success:", response.text)
        writeResponse(response.text)
    else:
        print("Error:", response.status_code, response.text)
        

class TestChatStream(unittest.TestCase):
    
    
    def test_text(self):
        param = {
            "content": "我手里有10000U，帮我挑几个酷酷的NFT送我女朋友",
            "msggroup": "170902157971789",
            "language": "cn",
            "messages": [
                {
                    "role": "user",
                    "type": "user",
                    "format": "text",
                    "version": "v001",
                    "content": "你好",
                    "code": "1709022647308"
                },
                {
                    "role": "assistant",
                    "type": "text",
                    "format": "text",
                    "version": "v001",
                    "content": "您好！有什么可以为您服务的吗？如果您有任何关于Web3、加密货币或区块链的问题，或者需要交易建议，随时告诉我。",
                    "code": "23377"
                },
                {
                    "role": "user",
                    "type": "text",
                    "format": "text",
                    "version": "v001",
                    "content": "我手里有10000U，帮我挑几个酷酷的NFT送我女朋友",
                    "code": 1709092029418
                }
            ],
            "device_no": None,
            "code": 1709092029418,
            "model": "ml-plus",
            "output_type": "text",
            "owner": "MountainLion",
            "source": "v001"
        }
        sendPost(param, headers)
        
        
    def test_image(self):
        base64_image = encode_base64('/home/ubuntu/users/zgc/GenAI-Platform/genaipf/test/pics/btc1.png')
        param = {
            "content": "你好",
            "msggroup": "170902157971789",
            "language": "cn",
            "messages": [
                {
                    "role": "user",
                    "type": "user",
                    "format": "text",
                    "version": "v001",
                    "content": "你好",
                    "code": "1709022647308"
                },
                {
                    "role": "assistant",
                    "type": "text",
                    "format": "text",
                    "version": "v001",
                    "content": "您好！有什么可以为您服务的吗？如果您有任何关于Web3、加密货币或区块链的问题，或者需要交易建议，随时告诉我。",
                    "code": "23377"
                },
                {
                    "role": "user",
                    "type": "image",
                    "format": "png",
                    "version": "v001",
                    "content": "你好",
                    "base64content": f"data:image/jpg;base64,{base64_image}",
                    "code": 1709092029418
                }
            ],
            "device_no": None,
            "code": 1709092029418,
            "model": "ml-plus",
            "output_type": "text",
            "owner": "MountainLion",
            "source": "v001"
        }
        sendPost(param, headers)
    