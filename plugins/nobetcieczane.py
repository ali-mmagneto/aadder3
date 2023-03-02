from pyrogram import Client, filters
import requests
from unidecode import unidecode

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)



@Client.on_message(filters.command('eczane'))
async def havaa(bot, message):
    try:
        ev = unidecode(message.text).split()
        if len(ev) < 3:
            await bot.send_message(message.chat.id, "Hatalı Kullanım :/ Doğru Kullanım Şu Şekilde:\n\n`/hava İstanbul Avcılar`") 
            return
        il = ev[1]
        ilce = ev[2]
        url = f"https://www.eczaneler.gen.tr/nobetci-{il}-{ilce}"
        res = requests.get(url) 
        veri = res.text
        LOGGER.info(veri) 
    except Exception as e:
        await message.reply_text(e)
