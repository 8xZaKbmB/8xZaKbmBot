import requests, json, commands
from imageget import get_image

async def run_command(discord, message, args, client, opt):
    image = await get_image(message=message,client=client)
    if image is None:
        await message.reply("i need an image to do that")
        return await commands.run_command("help", discord, message, [prefix, "upscale"], client, [])

    await message.add_reaction("⏱️")
    r = requests.post(
        "https://api.deepai.org/api/waifu2x",
        data={
            'image': image.url,
        },
        headers={'api-key': 'tryit-14665667316-5d7e3cf48271e6e5ae7d832197839927'}
    )
    await message.remove_reaction("⏱️", message.guild.me)
    await message.reply(json.loads(r.text)["output_url"])

