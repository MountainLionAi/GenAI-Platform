import os

import oss2
import base64
import asyncio

access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID')
access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET')
bucket_name = os.getenv('OSS_TEST_BUCKET')
endpoint = os.getenv('OSS_TEST_ENDPOINT')

bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)

def put_image(name: str, file: str):
    result = bucket.put_object(name, file)
    return result
