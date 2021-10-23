import os

if bool(os.environ.get("WEBHOOK", False)):
    from Config import Config
else:
    from config import Config
from about import About
from script import Script
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=Translation.START_TEXT.format(update.from_user.mention),
            reply_markup=Script.START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=Translation.HELP_TEXT,
            reply_markup=Script.HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=About.ABOUT_TEXT,
            reply_markup=About.ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    else:
        await update.message.delete()

