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
        "Pragma": "no-cache",
        } 
        text = unidecode(message.text).split()
        link = text[1]
        sezonsay = text[2]
        bölümsay = text[3]
        veri = session.get(link, headers=Hea)
        veriler = veri.text
        LOGGER.info(veriler)
        if '"contentUrl":"' in veriler:
            m3u8url1 = veriler.split('"contentUrl":"')[1]
            m3u8url = m3u8url1.split('"')[0]
            url = m3u8url.replace("\/", "/")
            await message.reply_text(url)
            urlurl = session.get(url, headers=Hea)
            LOGGER.info(urlurl.text)
    except Exception as e:
        await message.reply_text(e)
        
