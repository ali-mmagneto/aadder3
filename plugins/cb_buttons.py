
from pyrogram import filters
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from script import Script

from helper_func.progress_bar import PRGRS
from helper_func.tools import clean_up
from helper_func.download import download_file, DATA
from helper_func.ffmpeg import extract_audio, extract_subtitle


import asyncio
import json
import re
import os
from logging import getLogger, WARNING
from os import remove as osremove, walk, path as ospath, rename as osrename
from time import time, sleep
from pyrogram.errors import FloodWait, RPCError
from PIL import Image
from threading import RLock
from pyrogram.types import Message
import shutil
import time
from datetime import datetime

from config import Config
from pyrogram.enums import MessageEntityType, ChatAction
from database.database import db
from translation import Translation

from pyrogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, MessageNotModified
from helper_func.progress_bar import progress_bar, humanbytes
from helper_func.ffmpeg import generate_screen_shots, VideoThumb, VideoMetaData, VMMetaData, DocumentThumb, \
    AudioMetaData
from helper_func.utils import remove_urls, remove_emoji

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

 
@Client.on_callback_query()
async def cb_handlers(c: Client, cb: "types.CallbackQuery"):
    user_id = cb.from_user.id
    message = cb.message
    if cb.data == "home":
        await cb.answer()
        await message.edit_text(
            text=Translation.START_TEXT.format(cb.from_user.mention),
            reply_markup=Translation.START_BUTTONS,
            disable_web_page_preview=True
        )
    elif cb.data == "help":
        await cb.answer()
        await message.edit_text(
            text=Translation.HELP_TEXT,
            reply_markup=Translation.HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif cb.data == "login🔑":
        await cb.answer()
        await Login(c, message)
    elif cb.data == "Settings":
        await cb.answer()
        await Settings(message)
    elif cb.data == "showThumbnail":
        thumbnail = await db.get_thumbnail(user_id)
        if not thumbnail:
            await cb.answer("Herhangi bir thumbnail ayarlamadınız!", show_alert=True)
        else:
            await cb.answer()
            await c.send_photo(message.chat.id, thumbnail, "Ayarlı Thumbnail",
                               reply_markup=types.InlineKeyboardMarkup([[
                                   types.InlineKeyboardButton("Sil",
                                                              callback_data="deleteThumbnail")
                               ]]))
    elif cb.data == "deleteThumbnail":
        await db.set_thumbnail(user_id, None)
        await cb.answer("Başarıyla silindi.", show_alert=True)
        await message.delete(True)
    elif cb.data == "setThumbnail":
        await cb.answer(Translation.THUMBNAIL_TEXT, show_alert=True)
    elif cb.data == "triggerGenSS":
        await cb.answer()
        generate_ss = await db.get_generate_ss(user_id)
        if generate_ss:
            await db.set_generate_ss(user_id, False)
        else:
            await db.set_generate_ss(user_id, True)
        await Settings(message)
    elif cb.data == "triggerGenSample":
        await cb.answer()
        generate_sample_video = await db.get_generate_sample_video(user_id)
        if generate_sample_video:
            await db.set_generate_sample_video(user_id, False)
        else:
            await db.set_generate_sample_video(user_id, True)
        await Settings(message)
    elif cb.data == "setCaption":
        await cb.answer()
        caption = await db.get_caption(user_id)
        if caption:
            await db.set_caption(user_id, False)
        else:
            await db.set_caption(user_id, True)
        await Settings(message)
    elif cb.data == "aria2":
        await cb.answer()
        aria2 = await db.get_aria2(user_id)
        if aria2:
            await db.set_aria2(user_id, False)
        else:
            await db.set_aria2(user_id, True)
        await Settings(message)
    elif cb.data == "triggerUploadMode":
        upload_as_doc = await db.get_upload_as_doc(user_id)
        if upload_as_doc:
            await cb.answer("Video olarak yüklenecektir.", show_alert=True)
            await db.set_upload_as_doc(user_id, False)
        else:
            await cb.answer("Dosya olarak yüklenecektir.", show_alert=True)
            await db.set_upload_as_doc(user_id, True)
        await Settings(message)
    elif cb.data == "notifon":
        notif = await db.get_notif(user_id)
        if notif:
            await cb.answer("Bot bildirimleri kapatıldı.", show_alert=True)
            await db.set_notif(user_id, False)
        else:
            await cb.answer("Bot bildirimleri etkinleştirildi.", show_alert=True)
            await db.set_notif(user_id, True)
        await Settings(message)
    elif "reset" in cb.data:
        await db.delete_user(user_id)
        await db.add_user(user_id)
        await cb.answer("Ayarlar Başarıyla Sıfırlandı!", show_alert=True)
        await Settings(message)
    elif "blockFileExtensions" in cb.data:
        await cb.answer()
        await Filters(cb)
    elif cb.data.startswith("set_filter_"):
        data_load = await db.get_blocked_exts(user_id)
        get_cb_data = cb.data.split("_", 2)[2]
        if get_cb_data == "default":
            data_load = ["webm", "3gp", "m4a", "mp4"]
            await cb.answer(
                "Tüm Filtreler Varsayılan Olarak Değiştirildi!",
                show_alert=True)
        else:
            await cb.answer()
            if get_cb_data not in data_load:
                data_load.append(get_cb_data)
            elif get_cb_data in data_load:
                data_load.remove(get_cb_data)
        await db.set_blocked_exts(id=user_id, blocked_exts=data_load)
        await Filters(cb)
    elif cb.data == "close":
        await message.delete(True)
    elif "|" in cb.data:
        await yt_dlp_call_back(c, cb)
    elif "=" in cb.data:
        await ddl_call_back(c, cb)
    else:
        await message.delete(True)

@Client.on_callback_query()
async def cb_handler(client, query):
    if query.data == "close": 
        await query.message.delete()  
        await query.answer(
                "Cancelled...",
                show_alert=True
            ) 


    elif query.data.startswith('audio'):
        await query.answer()
        try:
            stream_type, mapping, keyword = query.data.split('_')
            data = DATA[keyword][int(mapping)]
            await extract_audio(client, query.message, data)
        except:
            await query.message.edit_text("Hata Oldu")   


    elif query.data.startswith('subtitle'):
        await query.answer()
        try:
            stream_type, mapping, keyword = query.data.split('_')
            data = DATA[keyword][int(mapping)]
            await extract_subtitle(client, query.message, data)
        except:
            await query.message.edit_text("**Hata Oldu**")  


    elif query.data.startswith('cancel'):
        try:
            query_type, mapping, keyword = query.data.split('_')
            data = DATA[keyword][int(mapping)]   
            await query.message.edit_text("**Iptal Edildi...**")
            await query.answer(
                "Iptal Ediliyor...",
                show_alert=True
            ) 
        except:
            await query.answer() 
            await query.message.edit_text("**Hata Oldu**")        
