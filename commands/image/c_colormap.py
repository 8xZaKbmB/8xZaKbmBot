from random import random
from tkinter.tix import DirTree
from PIL import Image
from PIL import ImageDraw
from io import BytesIO

from imageget import get_image

async def run_command(discord, message, args, client, opt): 
    args.pop(0)

    collist = ((0,0,0), (255,0,0), (255,255,0), (0,255,0), (0,255,255),(0,0,255), (255,0,255), (255,255,255))

    colors = await get_image(message=message,client=client)
    image = Image.new("RGBA", colors.size).convert("RGBA")

    for x in range(colors.size[0]):
        for y in range(colors.size[1]):
            distance = 9999
            best = ()
            for z in collist:
                pixel = colors.getpixel((x,y))
                tempdist = (abs(z[0] - pixel[0]),abs(z[1] - pixel[1]),abs(z[2] - pixel[2]))
                temptempdist = tempdist[0] + tempdist[1] + tempdist[2]
                if temptempdist < distance:
                    distance = temptempdist
                    best = z
            image.putpixel((x,y), best)
                

    with BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        await message.reply(file=discord.File(image_binary, "image.png"))
