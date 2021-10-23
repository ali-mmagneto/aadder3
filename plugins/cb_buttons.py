import os

if bool(os.environ.get("WEBHOOK", False)):
    from Config import Config
else:
    from config import Config

from translation import Translation
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=Translation.START_TEXT.format(update.from_user.mention),
            reply_markup=Translation.START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=Translation.HELP_TEXT,
            reply_markup=Translation.HELP_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()
