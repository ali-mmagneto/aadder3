from pyrogram import Client, filters
from config import Config

@Client.on_message(filters.command('rename')
async def rename(bot, message):
    message = message.reply_to_message
    msg = await bot.send_message("yeni Video ismini yaz")
    msg_reply = msg.get_reply()
    new_name = msg_reply.text
    print(new_name)
