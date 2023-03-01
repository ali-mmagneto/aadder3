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
        if 'name="popcorn:stream" content="' in veriler:
            m3u8url1 = veriler.split('name="popcorn:stream" content="')[1]
            m3u8url = m3u8url1.split('"')[0]
            await message.reply_text(m3u8url)
        LOGGER.info(veriler)
    except Exception as e:
        await message.reply_text(e)
        
