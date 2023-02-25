import os
from config import Config
from pyrogram import Client, filters, errors
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQueryResultArticle, \
    InputTextMessageContent, InlineQuery
from pyrogram.enums.parse_mode import ParseMode

@Client.on_message(filters.command('syukle'))
async def _main(_, message):
    if message.reply_to_message:
        button = InlineKeyboardButton("Streamtape'e Yükle", callback_data="uptostreamtape")
        await message.reply_text(
            "Aşağıdaki Butona Tıkla! ",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(button),
        )
    else:
        await message.reply_text("`Bir Video Yanıtla..`")

