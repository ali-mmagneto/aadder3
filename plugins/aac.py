from pyrogram import Client, filters
aquee = [] 
from helper_func.aac_helper import add_task


video_mimetype = [
    "video/x-flv",
    "video/mp4",
    "video/avi",
    "video/mkv",
    "application/x-mpegURL",
    "video/mp2t",
    "video/3gpp",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-ms-wmv",
    "video/x-matroska",
    "video/webm",
    "video/x-m4v",
    "video/quicktime",
    "video/mpeg"
]

@Client.on_message(filters.command('aac'))
async def encode_video(bot, message):
    if message.reply_to_message.document:
        if not message.reply_to_message.document.mime_type in video_mimetype:
            message.reply_text("```Bu Video Dosyası Değil.```", quote=True)
            return
    await message.reply_text(f"`Sıraya Ekledim...\n\nSıran: {len(aquee)}`", quote=True)
    aquee.append(message)
    if len(aquee) == 1:
        await add_task(bot, message) 
