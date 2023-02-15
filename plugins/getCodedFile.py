from pyrogram import Client, filters
from unidecode import unidecode
import os


@Client.on_message(filters.command('get'))
async def get_directory(bot, message):
    try:
        mes = unidecode(message.text).split()
        if len(mes) < 2:
            await bot.send_message(message.chat.id, "Hatalı Kullanım :/ Doğru Kullanım Şu Şekilde:\n\n`/get downloads`") 
            return
        directory = mes[1]
        if 1 == 1:
            if not os.listdir(directory):
                await message.reply(f"{directory} klasörünüz boş")
            else:
                for files in os.listdir(directory):
                    say = say + 1
                    dsy = dsy + "  " + str(say) + "-) " + files + '\n'
                await message.reply_text(
                    f"{directory} Klasöründeki Dosyalar." + "\n\n" + dsy + "\n" + str(
                        say) + "Tane Dosya Var.")
    except Exception as e:
        await message.reply_text(e)
