
from pyrogram import filters
from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from script import Script

from helper_func.progress_bar import PRGRS
from helper_func.tools import clean_up
from helper_func.download import download_file, DATA
from helper_func.ffmpeg import extract_audio, extract_subtitle


@Client.on_callback_query()
async def cb_handler(client, query):
    if query.data == "close": 
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
            await query.message.edit_text("Hata Oldu")   


    elif query.data.startswith('subtitle'):
        await query.answer()
        try:
            stream_type, mapping, keyword = query.data.split('_')
            data = DATA[keyword][int(mapping)]
            await extract_subtitle(client, query.message, data)
        except:
            await query.message.edit_text("**Hata Oldu**")  


    elif query.data.startswith('cancel'):
        try:
            query_type, mapping, keyword = query.data.split('_')
            data = DATA[keyword][int(mapping)]   
            await query.message.edit_text("**Iptal Edildi...**")
            await query.answer(
                "Iptal Ediliyor...",
                show_alert=True
            ) 
        except:
            await query.answer() 
            await query.message.edit_text("**Hata Oldu**")        
