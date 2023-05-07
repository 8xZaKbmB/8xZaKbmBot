import asyncio
import commands
import time

async def run_command(discord, message, args, client, opt):

    if message.author.guild_permissions.manage_messages == False:
        return await message.reply("you lack the required permissions to `manage messages`")
        
    if len(args) < 2:
        await message.reply("you need to tell me how many messages to delete")
        return await commands.run_command("help", discord, message, [prefix, "purge"], client, [])
    count = args[1]

    messages = await message.channel.history(limit=int(count)).flatten()

    loop = False

    delete = asyncio.get_event_loop()
    for x in messages:
        datenow = time.time() - x.created_at.timestamp()
        if(datenow > 1209600):
            loop = True

    if loop != None:
        for x in messages:
            await x.delete()
        msg = await message.channel.send("deleted **`"+str(count)+"`** messages in <#"+str(message.channel.id)+">")
        await asyncio.sleep(5)
        delete.run_until_complete(await msg.delete())
    else:
        await message.channel.delete_messages(messages)
        msg = await message.channel.send("deleted **`"+str(count)+"`** messages in <#"+str(message.channel.id)+">")
        await asyncio.sleep(5)
        delete.run_until_complete(await msg.delete())

