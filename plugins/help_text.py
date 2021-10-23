
# (c) mohdsabahat

#Logging
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

import os
import pyrogram
from translation import Translation
from config import Config
logging.getLogger('pyrogram').setLevel(logging.WARNING)



@pyrogram.Client.on_message(pyrogram.filters.command(["help"]))
async def help_user(bot, update):
    # logger.info(update)
    (update.from_user.id, update.text, "/help")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_TEXT,
        reply_markup=Script.HELP_BUTTON,
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )
@pyrogram.Client.on_message(pyrogram.filters.command(["start"]))
async def start(bot, update):
    # logger.info(update)
    (update.from_user.id, update.text, "/start")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT,
        reply_markup=Script.START_BUTTONS
        
        reply_to_message_id=update.message_id
    )
