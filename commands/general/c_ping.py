import psutil
import time
import datetime
import db
from helper import time_decorate


async def run_command(discord, message, args, client, opt):
    ramusage = psutil.cpu_percent()
    uptime = time.time() - client.starttime

    embed = discord.Embed(description="uptime: **`"+time_decorate(str(datetime.timedelta(seconds=uptime)), True) + "`**\n"+"latency: **`"+str("???")+"`**\n""RAM usage: **`"+str(ramusage)+"%`**\n", color=client.theme_color)
    embed.set_author(name=client.user.name+" stats", icon_url=client.user.display_avatar.url)

    mymsg = await message.reply(embed=embed)
    latency = mymsg.created_at - message.created_at

    embed = discord.Embed(description="uptime: **`"+time_decorate(str(datetime.timedelta(seconds=uptime)), True)+"`**\n" + "latency: **`"+time_decorate(str(latency), False)+"`**\n""RAM usage: **`"+str(ramusage)+"%`**\n", color=client.theme_color)
    embed.set_author(name=client.user.name+" stats", icon_url=client.user.display_avatar.url)

    await mymsg.edit(embed=embed)
