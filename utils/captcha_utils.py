import random
import string
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from conf.server import FONT_PATH


class CaptchaGenerator:
    def __init__(self, width=200, height=80, font_size=40):
        self.width = width
        self.height = height
        self.font_size = font_size
        self.font = ImageFont.truetype(fr'{FONT_PATH}', font_size)

    def generate_code(self, length=4):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        return code

    def generate_image(self, code):
        image = Image.new('RGB', (self.width, self.height), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)

        # 绘制干扰曲线
        line_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        line_start = (random.randint(0, self.width // 2), random.randint(0, self.height))
        line_end = (random.randint(self.width // 2, self.width), random.randint(0, self.height))
        draw.line([line_start, line_end], fill=line_color, width=3)

        text_width, text_height = draw.textsize(code, font=self.font)
        x = (self.width - text_width) / 2
        y = (self.height - text_height) / 2
        draw.text((x, y), code, font=self.font, fill=(0, 0, 0))

        # 绘制噪点
        num_dots = random.randint(100, 200)
        for _ in range(num_dots):
            dot_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            dot_position = (random.randint(0, self.width), random.randint(0, self.height))
            draw.point(dot_position, fill=dot_color)

        return image

    def generate_base64(self):
        code = self.generate_code()
        image = self.generate_image(code)
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return code, base64_image
