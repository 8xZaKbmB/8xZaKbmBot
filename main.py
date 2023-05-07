import discord
import commands
import re
import option_parse
import time
import os
import sys
import helper

sys.path.append("helpers")
from udelinelogging import log
from helper import db
from client_set_theme_color import set_theme_color

sys.path.append("misc")
from keep_running import keep_alive

from dotenv import load_dotenv
load_dotenv()

# comment

class MyClient(discord.Bot):

    async def on_ready(self):
        log('Logged on as ' + self.user.name + "#" + self.user.discriminator, "log")
        self.starttime = time.time()
        await self.change_presence(activity=discord.Streaming(name=f"{helper.prefix.my_prefixes(client)[0]}help for commands", url="https://www.twitch.tv/topgeartv"))

        set_theme_color(client)

    async def on_message(self, message):
        if message.author.bot:
            return
        if helper.prefix.check(message.content, self)[0]:
            opt = option_parse.parse_options(message.content)
            for x in opt:
                if '-' + x in message.content:
                    message.content = message.content.replace('-' + x, "")
            args = re.split(" +", message.content.strip())
            prefix_len = helper.prefix.check(message.content, self)[1]
            command = args[0][prefix_len:]
            try:
                await commands.run_command(command, discord, message, args, self, opt)
            except Exception as e:
                print(e)
                raise SystemError(e)


    async def on_member_join(self, member):
        server_configs = db.db_get("database/server_configs.json")
        server_configs.setdefault(str(member.guild.id), {"join_msg_enabled": False, "join_msg_text": "", "join_msg_channel": None})
        if server_configs[str(member.guild.id)]["join_msg_enabled"] == True:
            join_msg = server_configs[str(member.guild.id)]["join_msg_text"]
            join_msg = join_msg.replace("$USER", member.name)
            try:
                guild = await self.fetch_guild(member.guild.id)
                channel = await guild.fetch_channel(server_configs[str(member.guild.id)]["join_msg_channel"])
                await channel.send(join_msg)
            except Exception as e:
                print(e)

if os.getenv("REPLIT") == "True":
    keep_alive()

intents = discord.Intents.all()
client = MyClient(intents=intents)

log("Connecting to discord", "log")
try:    
    if len(sys.argv) > 1:
        client.run(os.getenv(sys.argv[1]))
    else:
        client.run(os.getenv("TOKEN_EXPERIMENTAL"))
except discord.errors.HTTPException as e:
    log(f"Recieved exception code {e.code} while trying to log in\n{e.text}", "error")
    os.system("python3 misc/restart.py")
    os.system('kill 1')
except discord.LoginFailure as e:
    log(f"Error while connecting, invalid token\n{e}", "error")
except discord.DiscordServerError as e:
    log(f"Error while connecting, discord server error\n{e}", "error")