# Coded by :d
import pyrogram
from pyrogram import Client, filters
import os
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from helper_func.thumb import get_thumbnail, get_duration, get_width_height
from helper_func.progress_bar import progress_bar
from config import Config
import time

@Client.on_message(filters.command('rename'))
async def rename(bot, message):
    text = message.text.split(" ", 1)
    file_name = text[1]
    ext = file_name.split('.').pop()
    caption = f"<code>{file_name}</code>"
    start_time = time.time()
    video = f"downloads/{file_name}"
    chat_id = str(message.from_user.id)
    msg = await message.reply_text(
        text="`İşlem Başlatıldı...`")
    await msg.edit("`Indiriliyor..`")
    media = await bot.download_media(
                message = message.reply_to_message,
                file_name = f"{file_name}",
                progress=progress_bar,
                progress_args=("`İndiriliyor...`", msg, start_time))
    splitpath = media.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name =f"downloads/{dow_file_name}"
    os.rename(old_file_name, video)
    if ext in ['mp4','mkv','ts']:
        start_time = time.time()
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
        await msg.edit("`Yükleniyor..`") 
        file_size = os.stat(video).st_size
        if file_size > 2093796556:
            copy = await Config.userbot.send_video(
                chat_id = Config.PRE_LOG,
                progress = progress_bar, 
                progress_args = (
                    'Dosyan Yükleniyor!',
                    msg,
                    start_time
                    ),
                video = video,
                caption = caption,
                duration = duration,
                thumb = thumb,
                width = width,
                height = height,
                supports_streaming=True)
            await bot.copy_message(
                chat_id=message.chat.id, 
                from_chat_id=Config.PRE_LOG, 
                message_id=copy.id)
            await msg.edit("`Başarı ile Tamamlandı...`")
        else:
            await bot.send_video(
                chat_id = message.chat.id,
                progress = progress_bar, 
                progress_args = (
                    'Dosyan Yükleniyor!',
                    msg,
                    start_time
                    ),
                video = video,
                caption = caption,
                duration = duration,
                thumb = thumb,
                width = width,
                height = height,
                supports_streaming=True) 
            await msg.edit("`Başarı ile Tamamlandı...`")
    elif ext in ['jpeg','png','jpg']:
        start_time = time.time()
        await msg.edit("`Yükleniyor..`") 
        await bot.send_photo(
            chat_id = message.chat.id,
            progress = progress_bar, 
            progress_args = (
                'Dosyan Yükleniyor!',
                msg,
                start_time
                ),
            photo = video,
            caption = caption) 
        await msg.edit("`Başarıyla Tamamlandı`")
    elif ext in ['m4a','mp3','aac']:
        title = None
        artist = None
        thumb_image_path = os.path.join(
            Config.DOWNLOAD_DIR,
            chat_id,
            chat_id + ".jpg"
        )
        if os.path.exists(thumb_image_path):
            thumb = thumb_image_path
        else:
            thumb = None
        duration = 0

        metadata = extractMetadata(createParser(video))
        if metadata and metadata.has("title"):
            title = metadata.get("title")
        if metadata and metadata.has("artist"):
            artist = metadata.get("artist")
        if metadata and metadata.has("duration"):
            duration = metadata.get("duration").seconds
        c_time = time.time()  
        await msg.edit("`Yükleniyor..`")  
        await bot.send_audio(
            chat_id=message.chat.id,
            audio=video,
            thumb=thumb,
            caption=caption,
            title=title,
            performer=artist,
            duration=duration,
            progress=progress_bar,
            progress_args=(
                "`Yükleniyor`",
                msg,
                c_time
            )
        )
        await msg.edit("`Başarıyla Tamamlandı`")
    os.remove(video)
