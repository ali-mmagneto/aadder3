#:d


import time
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from helper_func.download import download_file
from helper_func.tools import clean_up
from helper_func.progress_bar import progress_bar
from plugins.save_file import equee
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def upload_audio(client, message, file_loc):

    msg = await message.edit_text(
        text="**Ayıklanan Dosyan Yükleniyor...**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Progress", callback_data="progress_msg")]])
    )

    title = None
    artist = None
    thumb = None
    duration = 0

    metadata = extractMetadata(createParser(file_loc))
    if metadata and metadata.has("title"):
        title = metadata.get("title")
    if metadata and metadata.has("artist"):
        artist = metadata.get("artist")
    if metadata and metadata.has("duration"):
        duration = metadata.get("duration").seconds

    c_time = time.time()    

    try:
        await client.send_audio(
            chat_id=message.chat.id,
            audio=file_loc,
            thumb=thumb,
            caption="**@mmagneto**",
            title=title,
            performer=artist,
            duration=duration,
            progress=progress_bar,
            progress_args=(
                "**Uploading extracted stream...**",
                msg,
                c_time
            )
        )
    except Exception as e:
        print(e)     
        await msg.edit_text("**Some Error Occurred. See Logs for More Info.**")   
        return

    await msg.delete()
    await clean_up(file_loc)    
    del equee[0]
    if len(equee) > 0:
        await download_file(client, equee[0])

async def upload_subtitle(client, message, file_loc):

    msg = await message.edit_text(
        text="**Ayıklanan Dosyan Yükleniyor...**",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Progress", callback_data="progress_msg")]])
    )

    c_time = time.time() 

    try:
        await client.send_document(
            chat_id=message.chat.id,
            document=file_loc,
            caption="**@mmagneto**",
            progress=progress_bar,
            progress_args=(
                "**Uploading extracted subtitle...**",
                msg,
                c_time
            )
        )
    except Exception as e:
        print(e)     
        await msg.edit_text("**Some Error Occurred. See Logs for More Info.**")   
        return

    await msg.delete()
    await clean_up(file_loc)        
    del equee[0]
    if len(equee) > 0:
        await download_file(client, equee[0])
