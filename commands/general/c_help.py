from PIL import Image, ImageDraw, ImageFilter, ImageFont
import db
import helper
from io import BytesIO
import math
import datetime
import sys
import requests

sys.path.append('helpers')

from dominant_color import dominant_color, domimant_to_rgb, domimant_to_hex
from markup_ansi import getc

async def run_command(discord, message, args, client, opt):
    if len(args) > 1:
        commands_descriptive = db.db_get("commands/commands.json")

        if args[1] in commands_descriptive:
            command = {
                "description": commands_descriptive[args[1]][0],
                "usage": commands_descriptive[args[1]][1],
                "options": commands_descriptive[args[1]][2],
                "example": commands_descriptive[args[1]][3],
            }
            used_prefix = args[0].replace("help", "")
            embed = discord.Embed(color=client.theme_color)
            if args[1] == "exec":
                embed.description = command["description"] + "```ansi\n[1;31m[4;31mmwahahahaha you cannot use it exec is bot owner only evil face```"
            else:
                embed.description = command["description"].replace("BOTNAME", client.user.name) + "```ansi\n[0;31m```"
            embed.add_field(name="usage", value=used_prefix + command["usage"], inline=True)
            embed.add_field(name="options", value=command["options"], inline=True)
            embed.add_field(name="example use", value=f"`{used_prefix + command['example']}`" , inline=False)
            embed.set_author(name=client.user.name+": "+args[1], icon_url=client.user.display_avatar.url)
            return await message.reply(embed=embed)
        else:
            return await message.reply("that command doesn't exist")
    image = []

    command_categories = {
        "utility": [],
        "fun": [],
        "general": [],
        "other": [],
        "image": []
    }

    commands_descriptive = db.db_get("commands/commands.json")

    for x in commands_descriptive:
        if len(commands_descriptive[x]) > 4:
            if commands_descriptive[x][5] == "guildonly":
                command_categories[commands_descriptive[x][4]].append("*"+x)
            elif commands_descriptive[x][5] == "forbidden":
                command_categories[commands_descriptive[x][4]].append("&"+x)
            else:
                command_categories[commands_descriptive[x][4]].append(x)

    response = requests.get(client.user.display_avatar.with_size(1024).url)
    image = Image.open(BytesIO(response.content))
    image = image.resize((572,572))

    img_colors = dominant_color(image, "default")
    embed_color = domimant_to_rgb(img_colors[0]["color"])
    text_color = domimant_to_hex(img_colors[0]["color"])

    fontscale = 32
    smallfontscale = 20

    draw = ImageDraw.Draw(image)
    categoryfont = ImageFont.truetype("image/fonts/ConsolaMono-Bold.ttf", fontscale)
    font = ImageFont.truetype("image/fonts/ConsolaMono-Bold.ttf", smallfontscale)

    categories = ["general", "utility", "other", "image", "fun"]

    num_categories = len(categories)
    radius = 235
    aspect_y = 0.8

    for category_index in range(num_categories):
        theta = ((math.pi*2) / num_categories)
        offsetx = 50
        offsety = 50
        angle = (theta * category_index)+5.4

        category_pos = ((image.size[0]/2) - offsetx + math.sin(angle) * radius, (image.size[1] / 2) - offsety + math.cos(angle) * (radius * aspect_y))

        draw.text(category_pos, categories[category_index], text_color, font=categoryfont, stroke_width=2, stroke_fill="black")
        for y in range(len(command_categories[categories[category_index]])):
            current_command = command_categories[categories[category_index]][y]
            command_pos = ((image.size[0] / 2)-offsetx + math.sin(angle) * radius, (image.size[1] / 2)-offsety + math.cos(angle) * (radius * aspect_y) + fontscale + y * smallfontscale)
            current_fill = (255,255,255)
            if "*" in current_command:
                current_command = current_command.replace("*", "")
                current_fill = (128, 200, 255)
            if "&" in current_command:
                current_command = current_command.replace("&", "")
                current_fill = (255, 64, 64)
            draw.text(command_pos, current_command, current_fill, font=font, stroke_width=1, stroke_fill="black")


    prefix_list = " ".join(helper.prefixes[client.user.name])
    embed = discord.Embed(description=f"**prefixes: {prefix_list}**\n```ansi\n{getc('blue', 1)}blue{getc('clear', 0)} commands only work in servers\n{getc('red', 1)}red{getc('clear', 0)} commands are dev only```", color=embed_color)
    embed.set_author(name=f"{client.user.name} help",
                     icon_url=f"{client.user.display_avatar.url}")

    funfacts = open('misc/fun_facts.txt').readlines()
    now = datetime.datetime.today()
    embed.set_footer(text="Did you know? "+funfacts[now.day % len(funfacts)])

    with BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        file = discord.File(image_binary, filename="image.png")
        embed.set_image(url="attachment://image.png")
        await message.reply(file=file, embed=embed)
