
import time
import os

from translation import Translation
from config import Config
from pyrogram import Client, filters
from helper_func.progress_bar import progress_bar
from helper_func.dbhelper import Database as Db
from plugins.forcesub import handle_force_subscribe
import re
import requests
from urllib.parse import quote, unquote
db = Db()

@Client.on_message(filters.private)
async def save_doc(bot, message, cb=False):
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, message)
      if fsub == 400:
        return
    me = await bot.get_me()
    chat_id = message.from_user.id
    start_time = time.time()
    downloading = await bot.send_message(chat_id, '`İndiriliyor..`')
    download_location = await bot.download_media(
        message = message,
        file_name = Config.DOWNLOAD_DIR+'/',
        progress = progress_bar,
        progress_args = (
            'Başlatılıyor',
            downloading,
            start_time
        )
    )

    if download_location is None:
        return bot.edit_message_text(
            text = 'Indirme Bașarısız!',
            chat_id = chat_id,
            message_id = downloading.id
        )

    await bot.edit_message_text(
        text = Translation.DOWNLOAD_SUCCESS.format(round(time.time()-start_time)),
        chat_id = chat_id,
        message_id = downloading.id
    )

    tg_filename = os.path.basename(download_location)
    try:
        og_filename = message.document.filename
    except:
        og_filename = False

    if og_filename:
        #os.rename(Config.DOWNLOAD_DIR+'/'+tg_filename,Config.DOWNLOAD_DIR+'/'+og_filename)
        save_filename = og_filename
    else :
        save_filename = tg_filename

    ext = save_filename.split('.').pop()
    filename = str(round(start_time))+'.'+ext

    if ext in ['aac','mp3','m4a']:
        os.rename(Config.DOWNLOAD_DIR+'/'+tg_filename,Config.DOWNLOAD_DIR+'/'+filename)
        db.put_sub(chat_id, filename)
        if db.check_video(chat_id):
            text = 'Ses Dosyası Başarıyla Yüklendi.\n\n /sesekle komutu ile ișleme bașlayabilirsin.'
        else:
            text = 'Ses Dosyası Yüklendi.\nŞimdi Video Dosyasını yolla!'

        await bot.edit_message_text(
            text = text,
            chat_id = chat_id,
            message_id = downloading.id
        )

    elif ext in ['mp4','mkv']:
        os.rename(Config.DOWNLOAD_DIR+'/'+tg_filename,Config.DOWNLOAD_DIR+'/'+filename)
        db.put_video(chat_id, filename, save_filename)
        if db.check_sub(chat_id):
            text = 'Video Dosyası Başarı ile İndirildi.\n\n /sesekle komutu ile ișleme bașlayabilirsin.'
        else :
            text = 'Video Dosyası Başarı İle İndirildi.\nŞimdi Ses Dosyasını Yolla!'
        await bot.edit_message_text(
            text = text,
            chat_id = chat_id,
            message_id = downloading.id
        )

    else:
        text = Translation.UNSUPPORTED_FORMAT.format(ext)+f'\nFile = {tg_filename}'
        await bot.edit_message_text(
            text = text,
            chat_id = chat_id,
            message_id = downloading.id
        )
        os.remove(Config.DOWNLOAD_DIR+'/'+tg_filename)

@Client.on_message(filters.video & filters.private)
async def save_video(bot, message, cb=False):
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, message)
      if fsub == 400:
        return
    me = await bot.get_me()

    chat_id = message.from_user.id
    start_time = time.time()
    downloading = await bot.send_message(chat_id, 'Dosyan Indiriliyor!')
    download_location = await bot.download_media(
        message = message,
        file_name = Config.DOWNLOAD_DIR+'/',
        progress = progress_bar,
        progress_args = (
            'Initializing',
            downloading,
            start_time
            )
        )

    if download_location is None:
        return bot.edit_message_text(
            text = 'İndirme Başarısız!',
            chat_id = chat_id,
            message_id = downloading.id
        )

    await bot.edit_message_text(
        text = Translation.DOWNLOAD_SUCCESS.format(round(time.time()-start_time)),
        chat_id = chat_id,
        message_id = downloading.id
    )

    tg_filename = os.path.basename(download_location)
    try:
        og_filename = message.document.filename
    except:
        og_filename = False
    
    if og_filename:
        save_filename = og_filename
    else :
        save_filename = tg_filename
    
    ext = save_filename.split('.').pop()
    filename = str(round(start_time))+'.'+ext
    os.rename(Config.DOWNLOAD_DIR+'/'+tg_filename,Config.DOWNLOAD_DIR+'/'+filename)
    
    db.put_video(chat_id, filename, save_filename)
    if db.check_sub(chat_id):
        text = 'Video Dosyası Başarı İle İndirildi. \n\n /sesekle komutu ile ișleme bașlayabilirsin.'
    else :
        text = 'Video Dosyası Başarı İle İndirildi.\nŞimdi Ses Dosyasını Yolla!'
    await bot.edit_message_text(
            text = text,
            chat_id = chat_id,
            message_id = downloading.id
            )
