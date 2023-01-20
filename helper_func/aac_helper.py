import os
import time
import shutil
from plugins.aac import aquee
from config import Config
from pyrogram.types import Message
from helper_func.thumb import encode, get_codec, get_thumbnail, get_duration, get_width_height
from helper_func.progress_bar import progress_bar
from pyrogram.errors import FloodWait, MessageNotModified, MessageIdInvalid
from config import Config

async def on_task_complete(bot, message: Message):
    del aquee[0]
    if len(aquee) > 0:
        await add_task(bot, aquee[0])


async def add_task(bot, message):
    try:
        user_id = str(message.from_user.id)
        c_time = time.time()
        random = str(c_time)

        if message.reply_to_message.video:
             file_name = message.reply_to_message.video.file_name
        elif message.reply_to_message.document:
             file_name = message.reply_to_message.document.file_name
        elif message.reply_to_message.audio:
             file_name = message.reply_to_message.audio.file_name
        else:
             file_name = None

        if file_name is None:
            file_name = user_id

        msg = await message.reply_text("`Videon Indiriliyor...`", quote=True)
        path = os.path.join(
            Config.DOWNLOAD_DIR,
            user_id,
            random,
            file_name
        )
        filepath = await message.download(
            file_name=path,
            progress=progress_bar,
            progress_args=("`İndiriliyor...`", msg, c_time))
        await msg.edit("`🟣 Video Kodlanıyor... 🟣\n\n⚙ Motor: FFMPEG\n\n#kodlama`")
        new_file = await encode(filepath)
        if new_file:
            await msg.edit("`🟢 Video Kodlandı, Veriler Alınıyor... 🟢`")
            await handle_upload(bot, new_file, message, msg, random)
            await msg.edit_text("`Başarıyla Tamamlandı!`")
        else:
            await message.reply_text("<code>Dosyanızı kodlarken bir şeyler ters gitti.</code>")
            os.remove(filepath)
    except MessageNotModified:
        pass
    except MessageIdInvalid:
        await msg.edit_text('İndirme İptal!')
    except FloodWait as e:
        print(f"Sleep of {e.value} required by FloodWait ...")
        time.sleep(e.value)
    except Exception as e:
        await msg.edit_text(f"<code>{e}</code>")
    await on_task_complete(bot, message)


async def handle_upload(bot, new_file, message, msg, random):
    user_id = str(message.from_user.id)
    path = os.path.join(
        Config.DOWNLOAD_DIR,
        user_id,
        random
    )
    thumb_image_path = os.path.join(
        Config.DOWNLOAD_DIR,
        user_id,
        user_id + ".jpg"
    )
    # Variables
    c_time = time.time()
    filename = os.path.basename(new_file)
    duration = get_duration(new_file)
    width, height = get_width_height(new_file)
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    else:
        thumb = get_thumbnail(new_file, path, duration / 4)

    audio_codec = get_codec(new_file, channel='a:0')

    caption_str = ""
    caption_str += "<code>"
    caption_str += filename
    caption_str += "</code>"

    if message.caption is not None:
        caption = message.caption
    else:
        caption = caption_str
    
    # Upload
    get_chat = await bot.get_chat(chat_id=PRE_LOG)
    print(get_chat) 
    file_size = os.stat(new_file).st_size
    if file_size > 2093796556:
        try:
            await bot.send_message(Config.PRE_LOG, "2 gb üstü video geliyor..")
            video = await Config.userbot.send_video(
                PRE_LOG,
                new_file,
                supports_streaming=True,
                caption=caption,
                thumb=thumb,
                duration=duration,
                width=width,
                height=height,
                progress=progress_bar,
                progress_args=("`Yükleniyor...`", msg, c_time)
            )
            await bot.copy_message(
                chat_id=user_id, 
                from_chat_id=Config.PRE_LOG, 
                message_id=video.id)
            if not audio_codec:
                await video.reply_text("`⚪ Bu videonun sesi yoktu ama yine de kodladım.\n\n#bilgilendirme`", quote=True)
        except FloodWait as e:
            print(f"Sleep of {e.value} required by FloodWait ...")
            time.sleep(e.value)
        except MessageNotModified:
            pass
        try:
            shutil.rmtree(path)
            if thumb_image_path is None:
               os.remove(thumb)
        except:
            pass
    else:
        try:
            video = await bot.send_video(
                user_id,
                new_file,
                supports_streaming=True,
                caption=caption,
                thumb=thumb,
                duration=duration,
                width=width,
                height=height,
                progress=progress_for_pyrogram,
                progress_args=("`Yükleniyor...`", msg, c_time)
            )
            if not audio_codec:
                await video.reply_text("`⚪ Bu videonun sesi yoktu ama yine de kodladım.\n\n#bilgilendirme`", quote=True)
        except FloodWait as e:
            print(f"Sleep of {e.value} required by FloodWait ...")
            time.sleep(e.value)
        except MessageNotModified:
            pass
        try:
            shutil.rmtree(path)
            if thumb_image_path is None:
               os.remove(thumb)
        except:
            pass     
