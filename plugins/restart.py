from pyrogram import Client, filters
from sys import executable
import os

@Client.on_message(filters.private & filters.command("restart"))
async def restart(bot, message):
    cmd = message.text.split(' ', 1)
    dynoRestart = False
    dynoKill = False
    if len(cmd) == 2:
        dynoRestart = (cmd[1].lower()).startswith('d')
        dynoKill = (cmd[1].lower()).startswith('k')
    try:
        await message.reply_text("Normal Restart oluyor.")
        os.execl(executable, executable, "audiobot.py")
    except Exception as f:
        await message.reply_text(f"başaramadım {f}")
