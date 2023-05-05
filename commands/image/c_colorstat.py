###  WIP COMMAND ###

from PIL import Image
from PIL import ImageDraw
from io import BytesIO
import commands
from imageget import get_image
import math


async def run_command(discord, message, args, client, opt):

    colors = {}

    image = await get_image(message=message, client=client)
    if image is None:
        await message.reply("i need an image to do that")
        return await commands.run_command("help", discord, message, ["u>help", "imagestat"], client, [])

    progmsg = await message.reply(f"processing, please wait...")

    image = image.convert('RGBA')

    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pixel = image.getpixel((x, y))
            pixel = '%02x%02x%02x' % (pixel[0], pixel[1], pixel[2])
            if not pixel in colors:
                colors[pixel] = 1
            else:
                colors[pixel] += 1

    modulo = math.floor(image.size[0] / 4)
    newimage = Image.new(size=(65*modulo, math.floor(1+len(colors)/modulo)*65), color=(255, 255, 255), mode="RGBA")
    imagedraw = ImageDraw.Draw(newimage)
    amongus = 0
    for x in colors.items():
        imagedraw.rectangle(((amongus % modulo) * 64, 0+math.floor(amongus/modulo) * 64, 64+(amongus % modulo) * 64, 64+math.floor(amongus/modulo) * 64), fill="#"+x[0], outline="black")
        amongus += 1

    with BytesIO() as image_binary:
        newimage.save(image_binary, 'PNG')
        image_binary.seek(0)
        await message.reply(file=discord.File(image_binary, "image.png"))
        await progmsg.delete()
