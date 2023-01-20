from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from functions.settings import *
from translation import Translation
from database.database import db

@Client.on_message(filters.command(["setthumb", "set_thumbnail"]) & filters.incoming & filters.reply)
async def set_thumbnail(c: Client, m: "types.Message"):
    thumbnail = m.reply_to_message.photo.file_id
    editable = await m.reply_text("**👀 İşleniyor...**")
    await db.set_thumbnail(m.from_user.id, thumbnail=thumbnail)
    await editable.edit("Thumbnail Kaydedildi")


@Client.on_message(filters.private & filters.command(["delthumb", "delete_thumbnail"]))
async def delete_thumbnail(c: Client, m: "types.Message"):
    await db.set_thumbnail(m.from_user.id, thumbnail=None)
    await m.reply_text(
        "`Thumbnail Silindi..`"
    )


@Client.on_message(filters.private & filters.command(["showthumb", "show_thumbnail"]))
async def show_thumbnail(c: Client, m: "types.Message"):
    thumbnail = await db.get_thumbnail(m.from_user.id)
    if thumbnail is not None:
        await c.send_photo(
            chat_id=m.chat.id,
            photo=thumbnail,
            caption=f"**Ayarlı Thumbnail.**",
            reply_to_message_id=m.id)
    else:
        await m.reply_text(text=f"**Thumbnail Bulunamadı.**")
