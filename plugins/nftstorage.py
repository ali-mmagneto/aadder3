import pyrogram
from pyrogram import Client, filters
import os
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from helper_func.thumb import get_thumbnail, get_duration, get_width_height
from helper_func.progress_bar import progress_bar
from config import Config
import time
import time
import nft_storage
from nft_storage.api import nft_storage_api
from nft_storage.model.error_response import ErrorResponse
from nft_storage.model.upload_response import UploadResponse
from nft_storage.model.unauthorized_error_response import UnauthorizedErrorResponse
from nft_storage.model.forbidden_error_response import ForbiddenErrorResponse

@Client.on_message(filters.command('nft'))
async def nftstorage(bot, message):
    start_time = time.time()
    chat_id = str(message.from_user.id)
    msg = await message.reply_text(
        text="`İşlem Başlatıldı...`")
    await msg.edit("`Indiriliyor..`")
    media = await bot.download_media(
                message = message.reply_to_message,
                progress=progress_bar,
                progress_args=("`İndiriliyor...`", msg, start_time))
    splitpath = media.split("/downloads/")
    dow_file_name = splitpath[1]
    file_name = f"downloads/{dow_file_name}"
    configuration = nft_storage.Configuration(
    host = "https://api.nft.storage"
    )

    configuration = nft_storage.Configuration(
        access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDk5MzZjNzk3YzdBQkQzZEY0YWJlQjcyY2FlMjI5ZjY1MTlBMjlFOEIiLCJpc3MiOiJuZnQtc3RvcmFnZSIsImlhdCI6MTY3NzkzNTM2NDQxMSwibmFtZSI6ImJvdHVtIn0.USpc3vwmtqwp-5-7KxkXkrEZXMB8yUeSpHNIM1UlYDs'
    )


    with nft_storage.ApiClient(configuration) as api_client:
        api_instance = nft_storage_api.NFTStorageAPI(api_client)
        body = open(file_name, 'rb') # file_type | 
        try:
            api_response = api_instance.store(body)
            print(api_response)
            await message.reply_text(api_response)
        except nft_storage.ApiException as e:
            await message.reply_text(e)
