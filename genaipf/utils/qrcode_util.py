import qrcode
import base64
from io import BytesIO
import asyncio


async def generate_qr_code_base64(url: str) -> str:
    """异步生成包含url地址的二维码，并返回Base64编码的字符串。"""
    loop = asyncio.get_event_loop()
    # 使用run_in_executor运行同步代码
    img_base64_str = await loop.run_in_executor(None, sync_generate_qr_base64, url)
    return img_base64_str


def sync_generate_qr_base64(wallet_address: str) -> str:
    """同步生成二维码并转换为Base64字符串。"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(wallet_address)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # 将二维码图片保存到内存中的BytesIO对象
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # 将二维码图片转换为Base64字符串
    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"
