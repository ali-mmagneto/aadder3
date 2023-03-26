from pyrogram import Client, filters
import requests
from requests.structures import CaseInsensitiveDict

from bs4 import BeautifulSoup
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

from re import findall as re_findall 

_global_session = requests.Session()

@Client.on_message(filters.command('planetdp'))
async def planet(bot, message):
    try:
       split = message.text.split(" ", 1)
       aranacak = split[1].replace(" ", "+")
       url = f"https://planetdp.org/movie/search?title={aranacak}"
       istek = requests.get(url)
       c = BeautifulSoup(istek.content, "lxml")
       b = c.find('div', attrs={"class":"col-md-9 col-sm-9 translate_list-right2"})
       l = b.find("a")
       lnk = l.get("href") 
       urlmovie = f"https://planetdp.org/{lnk}\n" 
       i = requests.get(urlmovie)
       corba = BeautifulSoup(i.content, "lxml")
       text = "" 
       say=0
       for i in corba.findAll('td', attrs={"class":"t-content-one"})[0:]:
           t = i.find("a")
           altyazilar = t.get("href")
           dil = i.find('span', attrs={"itemprop":"subtitleLanguage"}).text
           surum = corba.findAll('td', attrs={"colspan":"9"})[say:]
           sur = surum[0]
           uri = f"https://planetdp.org{altyazilar}"
           log = requests.get(uri)
           co = BeautifulSoup(log.content, "lxml")
           bultoken = co.find('div', attrs={"class":"tebel-scroll"})
           bult = bultoken.find("input")
           LOGGER.info(bult)
           token = bult.get("value")
           bul = co.find('a', attrs={"class":"subButton download_btn_enable"})
           uniquekey = bul.get("rel-tag")
           subid = bul.get("rel-id")
           text += f"**Dil**: {dil}{sur}**Link**: https://planetdp.org{altyazilar}\n\n"
           say+=1
           url = "https://planetdp.org/subtitle/download"
           data = {
               'subtitle_id': subid,
               '_token': token,
               'uniquekey': uniquekey}
           cookies = _global_session.cookies.get_dict()
           request = _global_session.post(
               url="https://planetdp.org/subtitle/download",
               data=data,
               cookies=cookies)
           LOGGER.info(request.content)           
           file_name = "altyazidosyası.rar"
           content = request.content
           with open(file_name, "wb") as dosya:
               dosya.write(content)             
           await message.reply_document(
               document=file_name, 
               caption=text)
           text = ""
    except Exception as e:
        await message.reply_text(e)
