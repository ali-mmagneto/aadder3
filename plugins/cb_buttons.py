from pyrogram import filters
from pyrogram import Client as trojanz
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from script import Script

from helper_func.download import download_file, DATA
from helper_func.mux import extract_audio, extract_subtitle    

@Client.on_callback_query()
async def cb_handler(bot, query):
    if query.data == "download_file":
        await query.answer()
        await query.message.delete()
        await download_file(bot, query.message)


    elif query.data == "progress_msg":
        try:
            msg = "Progress Details...\n\nCompleted : {current}\nTotal Size : {total}\nSpeed : {speed}\nProgress : {progress:.2f}%\nETA: {eta}"
            await query.answer(
                msg.format(
                    **PRGRS[f"{query.message.chat.id}_{query.message.message_id}"]
                ),
                show_alert=True
            )
        except:
            await query.answer(
                "Processing your file...",
                show_alert=True
            )


    elif query.data == "close": 
        await query.message.delete()  
        await query.answer(
                "Cancelled...",
                show_alert=True
            ) 


    elif query.data.startswith('audio'):
        await query.answer()
        try:
            stream_type, mapping, keyword = query.data.split('_')
            data = DATA[keyword][int(mapping)]
            await extract_audio(client, query.message, data)
        except:
            await query.message.edit_text("**Details Not Found**")   


    elif query.data.startswith('subtitle'):
        await query.answer()
        try:
            stream_type, mapping, keyword = query.data.split('_')
            data = DATA[keyword][int(mapping)]
            await extract_subtitle(client, query.message, data)
        except:
            await query.message.edit_text("**Details Not Found**")  
