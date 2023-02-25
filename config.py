import os
import time

from helper_func.dbhelper import Database as Db
db = Db().setup()

import pyrogram
from pyrogram import Client, enums

botStartTime2 = time.time()

class Config:
    DEF_WATER_MARK_FILE = ""
    ENCODE_DIR = 'encodes'
    APP_ID = os.environ.get("APP_ID", None)
    API_HASH = os.environ.get("API_HASH", None)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 128))
    DOWNLOAD_LOCATION = 'downloads'
    DOWNLOAD_DIR = 'downloads'
    OWNER_ID = os.environ.get("OWNER_ID", '1276627253') 
    DEPO = os.environ.get("DEPO", None)
    SESSION_NAME = os.environ.get("SESSION_NAME", "")
    STREAMTAPE_API_PASS = os.environ.get("STREAMTAPE_API_PASS") 
    STREAMTAPE_API_USERNAME = os.environ.get("STREAMTAPE_API_USERNAME")
    # database uri (mongodb)
    DATABASE_URL = os.environ.get("DATABASE_URL", "")

    PRE_LOG = os.environ.get("PRE_LOG", "")
    STRING_SESSION = os.environ.get('STRING_SESSION', '')
    HTTP_PROXY = os.environ.get("HTTP_PROXY", "")
    MAX_FILE_SIZE = 50000000
    TG_MAX_FILE_SIZE = 4200000000
    DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "")

    userbot = Client(name='userbot', api_id=APP_ID, api_hash=API_HASH, session_string=STRING_SESSION, parse_mode=enums.ParseMode.HTML)
    userbot.start()
    print("Userbot Başlatıldı 4 gb yükleme aktif")
