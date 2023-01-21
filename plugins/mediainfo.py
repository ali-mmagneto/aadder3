from helper_func.tools import katbin_paste
from helper_func.tools import get_readable_size, get_readable_bitrate

from pyrogram.types import Message
from pyrogram import Client, filters

import subprocess
import requests
import json
import re
import os



async def telegram_mediainfo(client, message):
    """
    Telegram Dosyasından Mediainfo çıkartır.
    """

    message = message.reply_to_message

    if message.text:
        return await message.reply_text("`Farkındaysan Text mesajların mediainfosu olmuyor.", quote=True)

    elif message.media.value == 'video':
        media = message.video

    elif message.media.value == 'audio':
        media = message.audio

    elif message.media.value == 'document':
        media = message.document

    elif message.media.value == 'voice':
        media = message.voice

    else:
        return await message.reply_text("`Bu tür dosyaları desteklemiyorum`", quote=True)

    filename = str(media.file_name)
    mime = media.mime_type
    size = media.file_size

    reply_msg = await message.reply_text("`Mediainfoyu almaya çalıșıyorum, bekle..`", quote=True)

    if int(size) <= 50000000:
        await message.download(os.path.join(os.getcwd(), filename))

    else:
        async for chunk in client.stream_media(message, limit=5):
            with open(filename, 'ab') as f:
                f.write(chunk)

    mediainfo = subprocess.check_output(['mediainfo', filename]).decode("utf-8")
    mediainfo_json = json.loads(subprocess.check_output(['mediainfo', filename, '--Output=JSON']).decode("utf-8"))
    readable_size = get_readable_size(size)

    try:
        lines = mediainfo.splitlines()
        for i in range(len(lines)):
            if 'File size' in lines[i]:
                lines[i] = re.sub(r": .+", ': ' + readable_size, lines[i])

            elif 'Overall bit rate' in lines[i] and 'Overall bit rate mode' not in lines[i]:

                duration = float(mediainfo_json['media']['track'][0]['Duration'])
                bitrate_kbps = (size * 8) / (duration * 1000)
                bitrate = get_readable_bitrate(bitrate_kbps)

                lines[i] = re.sub(r": .+", ': ' + bitrate, lines[i])

            elif 'IsTruncated' in lines[i] or 'FileExtension_Invalid' in lines[i]:
                lines[i] = ''

        remove_N(lines)
        with open(f'{filename}.txt', 'w') as f:
            f.write('\n'.join(lines))

        with open(f"{filename}.txt", "r+") as file:
            content = file.read()

        output = await katbin_paste(content)

        await reply_msg.edit(f"**Dosya Adı :** `{filename}`\n\n**Mediainfo :** {output}", disable_web_page_preview=True)
        os.remove(f'{filename}.txt')
        os.remove(filename)

    except:
        await reply_msg.delete()
        await message.reply_text(f"mediainfoyu alırken bir hata oluștu bir daha dene.", quote=True)


@Client.on_message(filters.command('mediainfo'))
async def mediainfo(client, message: Message):
    if message.reply_to_message:
        await telegram_mediainfo(client, message)
