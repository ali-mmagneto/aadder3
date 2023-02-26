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


@Client.on_message(filters.command('del'))
async def deldirectory(bot, message):
    try:
        msg = await message.reply_text("`Siliyorum..`") 
        text = message.text.split(" ", 1)
        if len(text) < 2:
            await bot.send_message(message.chat.id, "Hatalı Kullanım :/ Doğru Kullanım Şu Şekilde:\n\n`/del downloads`") 
            return
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
        msg = await message.reply_text("`Siliyorum..`") 
        text = message.text.split(" ", 1)
        if len(text) < 2:
            await bot.send_message(message.chat.id, "Hatalı Kullanım :/ Doğru Kullanım Şu Şekilde:\n\n`/del downloads/RTE Twerk Yapıyor.mp4`") 
            return
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
