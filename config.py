import os
import time

from helper_func.dbhelper import Database as Db
db = Db().setup()

import pyrogram
from pyrogram import Client, enums

botStartTime2 = time.time()

class Config:

    ENCODE_DIR = 'encodes'
    APP_ID = os.environ.get("APP_ID", None)
    API_HASH = os.environ.get("API_HASH", None)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
   
    
    DOWNLOAD_DIR = 'downloads'
    OWNER_ID = os.environ.get("OWNER_ID", '1276627253') 
    
    SESSION_NAME = os.environ.get("SESSION_NAME", "")

    # database uri (mongodb)
    DATABASE_URL = os.environ.get("DATABASE_URL", "")

    PRE_LOG = os.environ.get("PRE_LOG", "")
    STRING_SESSION = os.environ.get('STRING_SESSION', '')

    userbot = Client(name='userbot', api_id=APP_ID, api_hash=API_HASH, session_string=STRING_SESSION, parse_mode=enums.ParseMode.HTML)
    userbot.start()
    print("Userbot Başlatıldı 4 gb yükleme aktif")
