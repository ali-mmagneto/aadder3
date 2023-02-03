import os
import time
import shutil
import re
import asyncio
from plugins.aac import aquee
from config import Config
from pyrogram.types import Message
from helper_func.thumb import get_codec, get_thumbnail, get_duration, get_width_height
from helper_func.progress_bar import progress_bar
from pyrogram.errors import FloodWait, MessageNotModified, MessageIdInvalid
from config import Config

progress_pattern = re.compile(
    r'(frame|fps|size|time|bitrate|speed)\s*\=\s*(\S+)'
)

def parse_progress(line):
    items = {
        key: value for key, value in progress_pattern.findall(line)
    }
    if not items:
        return None
    return items

async def readlines(stream):
    pattern = re.compile(br'[\r\n]+')

    data = bytearray()
    while not stream.at_eof():
        lines = pattern.split(data)
        data[:] = lines.pop(-1)

        for line in lines:
            yield line

        data.extend(await stream.read(1024))

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

        msg = await message.reply_to_message.reply_text("`Videon Indiriliyor...`", quote=True)
        path = os.path.join(
            Config.DOWNLOAD_DIR,
            user_id,
            random,
            file_name
        )
        filepath = await message.reply_to_message.download(
            file_name=path,
            progress=progress_bar,
            progress_args=("`İndiriliyor...`", msg, c_time))
        await msg.edit("`Video Kodlanıyor...`")
        new_file = await encode(msg, filepath)
        if new_file:
            await msg.edit("`Yükleniyor`")
            await handle_upload(bot, new_file, message, msg, random)
            await msg.edit_text(f"`{file_name} Tamamlandı!`")
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
        pass
    await on_task_complete(bot, message)



async def handle_upload(bot, new_file, message, msg, random):
    user_id = str(message.chat.id)
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
    file_size = os.stat(new_file).st_size
    if file_size > 2093796556:
        try:
            get_chat = await bot.get_chat(chat_id=Config.PRE_LOG)
            print(get_chat)
            await bot.send_message(Config.PRE_LOG, "2 gb üstü video geliyor..")
            video = await Config.userbot.send_video(
                Config.PRE_LOG,
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
                progress=progress_bar,
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

async def encode(msg, filepath):
    start = time.time()
    path, extension = os.path.splitext(filepath)
    file_name = os.path.basename(path)
    encode_dir = os.path.join(
        Config.ENCODE_DIR,
        file_name
    )
    output_filepath = encode_dir + '.[TR]' + '.mp4'
    assert (output_filepath != filepath)
    if os.path.isfile(output_filepath):
        print('"{}" Atlanıyor: dosya zaten var'.format(output_filepath))
    print(filepath)

    # Get the audio and subs channel codec
    audio_codec = get_codec(filepath, channel='a:0')

    if not audio_codec:
        audio_opts = '-c:v copy'
    elif audio_codec[0] in 'aac':
        audio_opts = '-c:v copy'
    else:
        audio_opts = '-c:a aac -c:v copy'

    command = ['ffmpeg', '-y', '-i', filepath]
    command.extend(audio_opts.split())
    proc = await asyncio.create_subprocess_exec(
        *command, output_filepath,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await asyncio.wait([
            read_stdera(start, msg, proc),
            proc.wait(),
        ])
    await proc.communicate()
    return output_filepath


async def read_stdera(start, msg, proc):
    async for line in readlines(proc.stderr):
            line = line.decode('utf-8')
            progress = parse_progress(line)
            if progress:
                #Progress bar logic
                now = time.time()
                diff = start-now
                text = 'İLERLEME\n'
                text += 'Boyut : {}\n'.format(progress['size'])
                text += 'Süre : {}\n'.format(progress['time'])
                text += 'Hız : {}\n'.format(progress['speed'])

                if round(diff % 5)==0:
                    try:
                        await msg.edit(text=text)
                    except Exception as e:
                        print(e)
