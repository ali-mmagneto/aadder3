from pyrogram import Client, filters
import requests
from unidecode import unidecode
from bs4 import BeautifulSoup
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

session = requests.Session()

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
        Hea={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Pragma": "no-cache",
        } 
        istek = session.get(url, headers=Hea) 
        corba = BeautifulSoup(istek.content, "lxml")
        veri = corba.text
        LOGGER.info(veri) 
    except Exception as e:
        await message.reply_text(e)
