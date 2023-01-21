from pyrogram import Client, filters
from config import Config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply 

@Client.on_message(filters.command('rename'))
async def rename(bot, message):
    chat_id = message.chat.id
    message = message.reply_to_message
    msg = await bot.ask(chat_id, '`Yeni Video İsmini Yazar mısın?`', filters=filters.text) 
    new_name = msg.text
    print(new_name)
