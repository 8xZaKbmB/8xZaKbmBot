

from PIL import Image
from io import BytesIO
import commands
from imageget import get_image
import math
import re


async def run_command(discord, message, args, client, opt):

    amp = 128

    for x in range(len(opt)):
        opt[x] = opt[x].split("=")
        if opt[x][0] == "power":
            if math.isnan(float(opt[x][1])):
                return await message.reply("\"power\" option must be number")
            amp = int(float(re.sub("\n.*$", "", opt[x][1])))

    image = await get_image(message=message, client=client)
    if image is None:
        await message.reply("i need an image to do that")
        return await commands.run_command("help", discord, message, ["u>help", "crispy"], client, [])

    progmsg = await message.reply(f"processing, please wait...")

    image = image.convert('RGBA')
    newimage = Image.new(
        size=(image.size[0], image.size[1]), mode="RGBA")

    for x in range(image.size[0]):
        for y in range(image.size[1]):
            pixel = image.getpixel((x, y))
            newpixel = (round(
                pixel[0] / amp) * amp, round(pixel[1] / amp) * amp, round(pixel[2] / amp) * amp)
            newimage.putpixel((x, y), (newpixel[0], newpixel[1], newpixel[2]))
    with BytesIO() as image_binary:
        newimage.save(image_binary, 'PNG')
        image_binary.seek(0)
        await message.reply(file=discord.File(image_binary, "image.png"))
        await progmsg.delete()
