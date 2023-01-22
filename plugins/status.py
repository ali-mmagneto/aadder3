import shutil
import psutil
import math
import time
import logging

from helper_func.progress_bar import humanbytes
from plugins.save_file import equee
from plugins.aac import aquee
from pyrogram import Client, filters
from config import botStartTime2
from helper_func.thumb import ReadableTime
from pyrogram.types import Message


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@Client.on_message(filters.command('log'))
async def log_handler(bot, message):
    with open('log.txt', 'rb') as f:
        try:
            await bot.send_document(document=f,
                                  file_name=f.name, reply_to_message_id=message.id,
                                  chat_id=message.chat.id, caption=f.name)
        except Exception as e:
            await message.reply_text(str(e))

@Client.on_message(filters.command("status") | filters.regex('Status😔'))
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
    text += f"**RAM Kullanımım:** `{ram_usage}%`\n"
    text += f"**Yașım:** `{ReadableTime(time.time() - botStartTime2)}`\n\n"
    text += f"**Yapacak extract ișim: {len(equee)} 😡**\n"
    text += f"**Yapacak aac ișim: {len(aquee)} 😡**" 
    await msg.edit(
        text=text
    )
    return
