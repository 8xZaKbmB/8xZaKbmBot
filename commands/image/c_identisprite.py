
import time
from PIL import Image, ImageDraw
from io import BytesIO
import hashlib
from random import randrange, seed, random
from colorutils import hsv_to_hex


async def run_command(discord, message, args, client, opt):

    randseed = time.time()
    hash = hashlib.sha256(str(int(randseed - 80)).encode('utf-8')).hexdigest()

    if len(args) > 1:
        args.pop(0)
        hash = hashlib.sha256(
            str(" ".join(args)).encode('utf-8')).hexdigest()

    seed(hash)

    identi_data = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    iterations = randrange(4, 16)

    for x in range(iterations):
        xr = randrange(0, 5)
        yr = randrange(0, 5)
        identi_data[xr][yr] = 1
        identi_data[xr][4 - yr] = 1

    img = Image.new('RGB', (25*7, 25*7), color='white')
    img1 = ImageDraw.Draw(img)

    color = hsv_to_hex((random() * 360, 0.75, 1))

    for x in range(5):
        for y in range(5):
            if identi_data[x][y] == 1:
                shape = [(25+y*25, 25+x*25), (25+y*25+25, 25+x*25+25)]
                img1.rectangle(shape, fill=color)

    with BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        await message.reply(file=discord.File(image_binary, "image.png"))
