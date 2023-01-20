import os
import logging
from config import Config
import time
from helper_func.dbhelper import Database as Db
db = Db().setup()
from pyrogram.raw.all import layer
import pyrogram
from pyrogram import Client, __version__

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    level=logging.INFO)
LOGGER = logging.getLogger(__name__)
botStartTime = time.time()

plugins = dict(root='plugins')

if not os.path.isdir(Config.DOWNLOAD_DIR):
        os.mkdir(Config.DOWNLOAD_DIR)
if not os.path.isdir(Config.ENCODE_DIR):
        os.mkdir(Config.ENCODE_DIR)

class Bot(Client):

    def __init__(self):
        super().__init__(
            name='multibot',
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=plugins
        )

    async def start(self):
        if not os.path.isdir(Config.DOWNLOAD_DIR): os.makedirs(Config.DOWNLOAD_DIR)
        await super().start()
        me = await self.get_me()
        self.username = '@' + me.username
        LOGGER.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}. Premium {me.is_premium}.")
        if Config.OWNER_ID != 0:
            try:
                await self.send_message(text="Karanlığın küllerinden yeniden doğdum.",
                    chat_id=Config.OWNER_ID)
            except Exception as t:
                LOGGER.error(str(t))

    async def stop(self, *args):
        if Config.OWNER_ID != 0:
            texto = f"Son nefesimi verdim.\nÖldüğümde yaşım: {ReadableTime(time.time() - botStartTime)}"
            try:
                await self.send_document(document='log.txt', caption=texto, chat_id=Config.OWNER_ID)
            except Exception as t:
                LOGGER.warning(str(t))
        await super().stop()
        LOGGER.info(msg="App Stopped.")
        exit()

app = Bot()
app.run()
