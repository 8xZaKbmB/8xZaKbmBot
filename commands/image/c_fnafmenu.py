from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageChops
from PIL import ImageFilter
from io import BytesIO
import math, commands
from imageget import get_image
from random import randint


async def run_command(discord, message, args, client, opt): 
    args.pop(0)

    game = randint(0,2)
    name_array = []    
    options = [
        ["New Game", "Continue"],
        ["New Game", "Continue"],
        ["NEW GAME", "LOAD GAME"]
    ]
    games = ["1","2","3"]
    games_list = ""
    for x in games:
        games_list += f"`{x}` "

    if not args[0].isnumeric():
        return await message.reply(f"{args[0]} is not one of the available options\navailable options are: {games_list}")
    if type(int(args[0])) is int:
        if not str(int(args[0])) in games:
            return await message.reply(f"{args[0]} is not one of the available options\navailable options are: {games_list}")
        game = int(args[0]) - 1
        args.pop(0)
    if len(args) > 0:
        name_array = args
    else:
        await message.reply("i need some text to do that")
        return await commands.run_command("help", discord, message, [prefix, "fnafmenu"], client, [])
    if len(args) < 0:
        await message.reply("missing arguments")
        return await commands.run_command("help", discord, message, [prefix, "fnafmenu"], client, [])
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
    if char is None:
        await message.reply("i need an image to do that")
        return await commands.run_command("help", discord, message, [prefix, "fnafmenu"], client, [])

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