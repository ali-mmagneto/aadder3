from pyrogram import Client, filters 
import requests
from unidecode import unidecode
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

session = requests.Session()

@Client.on_message(filters.command('getlinks'))
async def linkgetir(bot, message):
    try:
        Hea={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "content-type": "aplication/json" 
        }
        text = unidecode(message.text).split()
        link = text[1]
        veri = session.get(link, headers=Hea, timeout=15, verify=False)
        veriler = veri.text
        LOGGER.info(veriler)
    except Exception as e:
        await message.reply_text(e) 
