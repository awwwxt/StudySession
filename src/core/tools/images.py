from config import FONTS, X, Y, SCALING_X, SCALING_Y
from core.tools import sync_to_async
from core.database import Router

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

colors = dict(
        red = '🔴', yellow = '🟡', 
        blue = '🔵', orange = '🟠', 
        grey = '🔘', white = '⚪', 
        black = '⚫', green = "🟢"
    )

async def DrawPNG(text: str, user_id: int) -> bytes:
    user = await Router.getUser(user_id)
    img_byte_array = BytesIO()
    
    image = Image.new(
        mode = 'RGB', 
        size = (
             len(max(text.split("\n"), key = len)) * SCALING_X + X,
             len(text.split("\n")) * SCALING_Y + Y
            ), 
        color = user.BackgroundColorForImage)
    
    draw = ImageDraw.Draw(image)
    draw.text(
        xy = (X, Y), 
        text = text, 
        fill = user.FontColorForImage, 
        font = ImageFont.truetype(f'{FONTS}{user.FontNameForImage}', 18, encoding='utf-8'), 
        align = user.AlignTextForImage)
    
    image.save(img_byte_array, format='PNG')
    return img_byte_array.getvalue()