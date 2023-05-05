
import time
from PIL import Image, ImageDraw
from io import BytesIO
import hashlib
from random import randrange, seed, random, randint
from colorutils import hsv_to_hex


async def run_command(discord, message, args, client, opt):

    randseed = time.time()
    hash = hashlib.sha256(str(int(randseed - 80)).encode('utf-8')).hexdigest()

    if len(args) > 1:
        args.pop(0)
        hash = hashlib.sha256(
            str(" ".join(args)).encode('utf-8')).hexdigest()

    seed(hash)


    rand1 = randint(0, 44)
    if rand1 < 10:
        rand1 = "0" + str(rand1)
    else:
        rand1 = str(rand1)

    rand2 = randint(0, 44)
    if rand2 < 10:
        rand2 = "0" + str(rand2)
    else:
        rand2 = str(rand2)

    rand3 = randint(0, 44)
    if rand3 < 10:
        rand3 = "0" + str(rand3)
    else:
        rand3 = str(rand3)

    img1 = Image.open('image/resources/identicon/tile0' + rand1+'.png', 'r').convert("RGBA")
    img2 = Image.open('image/resources/identicon/tile0' + rand2+'.png', 'r').convert("RGBA")
    img3 = Image.open('image/resources/identicon/tile0' + rand3+'.png', 'r').convert("RGBA")
    color1 = hsv_to_hex((random() * 360, 0.4 + random() * 0.2, 1))
    color2 = hsv_to_hex((random() * 360, 0.4 + random() * 0.2, 1))
    color3 = hsv_to_hex((random() * 360, 0.4 + random() * 0.2, 1))

    img = Image.new('RGBA', (img1.size[0] * 4, img1.size[0] * 4), color='white')

    fill1 = Image.new('RGBA', img1.size, color=color1)
    fill2 = Image.new('RGBA', img1.size, color=color2)
    fill3 = Image.new('RGBA', img1.size, color=color3)

    # corners

    img.paste(fill1, (0, 0), img1)
    img1 = img1.rotate(-90)
    img.paste(fill1, (img1.size[0] * 3, 0), img1)
    img1 = img1.rotate(-90)
    img.paste(fill1, (img1.size[0] * 3, img1.size[1] * 3), img1)
    img1 = img1.rotate(-90)
    img.paste(fill1, (0, img1.size[1] * 3), img1)

    # edges

    img.paste(fill2, (img1.size[0] * 1, 0), img2)
    img2 = img2.rotate(-90)
    img.paste(fill2, (img1.size[0] * 2, 0), img2)

    img.paste(fill2, (img2.size[0] * 3, img2.size[1] * 1), img2)
    img2 = img2.rotate(-90)
    img.paste(fill2, (img2.size[0] * 3, img2.size[1] * 2), img2)

    img.paste(fill2, (img2.size[0] * 2, img2.size[1] * 3), img2)
    img2 = img2.rotate(-90)
    img.paste(fill2, (img2.size[0] * 1, img2.size[1] * 3), img2)

    img.paste(fill2, (img2.size[0] * 0, img2.size[1] * 2), img2)
    img2 = img2.rotate(-90)
    img.paste(fill2, (img2.size[0] * 0, img2.size[1] * 1), img2)

    # center

    img.paste(fill3, (img3.size[0] * 1, img3.size[1] * 1), img3)
    img3 = img3.rotate(-90)
    img.paste(fill3, (img3.size[0] * 2, img3.size[1] * 1), img3)
    img3 = img3.rotate(-90)
    img.paste(fill3, (img3.size[0] * 2, img3.size[1] * 2), img3)
    img3 = img3.rotate(-90)
    img.paste(fill3, (img3.size[0] * 1, img3.size[1] * 2), img3)

    with BytesIO() as image_binary:
        img.save(image_binary, 'PNG')
        image_binary.seek(0)
        await message.reply(file=discord.File(image_binary, "image.png"))
