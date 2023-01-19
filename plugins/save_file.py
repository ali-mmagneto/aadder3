from helper_func.tools import execute, clean_up
import time
import os
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from translation import Translation
from config import Config
from pyrogram import Client, filters
from helper_func.progress_bar import progress_bar
from helper_func.dbhelper import Database as Db
from plugins.forcesub import handle_force_subscribe
import re
import json
import requests
from urllib.parse import quote, unquote
db = Db()
DATA = {} 

@Client.on_message(filters.command('ses') & filters.private)
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
        message = message.reply_to_message,
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

@Client.on_message(filters.command('video') & filters.private)
async def save_video(bot, message, cb=False):
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, message)
      if fsub == 400:
        return
    me = await bot.get_me()

    chat_id = message.from_user.id
    start_time = time.time()
    downloading = await bot.send_message(chat_id, '`Indiriliyor.`')
    download_location = await bot.download_media(
        message = message.reply_to_message,
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

@Client.on_message(filters.command('extract') & filters.private)
async def confirm_dwnld(bot, message):
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, message)
      if fsub == 400:
        return
    me = await bot.get_me()
    chat_id = message.from_user.id
    start_time = time.time()
    downloading = await bot.send_message(chat_id, '`İndiriliyor..`')
    download_location = await bot.download_media(
        message = message.reply_to_message,
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

    await bot.edit_message_text(
        text="Processing your file....",
        chat_id = chat_id,
        message_id = downloading.id)

    output = await execute(f"ffprobe -hide_banner -show_streams -print_format json '{download_location}'")
    
    if not output:
        await clean_up(download_location)
        await msg.edit_text("Some Error Occured while Fetching Details...")
        return

    details = json.loads(output[0])
    buttons = []
    DATA[f"{message.chat.id}-{downloading.id}"] = {}
    for stream in details["streams"]:
        mapping = stream["index"]
        stream_name = stream["codec_name"]
        stream_type = stream["codec_type"]
        if stream_type in ("audio", "subtitle"):
            pass
        else:
            continue
        try: 
            lang = stream["tags"]["language"]
        except:
            lang = mapping
        
        DATA[f"{message.chat.id}-{downloading.id}"][int(mapping)] = {
            "map" : mapping,
            "name" : stream_name,
            "type" : stream_type,
            "lang" : lang,
            "location" : download_location
        }
        buttons.append([
            InlineKeyboardButton(
                f"{stream_type.upper()} - {str(lang).upper()}", f"{stream_type}_{mapping}_{message.chat.id}-{downloading.id}"
            )
        ])

    buttons.append([
        InlineKeyboardButton("CANCEL",f"cancel_{mapping}_{message.chat.id}-{downloading.id}")
    ])    

    await bot.edit_message_text(
        text="**Select the Stream to be Extracted...**",
        message_id=downloading.id,
        chat_id = chat_id,
        reply_markup=InlineKeyboardMarkup(buttons)
        )
