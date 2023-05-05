from random import random
from PIL import Image
from PIL import ImageDraw
from io import BytesIO

from imageget import get_image

async def run_command(discord, message, args, client, opt): 
    args.pop(0)

    colors = await get_image(message=message,client=client)
    image = Image.new("RGBA", colors.size)
    draw = ImageDraw.Draw(image)

    iteration = 1
    while iteration < 1000:
        x = random() * image.size[0]
        y = random() * image.size[1]
        size = (image.size[0] / (iteration * 0.1)) * 0.5

        x1 = x - size + ((random() * 100) / iteration)
        x2 = x + size + ((random() * 100) / iteration)
        y1 = y - size + ((random() * 100) / iteration)
        y2 = y + size + ((random() * 100) / iteration)

        draw.rectangle((x1,y1,x2,y2), fill=colors.getpixel((x,y)))
        iteration += 1

    with BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        await message.reply(file=discord.File(image_binary, "image.png"))
