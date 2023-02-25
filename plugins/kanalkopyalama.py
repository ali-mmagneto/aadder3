from pyrogram import Client, filters
import random
import asyncio
from unidecode import unidecode
import time
import math 
PRGRS = {}
import os
import time
import ffmpeg
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import asyncio
from subprocess import check_output
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import logging

from helper_func.thumb import get_thumbnail, get_duration, get_width_height
from helper_func.progress_bar import progress_bar, humanbytes

async def copy(bot, message, id, son_id, kanal_id, text1):
    try:
        if int(id) > int(son_id):
            await bot.send_message(message.chat.id, "`İşlem Tamamlandı`")
        else:
            film_kanal = await bot.get_chat(chat_id=kanal_id)
            print(film_kanal)
            await bot.copy_message(
                chat_id=Config.DEPO, 
                from_chat_id=kanal_id, 
                message_id=int(id))
            await filmdongu(bot, message, id, son_id, kanal_id, text1)
    except Exception as e:
        await message.reply_text(e)

async def gizlicopy(bot, message, id, son_id, kanal_id, text1, sayi):
    try:
        if int(id) > int(son_id):
            await text1.edit("`İşlem Tamamlandı`")
            await sayi.edit("`İşlem Tamamlandı..`")
        else:
            await sayi.edit(f"`{id}. Mesaj Kopyalanıyor...`")
            film_kanal = await userbot.get_chat(chat_id=kanal_id)
            koruma = film_kanal.has_protected_content
            print(film_kanal.has_protected_content)
            if film_kanal.has_protected_content == True:
                chat_id = str(message.chat.id)
                film_kanal = await userbot.get_chat(chat_id=kanal_id)
                print(film_kanal)
                msg = await userbot.get_messages(kanal_id, id)
                start_time = time.time()
                
                if msg.video:
                    caption = msg.caption
                    video = await userbot.download_media(
                        message = msg,
                        progress=progress_bar,
                        progress_args=("`İndiriliyor...`", text1, start_time))
                    duration = get_duration(video)
                    thumb_image_path = os.path.join(
                        Config.DOWNLOAD_DIR,
                        chat_id,
                        chat_id + ".jpg"
                    )
                    if os.path.exists(thumb_image_path):
                        thumb = thumb_image_path
                    else:
                        thumb = get_thumbnail(video, './' + DOWNLOAD_DIR, duration / 4)
                    width, height = get_width_height(video)
                    file_size = os.stat(video).st_size
                    if file_size > 2093796556:
                        await userbot.send_video(
                            chat_id = Config.DEPO,
                            progress = progress_bar, 
                            progress_args = (
                                'Dosyan Yükleniyor!',
                                text1,
                                start_time
                                ),
                            video = video,
                            caption = caption,
                            duration = duration,
                            thumb = thumb,
                            width = width,
                            height = height,
                            supports_streaming=True)
                        await filmdongug(bot, message, id, son_id, kanal_id, text1, sayi)
                    else:
                        await bot.send_video(
                            chat_id = Config.DEPO,
                            progress = progress_bar, 
                            progress_args = (
                                'Dosyan Yükleniyor!',
                                text1,
                                start_time
                                ),
                            video = video,
                            caption = caption,
                            duration = duration,
                            thumb = thumb,
                            width = width,
                            height = height,
                            supports_streaming=True)
                        await filmdongug(bot, message, id, son_id, kanal_id, text1, sayi)
                elif msg.document:
                    caption = msg.caption
                    video = await userbot.download_media(
                        message = msg,
                        progress=progress_bar,
                        progress_args=("`İndiriliyor...`", text1, start_time))
                    file_size = os.stat(video).st_size
                    if file_size > 2093796556:
                        await userbot.send_document(
                            chat_id = Config.DEPO, 
                            document = video, 
                            caption = caption)
                        await filmdongug(bot, message, id, son_id, kanal_id, text1, sayi)
                    else:
                        await bot.send_document(
                            chat_id = Config.DEPO, 
                            document = video, 
                            caption = caption)
                        await filmdongug(bot, message, id, son_id, kanal_id, text1, sayi)
                elif msg.text:
                    text = msg.text
                    await userbot.send_message(
                        chat_id = Config.DEPO, 
                        text = text) 
                    await filmdongug(bot, message, id, son_id, kanal_id, text1, sayi)
                elif msg.photo:
                    caption = msg.caption
                    photo = await userbot.download_media(
                                message = msg)
                    await userbot.send_photo(
                        chat_id = Config.DEPO, 
                        photo = photo, 
                        caption = caption) 
                    await filmdongug(bot, message, id, son_id, kanal_id, text1, sayi)
                else:
                    await bot.send_message(message.chat.id, f"`{id}. Mesajın ne tür olduğunu bilmiyorum özür dilerim 😭😭`")
                    await filmdongug(bot, message, id, son_id, kanal_id, text1, sayi)
            else:
                film_kanal = await userbot.get_chat(chat_id=kanal_id)
                print(film_kanal)
                await userbot.copy_message(
                    chat_id=Config.DEPO, 
                    from_chat_id=kanal_id, 
                    message_id=int(id))
                await filmdongug(bot, message, id, son_id, kanal_id, text1, sayi)
    except Exception as e:
        await message.reply_text(e)

async def filmdongu(bot, message, id, son_id, kanal_id, text1):
    try:
        id += 1
        await asyncio.sleep(5)
        await copy(bot, message, id, son_id, kanal_id, text1)
    except Exception as e:
        await message.reply_text(e)

async def filmdongug(bot, message, id, son_id, kanal_id, text1, sayi):
    try:
        id += 1
        await asyncio.sleep(5)
        await gizlicopy(bot, message, id, son_id, kanal_id, text1, sayi)
    except Exception as e:
        await message.reply_text(e)

@Client.on_message(filters.command("film") & filters.private)
async def filmg(bot, message):
    try:
        text = unidecode(message.text).split()
        if len(text) < 4:
            await message.reply_text("Hatalı Kullanım")
            return
        kanal_id = str(text[1])
        id = int(text[2])
        son_id = text[3]
        print(kanal_id) 
        print(id) 
        print(son_id) 
        sayi = await bot.send_message(message.chat.id, f"{kanal_id} {id} {son_id}")
        text1 = await bot.send_message(
            chat_id=message.chat.id,
            text="`Filmleri Kopyalıyorum Bekle`")
        await filmdongu(bot, message, id, son_id, kanal_id, text1)
    except Exception as e:
        await message.reply_text(e)

@Client.on_message(filters.command("gizlifilm") & filters.private)
async def filmgg(bot, message):
    try:
        text = unidecode(message.text).split()
        if len(text) < 4:
            await message.reply_text("Hatalı Kullanım")
            return
        kanal_id = str(text[1])
        id = int(text[2])
        son_id = text[3]
        print(kanal_id) 
        print(id) 
        print(son_id) 
        sayi = await bot.send_message(message.chat.id, f"@{kanal_id} {id} {son_id}")
        text1 = await bot.send_message(
            chat_id=message.chat.id,
            text="`Filmleri Kopyalıyorum Bekle`")
        await filmdongug(bot, message, id, son_id, kanal_id, text1, sayi)
    except Exception as e:
        await message.reply_text(e)
