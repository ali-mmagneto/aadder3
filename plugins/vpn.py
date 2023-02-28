from pyrogram import Client, filters 
import requests
from unidecode import unidecode
import logging
import os
import subprocess
import asyncio
import json
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

@Client.on_message(filters.command('connect'))
async def connect(client, message):
    connect = await client.send_message(message.chat.id, "Vpn Bağlanıyor..")
    try:
        subprocess.call("apt install openvpn")
        os.chmod("etc/openvpn/pass.txt", 600)
        process = subprocess.Popen(['openvpn', "--config", "etc/openvpn/tr-ist.prod.surfshark.com_udp.ovpn", '--auth-user-pass', 'etc/openvpn/pass.txt'], stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output:
               print(output.strip())
               if("Initialization Sequence Completed") in str(output):
                    await connect.edit_text("Başarıyla Bağlandı.")
                    break
               elif("Failed or something") in str(output):
                    await connect.edit_text("Bağlantı başarısız oldu.")
                    break
    except Exception as e:
        await connect.edit(f"HATA: {e}")
       
 
@Client.on_message(filters.command('disconnect'))
async def disconnect(client, message):
    disconnect = await client.send_message(message.chat.id, "Bağlantı kesiliyor..")
    try:
        os.system("pgrep openvpn | xargs sudo kill -9")
        await disconnect.edit_text("Bağlantı kesildi.")
    except Exception as e:
        await disconnect.edit(f"HATA: {e}")
       
       
@Client.on_message(filters.command('ip'))
async def ip(client, message):
    url = 'http://ipinfo.io/json'
    response = requests.get(url)
    data = response.json()
    IP=data['ip']
    org=data['org']
    city = data['city']
    country=data['country']
    region=data['region']
    ip = 'IP : {4} \nBölge : {1} \nÜlke : {2} \nŞehir : {3} \nOrg : {0}'.format(org,region,country,city,IP)
    await client.send_message(message.chat.id, ip)
