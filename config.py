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
from helper_func.thumb import ReadableTime
from pyrogram import Client, __version__
botStartTime = time.time()

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
    if len(STRING_SESSION) != 0:
        if 1 == 1:

            def __init__(self):
                userbot = Client(
                    name='multivideobot',
                    api_id=APP_ID,
                    api_hash=API_HASH,
                    session_name=STRING_SESSION,
                    workers=343,
                    sleep_threshold=5
                )

            async def start(self):
                await super().start()
                owner = await self.get_chat(OWNER_ID)
                me = await self.get_me()
                self.username = '@' + me.username
                LOGGER.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}. Premium {me.is_premium}.")
                if OWNER_ID != 0:
                    try:
                        await self.send_message(text="userbot Karanlığın küllerinden yeniden doğdum.",
                            chat_id=OWNER_ID)
                    except Exception as t:
                        LOGGER.error(str(t))

            async def stop(self, *args):
                if OWNER_ID != 0:
                    texto = f"Son nefesimi verdim.\nÖldüğümde yaşım: {ReadableTime(time.time() - botStartTime)}"
                    try:
                       await self.send_document(document='log.txt', caption=texto, chat_id=OWNER_ID)
                    except Exception as t:
                        LOGGER.warning(str(t))
                await super().stop()
                LOGGER.info(msg="App Stopped.")
                exit()

            userbot.run()
