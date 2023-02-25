# :d
import os, lk21, time, requests, math
from urllib.parse import unquote
from pySmartDL import SmartDL
from urllib.error import HTTPError
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image

# Configs

# Buttons
START_BUTTONS=[
    [
        InlineKeyboardButton("Rate Me 🌟", url="https://t.me/tlgrmcbot?start=DowntoStreamtape_Bot-review"),
        InlineKeyboardButton("Update Channel", url="https://t.me/BlueWhaleBots"),
    ],
    [InlineKeyboardButton("Author", url="https://t.me/SarfarazStark")],
]

# Helpers

# https://github.com/SpEcHiDe/AnyDLBot


# https://github.com/viperadnan-git/google-drive-telegram-bot/blob/main/bot/helpers/downloader.py
def download_file(url, dl_path):
  try:
    dl = SmartDL(url, dl_path, progress_bar=False)
    dl.start()
    filename = dl.get_dest()
    if '+' in filename:
          xfile = filename.replace('+', ' ')
          filename2 = unquote(xfile)
    else:
        filename2 = unquote(filename)
    os.rename(filename, filename2)
    return True, filename2
  except HTTPError as error:
    return False, error


@Client.on_message(filters.command("sindir") & filters.private)
async def loader(bot, update):
    dirs = './downloads/'
    if not os.path.isdir(dirs):
        os.mkdir(dirs)
    if not 'streamtape.com' in update.text:
        await update.reply_text("`git bir Streamtape urlsi at bana`") 
    link = update.reply_to_message.text
    if '/' in link:
        links = link.split('/')
        if len(links) == 6:
            if link.endswith('mp4'):
                link = link
            else:
                link = link + 'video.mp4'
        elif len(links) == 5:
            link = link + '/video.mp4'
        else:
            return
    else:
        return
    bypasser = lk21.Bypass()
    url = bypasser.bypass_url(link)
    pablo = await update.reply_text("`İndiriliyor...`", True)
    result, dl_path = download_file(url, dirs)
    start_dl = time.time()
    await pablo.edit_text("`Yüklüyorum...`")
    try:
        await update.reply_video(
            video=dl_path,
            quote=True,
            thumb=thumb,
            duration=duration,
            progress=progress_bar,
            progress_args=(
                'Yükleniyor...',
                pablo,
                start_dl
            )
        )
        os.remove(dl_path)
        os.remove(thumb)
    except Exception as e:
        await update.reply_text(e)
    
