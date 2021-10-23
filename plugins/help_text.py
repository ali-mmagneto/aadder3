
# (c) Shrimadhav uk | @Tellybots_4u

#Logging
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)
import os

import pyrogram
from help import Help
from script import Script
from about import About
from config import Config
logging.getLogger('pyrogram').setLevel(logging.WARNING)

@pyrogram.Client.on_message(pyrogram.filters.command(["help"]))
async def help_user(bot, update):
    # logger.info(update)
    (update.from_user.id, update.text, "/help")
    await bot.send_message(
        chat_id=update.chat.id,
        text=Help.HELP_TEXT,
        reply_markup=Help.HELP_BUTTONS,
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )
@pyrogram.Client.on_message(pyrogram.filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=Script.START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=Script.START_BUTTONS
    )
@pyrogram.Client.on_message(pyrogram.filters.command(["about"]))
async def get_me_info(bot, update):
    # logger.info(update)
    (update.from_user.id, update.text, "/about")
    chat_id = str(update.from_user.id)
    chat_id, plan_type, expires_at = GetExpiryDate(chat_id)
    await bot.send_message(
        chat_id=update.chat.id,
        text=About.ABOUT_TEXT,
        reply_markup=About.ABOUT_BUTTONS,
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )
