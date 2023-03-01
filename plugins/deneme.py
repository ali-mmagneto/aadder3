from pyrogram import Client, filters 
import requests
from unidecode import unidecode
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


@Client.on_message(filters.command('getlinks'))
async def linkgetir(bot, message):
    try:
        text = unidecode(message.text).split()
        link = text[1]
        veri = requests.get(link)
        veriler = veri.text
        LOGGER.info(veriler)
    except Exception as e:
        await message.reply_text(e)
        
