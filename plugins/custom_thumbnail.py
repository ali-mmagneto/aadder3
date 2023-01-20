import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
from pyrogram import Client, filters
from PIL import Image
from config import Config

logging.getLogger("pyrogram").setLevel(logging.WARNING)


@Client.on_message(filters.incoming & filters.photo)
async def save_photo(c, m):
    v = await m.reply_text("`Thumbnail Alıniyor..`", True)
    chat_id = m.from_user.id
    path = os.path.join(
        Config.DOWNLOAD_DIR,
        chat_id
    )
    thumb_image_path = os.path.join(
        path,
        chat_id + ".jpg"
    )

    downloaded_file_name = await m.download(
        file_name=thumb_image_path
    )
    Image.open(downloaded_file_name).convert(
        "RGB"
    ).save(downloaded_file_name)
    # ref: https://t.me/PyrogramChat/44663
    img = Image.open(downloaded_file_name)
    img.save(thumb_image_path, "JPEG")
    try:
        await v.edit_text("`Thumbnail Kaydedildi 😜`.")
    except Exception as e:
        print(f"#Error {e}")


@Client.on_message(filters.incoming & filters.command(["delthumb"]))
async def delete_thumbnail(c, m):
    chat_id = m.from_user.id
    path = os.path.join(
        Config.DOWNLOAD_DIR,
        chat_id
    )
    thumb_image_path = os.path.join(
        path,
        chat_id + ".jpg"
    )
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
    await m.reply_text("`Thumbnail Silindi.`", quote=True)
