from config import FONTS, X, Y, SCALING_X, SCALING_Y, BACKGROUNDS
from core.database import Router

from random import choice
from os import listdir
from typing import List
from io import BytesIO
from PIL import (
    Image, 
    ImageDraw, 
    ImageFont
)

def get_fonts() -> List[str]:
    return listdir(FONTS)

def get_background() -> str:
    return BACKGROUNDS + choice(listdir(BACKGROUNDS))

colors = dict(
        red = '🔴', yellow = '🟡', 
        blue = '🔵', orange = '🟠', 
        grey = '🔘', white = '⚪', 
        black = '⚫', green = "🟢"
    )

async def DrawPNG(text: str, user_id: int, font_size: int = 18) -> bytes:
    user = await Router.getUser(user_id)
    img_byte_array = BytesIO()
    color = get_background()
    print(color)
    background = Image.open(color).convert('RGBA')
    max_line_length = len(max(text.split("\n"), key=len))
    num_lines = len(text.split("\n"))
    image_size = (max_line_length * SCALING_X + X, num_lines * SCALING_Y + Y)
    background = background.resize(image_size, Image.LANCZOS)
    
    combined_image = Image.new('RGBA', image_size)
    combined_image.paste(background, (0, 0))  

    image = Image.new('RGBA', image_size, (0, 0, 0, 0))  
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(f'{FONTS}{user.FontNameForImage}', font_size, encoding='utf-8')

    for index, line in enumerate(text.split("\n")):
        draw.text((X, Y + index * SCALING_Y), line, fill=user.FontColorForImage, font=font)

    combined_image.paste(image, (0, 0), mask=image)  
    combined_image.save(img_byte_array, format='PNG')
    
    return img_byte_array.getvalue()


