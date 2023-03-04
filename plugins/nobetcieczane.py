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
async def eczane(bot, message):
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
        LOGGER.info(istek.text)
        corba = BeautifulSoup(istek.content, "lxml")
        bugun = corba.find('div', id='nav-bugun')
        if not bugun: 
            return
        tumu = []
        text = f"`{il}/{ilce}` için Nöbetçi Eczaneler 👇:\n\n" 
        for bak in bugun.findAll('tr')[1:]:
            ad = bak.find('span', class_='isim').text if bak.find('span', class_='isim') else None
            mah = (None if bak.find('div', class_='my-2') is None else bak.find('div', class_='my-2').text)
            adres = bak.find('div', class_='col-lg-6').text if bak.find('div', class_='col-lg-6') else None
            tarif = (None if bak.find('span', class_='text-secondary font-italic') is None else bak.find('span', class_='text-secondary font-italic').text)
            telf = bak.find('div', class_='col-lg-3 py-lg-2').text if bak.find('div', class_='col-lg-3 py-lg-2') else None
            if ad: 
                text += f"**🏥 Eczane Adı**: {ad}\n"
            if mah: 
                text += f"**🚬 Mahallesi**: {mah}\n"
            if adres:
                text += f"**🧭 Adresi**: {adres}\n"
            if tarif: 
                text += f"**🎯 Tarif**: {tarif}\n"
            if telf: 
                text += f"**☎️ Telefon No**: {telf}\n\n"
        await message.reply_text(text)
        LOGGER.info(corba) 
    except Exception as e:
        await message.reply_text(e)
