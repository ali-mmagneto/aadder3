import json
from pyrogram import Client, filters
from pyrogram.types import Message
import subprocess
import datetime
import requests
import asyncio
import time
import shlex
import json
import random
import re
import os
import string
import shutil
import random

from pyrogram.errors import MessageNotModified
from requests_toolbelt import MultipartEncoder
from urllib.parse import unquote


def makedir(name: str):
    if os.path.exists(name):
        shutil.rmtree(name)
    os.mkdir(name)

def randstr():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))


async def slowpics_collection(client, message, file_name, path):
    """
    slow.pics'e yükleme yapar.
    """

    msg = await message.reply_text("`Screenshotlar slow.pics'e yükleniyor.`", quote=True)

    img_list = os.listdir(path)
    data = {
        "collectionName": f"{unquote(file_name)}",
        "hentai": "false",
        "optimizeImages": "false",
        "public": "false",
    }

    for i in range(0, len(img_list)):
        data[f"images[{i}].name"] = img_list[i]
        data[f"images[{i}].file"] = (
            img_list[i],
            open(f"{path}/{img_list[i]}", "rb"),
            "image/png",
        )

    with requests.Session() as client:
        client.get("https://slow.pics/api/collection")
        files = MultipartEncoder(data)
        length = str(files.len)

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Length": length,
            "Content-Type": files.content_type,
            "Origin": "https://slow.pics/",
            "Referer": "https://slow.pics/collection",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
            "X-XSRF-TOKEN": client.cookies.get_dict()["XSRF-TOKEN"]}

        response = client.post("https://slow.pics/api/collection", data=files, headers=headers)
        await msg.edit(
            f"Dosya Adı: `{unquote(file_name)}`\n\nScreenshotlar: https://slow.pics/c/{response.text}",
            disable_web_page_preview=True)
        for files in os.listdir(path):
            await bot.send_photo(
                chat_id=message.chat.id, 
                photo=files)
        for remover in os.listdir(path):
            os.remove(remover)
        
async def generate_ss_from_file(
        client,
        message,
        replymsg,
        file_name,
        frame_count,
        file_duration
):
    """
    FFMPEG İLE DOSYADAN SCREENSHOT ALMA.
    """

    await replymsg.edit(f"`{frame_count} tane screnshots `{unquote(file_name)}` dosyasından alınıyor..` `Lütfen Bekle...`")

    rand_str = randstr()
    makedir(f"screenshot_{rand_str}")

    loop_count = frame_count
    while loop_count != 0:

        random_timestamp = random.uniform(1, file_duration)
        timestamp = str(datetime.timedelta(seconds=int(random_timestamp)))
        outputpath = f"screenshot_{rand_str}/{(frame_count - loop_count) + 1}.png"

        ffmpeg_command = f"ffmpeg -y -ss {timestamp} -i '{file_name}' -vframes 1 {outputpath}"
        args = shlex.split(ffmpeg_command)

        shell = await asyncio.create_subprocess_exec(*args, stdout=asyncio.subprocess.PIPE,
                                                     stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await shell.communicate()
        result = str(stdout.decode().strip()) + str(stderr.decode().strip())

        if "File ended prematurely" in result:
            loop_count += 1
        loop_count -= 1

    await replymsg.delete()
    await slowpics_collection(client, message, file_name, path=f"{os.getcwd()}/screenshot_{rand_str}")

    shutil.rmtree(f"screenshot_{rand_str}")
    os.remove(file_name)

async def telegram_screenshot(client, message, frame_count):
    """
    Generates Screenshots from Telegram Video Files.
    """

    message = message.reply_to_message
    if message.text:
        return await message.reply_text("Reply to a proper video file to Generate Screenshots. **", quote=True)

    elif message.media.value == "video":
        media = message.video

    elif message.media.value == "document":
        media = message.document

    else:
        return await message.reply_text("can only generate screenshots from video file....", quote=True)

    file_name = str(media.file_name)
    mime = media.mime_type
    size = media.file_size

    if message.media.value == "document" and "video" not in mime:
        return await message.reply_text("`Sadece Dosyalardan Screenshot alabiliyorum`....", quote=True)

    # Downloading partial file.
    replymsg = await message.reply_text("`Dosyan Kısmi olarak Indiriliyor....`", quote=True)

    if int(size) <= 200000000:
        await message.download(os.path.join(os.getcwd(), file_name))
        downloaded_percentage = 100  # (100% download)

    else:
        limit = ((25 * size) / 100) / 1000000
        async for chunk in client.stream_media(message, limit=int(limit)):
            with open(file_name, "ab") as file:
                file.write(chunk)

        downloaded_percentage = 25

    await replymsg.edit("`Dosyan İndirildi....`")
    # Partial file downloaded

    mediainfo_json = json.loads(subprocess.check_output(["mediainfo", file_name, "--Output=JSON"]).decode("utf-8"))
    total_duration = mediainfo_json["media"]["track"][0]["Duration"]

    if downloaded_percentage == 100:
        partial_file_duration = float(total_duration)
    else:
        partial_file_duration = (downloaded_percentage * float(total_duration)) / 100

    await generate_ss_from_file(
        client, 
        message,
        replymsg,
        file_name,
        frame_count,
        file_duration=partial_file_duration)

mediainfo_usage = "Generates video frame screenshot from GoogleDrive links, Telegram files or direct download links."

@Client.on_message(filters.command('ss'))
async def screenshot(client, message: Message):
    replied_message = message.reply_to_message
    if replied_message:
        try:
            user_input = message.text.split(None, 1)[1]
            frame_count = int(user_input.strip())
        except:
            frame_count = 5

        if frame_count > 15:
            frame_count = 15
        return await telegram_screenshot(client, message, frame_count)
