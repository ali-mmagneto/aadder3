from pyrogram import Client, filters
from unidecode import unidecode
import os
from config import Config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from helper_func.progress_bar import progress_bar
from helper_func.dbhelper import Database as Db
from helper_func.mux import sesekle_vid
from helper_func.thumb import get_thumbnail, get_duration, get_width_height
import time
import logging 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)
from sys import executable

async def dosyasil(dosyaYolu, message, silinecekler):
    for dosya in os.listdir(dosyaYolu):
        text = dosyaYolu
        dosyaYolu = os.path.join(text, dosya)
        try:
            if os.path.isfile(dosyaYolu):
                os.remove(dosyaYolu)
                textim += f"{dosyaYolu}\n"
            elif os.path.isdir(dosyaYolu):
                for i in os.listdir(dosyaYolu):
                    text = f"{dosyaYolu}"
                    dosyaYol = os.path.join(text, i)
                    await message.reply_text(dosyaYol)
                    if os.path.isfile(dosyaYol):
                        textim = f"{dosyaYol}"
                        silinecekler.append(textim)
                    elif os.path.isdir(dosyaYol):
                        for i in os.listdir(dosyaYol):
                            text = f"{dosyaYol}"
                            dosyaYolu = os.path.join(text, i)
                            if os.path.isfile(dosyaYolu):
                                textim = f"{dosyaYolu}"
                                silinecekler.append(textim)
                            else:
                                await message.reply_text("Silemiyom aq..")
        except Exception as hata:
            await message.reply_text(hata)

@Client.on_message(filters.command('diskisil'))
async def deldirecttory(bot, message):
    try:
        silinecekler = []
        text = "DOWNLOADS"
        msg = await message.reply_text("`Siliyorum..`") 
        for dosya in os.listdir(text):
            dosyaYolu = os.path.join(text, dosya)
            try:
                if os.path.isfile(dosyaYolu):
                    textim = f"{dosyaYolu}"
                    silinecekler.append(textim)
                elif os.path.isdir(dosyaYolu):
                    dosyaYolu = await dosyasil(dosyaYolu, message, silinecekler)
            except Exception as hata:
                await message.reply_text(hata)
        for sil in silinecekler:
            await message.reply_text(sil)
            os.remove(sil)
        await msg.edit(f"Dosyaları Başarıyla Silindi..")
        await message.reply_text("Şimdi Botu Resetliyorum..")
        try:
            os.execl(executable, executable, "bot.py")
        except Exception as e:
            await message.reply_text(e)
    except Exception as e:
        await message.reply_text(e) 

@Client.on_message(filters.command('get'))
async def get_directoryyy(bot, message):
    try:
        text = message.text.split(" ", 1)
        if len(text) < 2:
            await bot.send_message(message.chat.id, "Hatalı Kullanım :/ Doğru Kullanım Şu Şekilde:\n\n`/get downloads`") 
            return
        directory = text[1]
        if 1 == 1:
            if not os.listdir(directory):
                await message.reply(f"{directory} klasörünüz boş")
            else:
                dsy = ""
                say = 0
                for files in os.listdir(directory):
                    say += 1
                    dsy = dsy + "  " + str(say) + "-) " + f"`{directory}/{files}`" + '\n'
                await message.reply_text(
                    f"{directory} Klasöründeki Dosyalar." + "\n\n" + dsy + "\n" + str(
                        say) + " Tane Dosya Var.")
    except Exception as e:
        await message.reply_text(e)

@Client.on_message(filters.command('del'))
async def deldirectory(bot, message):
    try:
        text = message.text.split(" ", 1)
        if len(text) < 2:
            await bot.send_message(message.chat.id, "Hatalı Kullanım :/ Doğru Kullanım Şu Şekilde:\n\n`/del downloads`") 
            return
        msg = await message.reply_text("`Siliyorum..`") 
        for files in os.listdir(text[1]):
            os.remove(f"{text[1]}/{files}")
        await msg.edit(f"`{text[1]} Klasörü Başarıyla Silindi..`")
    except Exception as e:
        await message.reply_text(e) 

@Client.on_message(filters.command('get'))
async def get_directory(bot, message):
    try:
        text = message.text.split(" ", 1)
        if len(text) < 2:
            await bot.send_message(message.chat.id, "Hatalı Kullanım :/ Doğru Kullanım Şu Şekilde:\n\n`/get downloads`") 
            return
        directory = text[1]
        if 1 == 1:
            if not os.listdir(directory):
                await message.reply(f"{directory} klasörünüz boş")
            else:
                dsy = ""
                say = 0
                for files in os.listdir(directory):
                    say += 1
                    dsy = dsy + "  " + str(say) + "-) " + f"`{directory}/{files}`" + '\n'
                await message.reply_text(
                    f"{directory} Klasöründeki Dosyalar." + "\n\n" + dsy + "\n" + str(
                        say) + " Tane Dosya Var.")
    except Exception as e:
        await message.reply_text(e)

@Client.on_message(filters.command('delfile'))
async def delfile(bot, message):
    try:
        text = message.text.split(" ", 1)
        if len(text) < 2:
            await bot.send_message(message.chat.id, "Hatalı Kullanım :/ Doğru Kullanım Şu Şekilde:\n\n`/del downloads/RTE Twerk Yapıyor.mp4`") 
            return
        msg = await message.reply_text("`Siliyorum..`") 
        os.remove(f"{text[1]}")
        await msg.edit(f"`{text[1]} Dosyası Başarıyla Silindi..`")
    except Exception as e:
        await message.reply_text(e) 

@Client.on_message(filters.command('getfile'))
async def get_file(bot, message):
    try:
        text = message.text.split(" ", 1)
        if len(text) < 2:
            await bot.send_message(message.chat.id, "Hatalı Kullanım :/ Doğru Kullanım Şu Şekilde:\n\n`/getfile downloads/1676486384.mp4`") 
            return
        video = text[1]
        sent_msg = await message.reply_text("`Dosyayı Getirmeye Çalışıyorum...`")
        start_time = time.time()
        try:
            chat_id = str(message.chat.id)
            duration = get_duration(video)
            thumb_image_path = os.path.join(
                Config.DOWNLOAD_DIR,
                chat_id,
                chat_id + ".jpg"
            )
            if os.path.exists(thumb_image_path):
                thumb = thumb_image_path
            else:
                thumb = get_thumbnail(video, './' + Config.DOWNLOAD_DIR, duration / 4)
            width, height = get_width_height(video)
            file_size = os.stat(video).st_size
            if file_size > 2093796556:
                get_chat = await bot.get_chat(chat_id=Config.PRE_LOG)
                print(get_chat)
                await bot.send_message(Config.PRE_LOG, "2 gb üstüVideo Geliyor.")
                copy = await Config.userbot.send_video(
                        chat_id = Config.PRE_LOG, 
                        progress = progress_bar, 
                        progress_args = (
                            'Dosyan Yükleniyor!',
                            sent_msg,
                            start_time
                            ),
                        duration = duration,
                        thumb = thumb,
                        width = width,
                        height = height,
                        supports_streaming=True,
                        video = video,
                        caption = f"{video}"
                        )
                text = 'Dosyan Başarı İle Yüklendi!\nGeçen Toplam Zaman : {} saniye'.format(round(time.time()-start_time))
                await sent_msg.edit(text)
                await bot.copy_message(
                    chat_id=message.chat.id, 
                    from_chat_id=Config.PRE_LOG, 
                    message_id=copy.id)
            else:
                copy = await bot.send_video(
                        chat_id = message.chat.id, 
                        progress = progress_bar, 
                        progress_args = (
                            'Dosyan Yükleniyor!',
                            sent_msg,
                            start_time
                            ),
                        duration = duration,
                        thumb = thumb,
                        width = width,
                        height = height,
                        supports_streaming=True,
                        video = video,
                        caption = f"{video}")
                text = 'Dosyan Başarı İle Yüklendi!\nGeçen Toplam Zaman : {} saniye'.format(round(time.time()-start_time))
                await sent_msg.edit(text)
        except Exception as f:
            await message.reply_text(f)        
    except Exception as e:
        await message.reply_text(e)
