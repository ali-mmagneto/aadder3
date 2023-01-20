import shutil
import psutil
import math

from functions.progress import humanbytes
from plugins.save_file import equee
from plugins.aac import aquee
from pyrogram import Client, filters


@Client.on_message(filters.command("status"))
async def status(bot, message):
    msg = await message.reply_text(text="`Bekle 😊😇🙃`")
    toplam, kullanilan, bos = shutil.disk_usage(".")
    toplam = humanbytes(toplam)
    kullanilan = humanbytes(kullanilan)
    bos = humanbytes(bos)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    text = f"**Toplam Alanım:** `{toplam}` \n"
    text += f"**Kullanılan Alan:** `{kullanilan}({disk_usage}%)` \n"
    text += f"**Boş Alanım:** `{bos}` \n"
    text += f"**CPU Kullanımım:** `{cpu_usage}%` \n"
    text += f"**RAM Kullanımım:** `{ram_usage}%`\n\n"
    text += f"**Yapacak extract ișim: {len(equee)} 😡**\n"
    text += f"**Yapacak aac ișim: {len(aquee)} 😡**" 
    await msg.edit(
        text=text
    )
    return
