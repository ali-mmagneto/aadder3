from pyrogram import Client, filters
from helper_func.progress_bar import progress_bar
from helper_func.dbhelper import Database as Db
from helper_func.mux import softmux_vid, hardmux_vid
from helper_func.thumb import get_thumbnail, get_duration, get_width_height
from config import Config
from plugins.forcesub import handle_force_subscribe
import time
import os
db = Db()

@Client.on_message(filters.command('softmux') & filters.private)
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
        text += 'İlk Önce Bir Video Dosyası Gönder\n'
    if not og_sub_filename :
        text += 'Altyazı Dosyası Gönder!'

    if not (og_sub_filename and og_vid_filename) :
        await bot.send_message(chat_id, text)
        return

    text = 'Dosyanıza soft altyazı uygulanıyor. Birkaç saniye içinde yapılır!'
    sent_msg = await bot.send_message(chat_id, text)

    softmux_filename = await softmux_vid(og_vid_filename, og_sub_filename, sent_msg)
    if not softmux_filename:
        return

    final_filename = db.get_filename(chat_id)
    os.rename(Config.DOWNLOAD_DIR+'/'+softmux_filename,Config.DOWNLOAD_DIR+'/'+final_filename)
    video = os.path.join(Config.DOWNLOAD_DIR, final_filename)
    start_time = time.time()
    file_size = os.stat(video).st_size
    if file_size > 2093796556:
        copy = await Config.userbot.send_video(
                Config.PRE_LOG, 
                progress = progress_bar, 
                progress_args = (
                    'Dosyan Yükleniyor!',
                    sent_msg,
                    start_time
                    ), 
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
                chat_id, 
                progress = progress_bar, 
                progress_args = (
                    'Dosyan Yükleniyor!',
                    sent_msg,
                    start_time
                    ), 
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


@Client.on_message(filters.command('hardmux') & filters.private)
async def hardmux(bot, message, cb=False):
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
        text += 'Önce Video Dosyasını Gönder\n'
    if not og_sub_filename :
        text += 'Altyazı Dosyasını Gönder!'
    
    if not (og_sub_filename or og_vid_filename) :
        return await bot.send_message(chat_id, text)
    
    text = 'Dosyana Hard Altyazı Uygulanıyor. Bu Uzun Sürebilir!'
    sent_msg = await bot.send_message(chat_id, text)

    hardmux_filename = await hardmux_vid(og_vid_filename, og_sub_filename, sent_msg)
    
    if not hardmux_filename:
        return
    
    final_filename = db.get_filename(chat_id)
    os.rename(Config.DOWNLOAD_DIR+'/'+hardmux_filename,Config.DOWNLOAD_DIR+'/'+final_filename)
    video = os.path.join(Config.DOWNLOAD_DIR, final_filename)
    duration = get_duration(video)
    thumb = get_thumbnail(video, './' + Config.DOWNLOAD_DIR, duration / 4)
    width, height = get_width_height(video)
    start_time = time.time()
    file_size = os.stat(video).st_size
    if file_size > 2093796556:
        copy = await Config.userbot.send_video(
                Config.PRE_LOG, 
                progress = progress_bar,
                duration = duration,
                thumb = thumb,
                width = width,
                height = height,
                supports_streaming=True,
                progress_args = (
                    'Dosyan Yükleniyor!',
                    sent_msg,
                    start_time
                    ), 
                video = video,
                caption = final_filename
                )
        text = 'Dosya Başarı İle Yüklendi!\nToplam Geçen zaman : {} saniye'.format(round(time.time()-start_time))
        await sent_msg.edit(text)
        await bot.copy_message(
            chat_id=chat_id, 
            from_chat_id=Config.PRE_LOG, 
            message_id=copy.id)
    else:
        copy = await bot.send_video(
                chat_id, 
                progress = progress_bar,
                duration = duration,
                thumb = thumb,
                width = width,
                height = height,
                supports_streaming=True,
                progress_args = (
                    'Dosyan Yükleniyor!',
                    sent_msg,
                    start_time
                    ), 
                video = video,
                caption = final_filename
                )
        text = 'Dosya Başarı İle Yüklendi!\nToplam Geçen zaman : {} saniye'.format(round(time.time()-start_time))
        await sent_msg.edit(text)
            
    path = Config.DOWNLOAD_DIR+'/'
    os.remove(path+og_sub_filename)
    os.remove(path+og_vid_filename)
    try :
        os.remove(path+final_filename)
    except :
        pass
    db.erase(chat_id)

