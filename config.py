import os
import time
import re
import os
from os import environ
from dotenv import load_dotenv
from pyrogram import Client, __version__
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, enums
import string
import random
import re
import os
from os import environ
from dotenv import load_dotenv
import time, requests
from pyrogram import __version__
from platform import python_version

from helper_func.dbhelper import Database as Db
db = Db().setup()

import pyrogram
from pyrogram import Client, enums
import logging
import logging.config

import logging

logging.basicConfig(
    format='%(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'),
              logging.StreamHandler()],
    level=logging.INFO
)

LOGGER = logging

botStartTime2 = time.time()
if os.path.exists('config.env'):
    load_dotenv('config.env')

id_pattern = re.compile(r'^.\d+$') 

def is_enabled(value:str):
    return bool(str(value).lower() in ["true", "1", "e", "d"])

def get_config_from_url():
    CONFIG_FILE_URL = os.environ.get('CONFIG_FILE_URL', None)
    try:
        if len(CONFIG_FILE_URL) == 0: raise TypeError
        try:
            res = requests.get(CONFIG_FILE_URL)
            if res.status_code == 200:
                LOGGER.info("Config uzaktan alındı. Status 200.")
                with open('config.env', 'wb+') as f:
                    f.write(res.content)
                    f.close()
            else:
                LOGGER.error(f"Failed to download config.env {res.status_code}")
        except Exception as e:
            LOGGER.error(f"CONFIG_FILE_URL: {e}")
    except TypeError:
        pass

get_config_from_url()
if os.path.exists('config.env'): load_dotenv('config.env')

id_pattern = re.compile(r'^.\d+$')

LOGGER.info("--- CONFIGS STARTS HERE ---")


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
    if STRING_SESSION != 0:
        userbot = Client(name='userbot', api_id=APP_ID, api_hash=API_HASH, session_string=STRING_SESSION, parse_mode=enums.ParseMode.HTML)
        userbot.start()
        print("Userbot Başlatıldı 4 gb yükleme aktif")
