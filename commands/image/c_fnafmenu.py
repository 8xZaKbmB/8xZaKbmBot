from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageChops
from PIL import ImageFilter
from io import BytesIO
import math
from imageget import get_image
from random import randint


async def run_command(discord, message, args, client, opt): 
    game = randint(0,2)
    name_array = []    
    options = [
        ["New Game", "Continue"],
        ["New Game", "Continue"],
        ["NEW GAME", "LOAD GAME"]
    ]
    if len(args) > 2:
        game = int(args[2])
    if len(args) > 1:
        name_array = name_array + args[3:]
    else:
        name_array = ["Please", "Give", "a", "Name"]
    res = [(854, 480), (640, 480), (640, 480)]
    colors = [(255,255,255), (255,255,255), (190,255,128)]
    positions = [(115, 51), (56, 15), (115, 51)]

    fnt1 = ImageFont.truetype("image/fonts/CONSOLA.TTF", 32)
    fnt2 = ImageFont.truetype("image/fonts/OCR-A.ttf", 40)
    fnt2opt = ImageFont.truetype("image/fonts/OCR-A.ttf", 34)
    fnt3 = ImageFont.truetype("image/fonts/5Computers-In-Love.ttf", 24)

    offsets = [37,37,37]
    optoffsets = [48,48,37]

    fonts = [fnt1, fnt2, fnt3]

    static = Image.open("image/resources/fnafstatic.png")
    static.putalpha(75)

    effect = Image.open(f"image/resources/fnaf{game+1}effect.png")


    char = await get_image(message=message,client=client)

    image = Image.new("RGBA", res[game], "black")
    text = Image.new("RGBA", res[game], "black")

    propotion = image.size[1] / char.size[1]

    char = char.resize((math.floor(char.size[0] * propotion), math.floor(char.size[1] * propotion)))

    gradient = Image.open("image/resources/gradient.png")

    image.paste(char, (image.size[0] - char.size[0],0))

    if game != 0:
        image.paste(gradient, (-100,0), gradient)
    else:
        image.paste(gradient, (0,0), gradient)

    image.paste(effect, (0,0), effect)

    image.paste(static, (0,0), static)

    # title
    d1 = ImageDraw.Draw(text)
    for i, word in enumerate(name_array):
        d1.text((positions[game][0], positions[game][1] + i * offsets[game]), word, fill=colors[game], font=fonts[game])

    # options
    if game == 1:
        fonts[1] = fnt2opt
    for i, word in enumerate(options[game]):
        d1.text((positions[game][0],250 +  positions[game][1] + i * optoffsets[game]), word, fill=colors[game], font=fonts[game])
    image = ImageChops.screen(text, image)

    # fnaf 3 blur
    if game == 2:
        image = ImageChops.screen(text, image)
        image = ImageChops.screen(text, image)

        text = text.filter(ImageFilter.GaussianBlur(radius=5))

        image = ImageChops.screen(text, image)
        image = ImageChops.screen(text, image)

    with BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        await message.reply(file=discord.File(image_binary, "image.png"))