import os
import sys
sys.path.append('helpers')
import db
import helper
sys.path.append('commands')
sys.path.append('commands/fun')
sys.path.append('commands/general')
sys.path.append('commands/image')
sys.path.append('commands/other')
sys.path.append('commands/utility')
sys.path.append("api")

async def run_command(command, discord, message, args, client, opt):
    command_module = None
    try:
        command_module = __import__(f"c_{command}", globals(), locals(), [], 0)
    except Exception as e:
        print(e)
        raise SystemError(e)

    try:
        command_module.prefix = helper.prefix.check(message.content, client)[2]
        await command_module.run_command(discord, message, args, client, opt)
    except Exception as e:
        print(e)
        raise SystemError(e)

    activity_measure(message)


def activity_measure(message):
    activity = db.db_get("database/activity.json")

    usertosave = str(message.author.id)
    activity.setdefault(usertosave, 0)

    activity[usertosave] = activity[usertosave] + 1
    db.db_write(activity, "database/activity.json")
