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

async def videotrimleyici(msg, trimtemp, baslangic, bitis, bot, message):
    start = time.time()
    output = "KesilmisVideo.mp4"
    out_location = f"downloads/{output}"
    command = [
        "ffmpeg",
        "-i",
        trimtemp,
        "-ss",
        str(baslangic),
        "-to",
        str(bitis),
        "-async",
        "1",
        "-strict",
        "-2",
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

@Client.on_message(filters.command('trim'))
async def trimmes(bot, message):
    if not message.reply_to_message:
       await message.reply_text("`Bir Video Yanıtla..`")
       return
    info = unidecode(message.text).split()
    if len(info) < 3:
        await bot.send_message(message.chat.id, "Hatalı Kullanım :/ Doğru Kullanım Şu Şekilde:\n\n`/trim 00:05:00 00:06:00`") 
        return
    baslangic = info[1]
    bitis = info[2]
    print(baslangic) 
    print(bitis)
    msg = await bot.send_message(
        chat_id=message.chat.id,
        text="`İşlem Başlatıldı...`")
    await msg.edit("`Indiriliyor..`")
    start_time = time.time()
    media = await bot.download_media(
                message = message.reply_to_message,
                file_name = f"downloads/trimolcakvideo.mp4",
                progress=progress_bar,
                progress_args=("`İndiriliyor...`", msg, start_time))
    dosyaadi = message.reply_to_message.file_name
    gercekad = f"downloads/{dosyaadi}"
    trimtemp = f"downloads/trimolcakvideo.mp4"
    trimolmus = await videotrimleyici(msg, trimtemp, baslangic, bitis, bot, message)
    os.rename(trimolmus, gercekad)
    
