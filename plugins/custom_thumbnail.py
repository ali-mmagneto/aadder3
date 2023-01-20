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
    v = await m.reply_text("Thumbnail Aliniyor.", True)
    user_id = str(m.from_user.id)
    path = os.path.join(
        Config.DOWNLOAD_DIR,
        user_id
    )
    thumb_image_path = os.path.join(
        path,
        user_id + ".jpg"
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
        await v.edit_text("Thumbnail Saved.")
    except Exception as e:
        print(f"#Error {e}")


@Client.on_message(filters.incoming & filters.command(["delthumb"]))
async def delete_thumbnail(c, m):
    user_id = str(m.from_user.id)
    path = os.path.join(
        Config.DOWNLOAD_DIR,
        user_id
    )
    thumb_image_path = os.path.join(
        path,
        user_id + ".jpg"
    )
    if os.path.exists(thumb_image_path):
        os.remove(thumb_image_path)
    await m.reply_text("Thumbnail Removed.", quote=True)
