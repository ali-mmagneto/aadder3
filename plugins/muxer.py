from pyrogram import Client, filters
from helper_func.progress_bar import progress_bar
from helper_func.dbhelper import Database as Db
from helper_func.mux import softmux_vid
from helper_func.thumb import get_thumbnail, get_duration, get_width_height
from config import Config
from plugins.forcesub import handle_force_subscribe
import time
import os
db = Db()

@Client.on_message(filters.command('sesekle') & filters.private)
async def softmux(bot, message, cb=False):
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, message)
      if fsub == 400:
        return
    me = await bot.get_me()

    chat_id = message.from_user.id
    og_vid_filename = db.get_vid_filename(chat_id)
    og_sub_filename = db.get_sub_filename(chat_id)
    text = ''
    if not og_vid_filename :
        text += 'Dostum Önce Bir Video Gönder\n'
    if not og_sub_filename :
        text += 'Sonra Ses Dosyası Gönder!'

    if not (og_sub_filename and og_vid_filename) :
        await bot.send_message(chat_id, text)
        return

    text = 'Ses dosyanız Video dosyanıza ekleniyor..'
    sent_msg = await bot.send_message(chat_id, text)

    softmux_filename = await softmux_vid(og_vid_filename, og_sub_filename, sent_msg)
    if not softmux_filename:
        return

    final_filename = db.get_filename(chat_id)
    os.rename(Config.DOWNLOAD_DIR+'/'+softmux_filename,Config.DOWNLOAD_DIR+'/'+final_filename)
    video = os.path.join(Config.DOWNLOAD_DIR, final_filename)
    start_time = time.time()
    duration = get_duration(video)
    thumb = get_thumbnail(video, './' + Config.DOWNLOAD_DIR, duration / 4)
    width, height = get_width_height(video)
    get_chat = await bot.get_chat(chat_id=Config.PRE_LOG)
    print(get_chat)
    file_size = os.stat(video).st_size
    if file_size > 2:
        await bot.send_message(Config.PRE_LOG, "2 gb üstüVideo Geliyor.")
        copy = await Config.userbot.send_video(
                chat_id = Config.PRE_LOG, 
                progress = progress_bar, 
                progress_args = (
                    'Dosyan Yükleniyor!',
                    sent_msg,
                    start_time
                    ),
                duration = duration,
                thumb = thumb,
                width = width,
                height = height,
                supports_streaming=True,
                video = video,
                caption = final_filename
                )
        text = 'Dosyan Başarı İle Yüklendi!\nGeçen Toplam Zaman : {} saniye'.format(round(time.time()-start_time))
        await sent_msg.edit(text)
        await bot.copy_message(
            chat_id=chat_id, 
            from_chat_id=Config.PRE_LOG, 
            message_id=copy.id)
    else:
        copy = await bot.send_video(
                chat_id = chat_id, 
                progress = progress_bar, 
                progress_args = (
                    'Dosyan Yükleniyor!',
                    sent_msg,
                    start_time
                    ),
                duration = duration,
                thumb = thumb,
                width = width,
                height = height,
                supports_streaming=True,
                video = video,
                caption = final_filename
                )
        text = 'Dosyan Başarı İle Yüklendi!\nGeçen Toplam Zaman : {} saniye'.format(round(time.time()-start_time))
        await sent_msg.edit(text)
    path = Config.DOWNLOAD_DIR+'/'
    os.remove(path+og_sub_filename)
    os.remove(path+og_vid_filename)
    try :
        os.remove(path+final_filename)
    except :
        pass

    db.erase(chat_id)

