import os

from helper_func.dbhelper import Database as Db
db = Db().setup()

import pyrogram
from pyrogram import Client, enums



class Config:

    ENCODE_DIR = os.environ.get("ENCODE_DIR", "encodes") 
    APP_ID = os.environ.get("APP_ID", None)
    API_HASH = os.environ.get("API_HASH", None)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
   
    #comma seperated user id of users who are allowed to use
    #ALLOWED_USERS = [x.strip(' ') for x in os.environ.get('ALLOWED_USERS','1098504493').split(',')]

    DOWNLOAD_DIR = 'downloads'
    OWNER_ID = os.environ.get("OWNER_ID", '1276627253') 
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", '-1001157048481')
    


    PRE_LOG = os.environ.get("PRE_LOG", "")
    STRING_SESSION = os.environ.get('STRING_SESSION', '')

    userbot = Client(name='userbot', api_id=APP_ID, api_hash=API_HASH, session_string=STRING_SESSION, parse_mode=enums.ParseMode.HTML)
    userbot.start()
    print("Userbot Başlatıldı 4 gb yükleme aktif")

