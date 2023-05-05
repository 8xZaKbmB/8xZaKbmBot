import requests, json, commands
from imageget import get_image

async def run_command(discord, message, args, client, opt):
    image = await get_image(message=message,client=client)
    if image is None:
        await message.reply("i need an image to do that")
        return await commands.run_command("help", discord, message, ["u>help", "upscale"], client, [])

    await message.add_reaction("⏱️")
    r = requests.post(
        "https://api.deepai.org/api/waifu2x",
        data={
            'image': image.url,
        },
        headers={'api-key': '23e20387-716c-41e4-9773-2a653e726b32'}
    )
    await message.remove_reaction("⏱️", message.guild.me)
    await message.reply(json.loads(r.text)["output_url"])

