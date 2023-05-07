import commands

async def run_command(discord, message, args, client, opt):
    
    if len(args) < 1 and not message.reference:
        await message.reply("i need a number to do that")
        return await commands.run_command("undecimal", discord, message, [prefix, "undecimal"], client, [])

    if not args[1].isnumeric():
        await message.reply("i need a number to do that and that's not a number")
        return await commands.run_command("undecimal", discord, message, [prefix, "undecimal"], client, [])

    x = int(args[1])
    digs = "0123456789⒑"
    base = 11
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return await message.reply(''.join(digits))