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
import random
from config import Config
import time
import re
import asyncio
from unidecode import unidecode
videolarr = []
videolar = [] 

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

async def read_stderr(start, msg, process):
    async for line in readlines(process.stderr):
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


async def videobirlestirici(msg, input_file, bot, message):
    start = time.time()
    output = "BirleştirilmişVideo.mp4"
    out_location = f"downloads/{output}"
    command = [
        "ffmpeg",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        input_file,
        "-c",
        "copy",
        out_location
    ]
    
    process = await asyncio.create_subprocess_exec(
            *command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )

    await asyncio.wait([
            read_stderr(start, msg, process),
            process.wait(),
        ])

    if process.returncode == 0:
        await msg.edit('Video Başarıyla Kesildi!\n\nGeçen Süre : {} saniye'.format(round(start-time.time())))
    else:
        await msg.edit('Video kesilirken Bir Hata Oluştu!')
        return False
    time.sleep(2)
    return output

@Client.on_message(filters.command('videolar'))
async def mergevideosu(bot, message):
    try:
        media = message.reply_to_message.video or message.reply_to_message.document
        if media.file_name is None:
            await message.reply_text("Bu Videonun Adı Yok!")
            return
        if media.file_name.rsplit(".", 1)[-1].lower() not in ["mp4", "mkv", "webm"]:
            await message.reply_text("Bu Video formatı desteklenmiyor\nSadece mp4 mkv webm gönder.", quote=True)
            return
        try:
            start_time = time.time()
            msg = await message.reply_text("`İşleme Başlıyorum..`")
            video = await bot.download_media(
                        message=message.reply_to_message,
                        progress=progress_bar,
                        progress_args=("`İndiriliyor...`", msg, start_time))
            splitpath = video.split("/downloads/")
            dow_file_name = splitpath[1]
            videolocu = f"downloads/{dow_file_name}"
            videolarr.append(videolocu)
            print(videolarr)
            sayi = len(videolarr)
            await msg.edit(f"`{sayi}. Video Kaydedildi Diğer videoları yanıtla.`")
        except Exception as e:
            await message.reply_text(e) 
    except Exception as e:
        await message.reply_text(e)

@Client.on_message(filters.command('birlestir'))
async def videobirlesislemi(bot, message):
    try:
        if len(videolarr) == 1:
            await message.reply_text("`Yeterli Sayıda Video Kaydetmemişsin 😡`") 
            return
        msg = await message.reply_text("`İşleme Başlıyorum`") 
        input_file = f"downloads/{message.chat.id}.txt"
        with open(input_file, 'w') as _list:
            _list.write("\n".join(videolarr))
        await bot.send_document(
            chat_id = message.chat.id,
            document = input_file)
        birlestirilmistemp = await videobirlestirici(msg, input_file, bot, message)
    except Exception as e:
        await message.reply_text(e)
