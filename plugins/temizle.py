import os
from pyrogram import Client, filters

@Client.on_message(filters.command('diskd'))
async def disksil(bot, message):
    try:
        silkomut = "rm -rf downloads"
        try:
            os.system(silkomut)
            await message.reply_text("Dosyalar Silindi..")
        except Exception as e:
            await message.reply_text("silemedim") 
        downloadskomut = "mkdir downloads" 
        try:
            os.system(downloadskomut)
            await message.reply_text("downloads klasörü tekrar oluşturuldu") 
        except Exception as e:
            await message.reply_text(e)
    except Exception as e:
        await message.reply_text(e)
