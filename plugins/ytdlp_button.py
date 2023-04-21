import asyncio
import json
import re
import os
from logging import getLogger, WARNING
from os import remove as osremove, walk, path as ospath, rename as osrename
from time import time, sleep
import requests
from pyrogram.errors import FloodWait, RPCError
from PIL import Image
from threading import RLock
from pyrogram.types import Message
import shutil
import time
from datetime import datetime

from config import Config
from pyrogram.enums import MessageEntityType, ChatAction
from database.database import db
from translation import Translation

from pyrogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, MessageNotModified
from helper_func.thumb import get_thumbnail, get_duration, get_width_height
from helper_func.progress_bar import progress_bar, humanbytes
from helper_func.ffmpeg import generate_screen_shots, VideoThumb, VideoMetaData, VMMetaData, DocumentThumb, \
    AudioMetaData
from helper_func.utils import remove_urls, remove_emoji

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

 
progress_pattern = re.compile(
    r'(frame|fps|size|time|bitrate|speed|Duration)\s*\=\s*(\S+)'
)

async def read_stdera(start, process, bot, message_id, chat_id):
    async for line in readlines(process.stderr):
            line = line.decode('utf-8')
            progress = parse_progress(line)
            if progress:
                #Progress bar logic
                now = time.time()
                diff = start-now
                text = 'İndiriliyor 📥\n\n'
                text += 'İndirilen Video Boyutu : {}\n'.format(progress['size'])
                text += 'İndirilen Video Süresi: {}\n'.format(progress['time'])
                text += 'İndirme Hızı : {}\n'.format(progress['bitrate'])
                text += 'İşlem Hızı : {}\n'.format(progress['speed'])

                if round(diff % 5)==0:
                    try:
                        await bot.edit_message_text(
                            text=text,
                            chat_id=chat_id,
                            message_id=message_id)
                    except Exception as e:
                        print(e)

def parse_progress(line):
    items = {
        key: value for key, value in progress_pattern.findall(line)
    }
    if not items:
        return None
    return items

async def readlines(stream):
    pattern = re.compile(br'[\r\n]+')

    data = bytearray()
    while not stream.at_eof():
        lines = pattern.split(data)
        data[:] = lines.pop(-1)
        for line in lines:
            yield line

        data.extend(await stream.read(1024 * 1024))

async def yt_dlp_call_back(bot, update):
    cb_data = update.data
    LOGGER.info(cb_data) 
    tg_send_type, yt_dlp_format, yt_dlp_ext, random = cb_data.split("|")

    dtime = str(time.time())
    
    message = update.message
    current_user_id = message.reply_to_message.from_user.id
    user_id = update.from_user.id
    chat_id = str(message.chat.id)
    message_id = message.id
    
    if current_user_id != user_id:
        await bot.answer_callback_query(
            callback_query_id=update.id,
            text="Seni tanımıyorum ahbap.",
            show_alert=True,
            cache_time=0,
        )
        return False, None

    thumb_image_path = Config.DOWNLOAD_LOCATION + \
                       "/" + str(user_id) + f'{random}' + ".jpg"
    save_ytdl_json_path = Config.DOWNLOAD_LOCATION + \
                          "/" + str(user_id) + f'{random}' + ".json"
    LOGGER.info(save_ytdl_json_path)

    try:
        with open(save_ytdl_json_path, "r", encoding="utf8") as f:
            response_json = json.load(f)
    except FileNotFoundError as e:
        await bot.delete_messages(
            chat_id=chat_id,
            message_ids=message_id,
            revoke=True
        )
        return False
    #
    response_json = response_json[0]
    # TODO: temporary limitations
    # LOGGER.info(response_json)
    ynt = message.reply_to_message 
    yt_dlp_url = ynt.reply_to_message.text
    LOGGER.info(yt_dlp_url)
    name = str(response_json.get("title")[:100]) + \
           "." + yt_dlp_ext
    custom_file_name = remove_emoji(remove_urls(name))
    LOGGER.info(name)
    #
    yt_dlp_username = None
    yt_dlp_password = None
    if "|" in yt_dlp_url:
        url_parts = yt_dlp_url.split("|")
        if len(url_parts) == 2:
            yt_dlp_url = url_parts[0]
            custom_file_name = url_parts[1]
            caption = custom_file_name
            if len(custom_file_name) > 60:
                await update.edit_message_text(
                    Translation.IFLONG_FILE_NAME.format(
                        alimit="64",
                        num=len(custom_file_name)
                    )
                )
                return
        elif len(url_parts) == 4:
            yt_dlp_url = url_parts[0]
            custom_file_name = url_parts[1]
            yt_dlp_username = url_parts[2]
            yt_dlp_password = url_parts[3]
        else:
            for entity in message.reply_to_message.entities:
                if entity.type == MessageEntityType.TEXT_LINK:
                    yt_dlp_url = entity.url
                elif entity.type == MessageEntityType.URL:
                    o = entity.offset
                    l = entity.length
                    yt_dlp_url = yt_dlp_url[o:o + l]
        if yt_dlp_url is not None:
            yt_dlp_url = yt_dlp_url.strip()
        if custom_file_name is not None:
            custom_file_name = custom_file_name.strip()
        if yt_dlp_username is not None:
            yt_dlp_username = yt_dlp_username.strip()
        if yt_dlp_password is not None:
            yt_dlp_password = yt_dlp_password.strip()
        LOGGER.info(yt_dlp_url)
        LOGGER.info(custom_file_name)
    else:
        title = response_json["fulltitle"][0:100]
        caption = title
        for entity in message.reply_to_message.entities:
            if entity.type == MessageEntityType.TEXT_LINK:
                yt_dlp_url = entity.url
            elif entity.type == MessageEntityType.URL:
                o = entity.offset
                l = entity.length
                yt_dlp_url = yt_dlp_url[o:o + l]

    await bot.edit_message_text(
        text=Translation.DOWNLOAD_START.format(custom_file_name),
        chat_id=chat_id,
        message_id=message_id
    )

    tmp_directory_for_each_user = os.path.join(
        Config.DOWNLOAD_LOCATION,
        str(user_id),
        dtime
    )
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)
    download_directory = os.path.join(tmp_directory_for_each_user, custom_file_name)
    command_to_exec = []
    if tg_send_type == "audio":
        command_to_exec = [
            "yt-dlp",
            "-c",
            "--max-filesize", str(Config.TG_MAX_FILE_SIZE),
            "--prefer-ffmpeg",
            "--extract-audio",
            "--audio-format", yt_dlp_ext,
            "--audio-quality", yt_dlp_format,
            yt_dlp_url,
            "-o", download_directory
        ]
    else:
        try:
            for for_mat in response_json["formats"]:
                format_id = for_mat.get("format_id")
                if format_id == yt_dlp_format:
                    acodec = for_mat.get("acodec")
                    if acodec == "none":
                        yt_dlp_format += "+bestaudio"
                    break

            command_to_exec = [
                "yt-dlp",
                "-c",
                "--max-filesize", str(Config.TG_MAX_FILE_SIZE),
                "--embed-subs",
                "-f", yt_dlp_format,
                "--hls-prefer-ffmpeg", yt_dlp_url,
                "-o", download_directory
            ]
        except KeyError:
            command_to_exec = [
                "yt-dlp",
                "-c",
                "--max-filesize", str(Config.TG_MAX_FILE_SIZE),
                yt_dlp_url, "-o", download_directory
            ]

    #
    command_to_exec.append("--no-warnings")
    # command_to_exec.append("--quiet")
    command_to_exec.append("--restrict-filenames")
    #
    if ".cloud" in yt_dlp_url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://vidmoly.to/")
    if ".mubicdn.net" in yt_dlp_url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://mubi.com")
    if "https://streamtape.com/" in yt_dlp_url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://streamtape.com/")
    if "storage.diziyou.co" in yt_dlp_url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://storage.diziyou.co/episodes/")
    if ".online" in yt_dlp_url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://vidmoly.to/")
    if ".space" in yt_dlp_url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://vidmoly.to/")
    if ".lat" in yt_dlp_url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://vidmoly.to/")
    if "https://upstreamcdn.co" in yt_dlp_url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://upstreamcdn.co")
    if "closeload" in yt_dlp_url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://closeload.com/")
    if yt_dlp_username is not None:
        command_to_exec.append("--username")
        command_to_exec.append(yt_dlp_username)
    if yt_dlp_password is not None:
        command_to_exec.append("--password")
        command_to_exec.append(yt_dlp_password)
    if len(Config.MOLY_LINKLERI) != 0:
        for ref in Config.MOLY_LINKLERI:
            if f"{ref}" in yt_dlp_url:
                command_to_exec.append("--referer")
                command_to_exec.append("https://vidmoly.to/")
    LOGGER.info(command_to_exec)
    start = datetime.now()
    start1 = time.time() 
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await asyncio.wait([
            read_stdera(start1, process, bot, message_id, chat_id),
            process.wait(),
        ])
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    # LOGGER.info(e_response)
    # LOGGER.info(t_response)
    ad_string_to_replace = "please report this issue on  https://github.com/yt-dlp/yt-dlp/issues?q= , filling out the " \
                           "appropriate issue template. Confirm you are on the latest version using  yt-dlp -U "
    if e_response and ad_string_to_replace in e_response:
        error_message = e_response.replace(ad_string_to_replace, "")
        await message.edit_caption(caption=error_message)
        return False, None
    if t_response:
        # LOGGER.info(t_response)
        try:
            os.remove(save_ytdl_json_path)
        except FileNotFoundError as exc:
            pass

        end_one = datetime.now()
        time_taken_for_download = (end_one - start).seconds

        #
        file_size = Config.TG_MAX_FILE_SIZE + 1
        #
        LOGGER.info(tmp_directory_for_each_user)
        user = await bot.get_me()
        BotMention = user.mention
        UserMention = update.from_user.mention

        reply_markup = False

        if os.path.isdir(tmp_directory_for_each_user):
            directory_contents = os.listdir(tmp_directory_for_each_user)
            directory_contents.sort()
        else:
            try:
                shutil.rmtree(tmp_directory_for_each_user)  # delete folder for user
                os.remove(thumb_image_path)
            except:
                pass

        for single_file in directory_contents:
            print(single_file)
            path = os.path.join(tmp_directory_for_each_user, single_file)

            file_size = os.stat(path).st_size

            try:
                if tg_send_type == 'video' and 'webm' in path:
                    download_directory = path.rsplit('.', 1)[0] + '.mkv'
                    os.rename(path, download_directory)
                    path = download_directory
            except:
                pass

            if file_size > 2093796556:
                is_w_f = False
                images = await generate_screen_shots(
                    path,
                    tmp_directory_for_each_user,
                    is_w_f,
                    Config.DEF_WATER_MARK_FILE,
                    300,
                    9
                )
                try:
                    await bot.edit_message_text(
                        text=Translation.UPLOAD_START,
                        chat_id=chat_id,
                        message_id=message_id
                    )
                except:
                    pass

                start_time = time.time()

                try:
                    if tg_send_type == "audio":
                        await message.reply_to_message.reply_chat_action(ChatAction.UPLOAD_AUDIO)
                        duration = get_duration(path)
                        width, height = get_width_height(path)
                        thumb_image_path = os.path.join(
                                               Config.DOWNLOAD_DIR,
                                               chat_id,
                                               chat_id + ".jpg")
                        if os.path.exists(thumb_image_path):
                            thumb = thumb_image_path
                        elif "youtu" in yt_dlp_url:
                            url = response_json.get("thumbnail")
                            thumb = "ytthumbfoto.jpg"
                            img = Image.open(requests.get(url, stream = True).raw)
                            img.save(thumb)  
                        else:
                            thumb = None
                        copy = await userbot.send_audio(
                            chat_id=Config.PRE_LOG,
                            audio=path,
                            caption=caption,
                            thumb=thumb,
                            reply_to_message_id=message.reply_to_message.id,
                            reply_markup=reply_markup,
                            progress=progress_for_pyrogram,
                            progress_args=(
                                Translation.UPLOAD_START,
                                message,
                                start_time
                            )
                        )
                        LOGGER.info(str(copy)) 
                        await bot.copy_message(
                            chat_id=chat_id, 
                            from_chat_id=Config.PRE_LOG, 
                            message_id=copy.id)

                    elif tg_send_type == "vm":
                        duration = get_duration(path)
                        width, height = get_width_height(path)
                        thumb_image_path = os.path.join(
                                               Config.DOWNLOAD_DIR,
                                               chat_id,
                                               chat_id + ".jpg")
                        if os.path.exists(thumb_image_path):
                            thumb = thumb_image_path
                        else:
                            thumb = get_thumbnail(path, './' + Config.DOWNLOAD_DIR, duration / 4)
                        await message.reply_to_message.reply_chat_action(ChatAction.UPLOAD_VIDEO_NOTE)
                        copy = await userbot.send_video_note(
                            chat_id=Config.PRE_LOG,
                            video_note=path,
                            duration=duration,
                            length=width,
                            thumb=thumb,
                            reply_to_message_id=message.reply_to_message.id,
                            reply_markup=reply_markup,
                            progress=progress_for_pyrogram,
                            progress_args=(
                                Translation.UPLOAD_START,
                                message,
                                start_time
                            )
                        )
                        LOGGER.info(str(copy)) 
                        await bot.copy_message(
                            chat_id=chat_id, 
                            from_chat_id=Config.PRE_LOG, 
                            message_id=copy.id)

                    elif tg_send_type == "file":
                        copy = await userbot.send_document(
                            chat_id=Config.PRE_LOG,
                            document=path,
                            caption=caption,
                            reply_to_message_id=message.reply_to_message.id,
                            reply_markup=reply_markup,
                            progress=progress_bar,
                            progress_args=(
                                Translation.UPLOAD_START,
                                message,
                                start_time
                            )
                        )
                        LOGGER.info(str(copy)) 
                        await bot.copy_message(
                            chat_id=chat_id, 
                            from_chat_id=Config.PRE_LOG, 
                            message_id=copy.id)
                    if 1 == 0:
                        print("1 0'a eşit olmuş aq")
                    else:
                        duration = get_duration(path)
                        width, height = get_width_height(path)
                        thumb_image_path = os.path.join(
                                               Config.DOWNLOAD_DIR,
                                               chat_id,
                                               chat_id + ".jpg")
                        if os.path.exists(thumb_image_path):
                            thumb = thumb_image_path
                        elif "youtu" in yt_dlp_url:
                            url = response_json.get("thumbnail")
                            thumb = "ytthumbfoto.jpg"
                            img = Image.open(requests.get(url, stream = True).raw)
                            img.save(thumb)  
                        else:
                            thumb = get_thumbnail(path, './' + Config.DOWNLOAD_DIR, duration / 4)
                        await message.reply_to_message.reply_chat_action(ChatAction.UPLOAD_VIDEO)
                        copy = await userbot.send_video(
                            chat_id=Config.PRE_LOG,
                            video=path,
                            caption=caption,
                            duration=duration,
                            width=width,
                            height=height,
                            supports_streaming=True,
                            reply_markup=reply_markup,
                            thumb=thumb,
                            reply_to_message_id=message.reply_to_message.id,
                            progress=progress_bar,
                            progress_args=(
                                Translation.UPLOAD_START,
                                message,
                                start_time
                            )
                       )
                        LOGGER.info(str(copy)) 
                        await bot.copy_message(
                            chat_id=chat_id, 
                            from_chat_id=Config.PRE_LOG, 
                            message_id=copy.id)
                except FloodWait as e:
                    print(f"Sleep of {e.value} required by FloodWait ...")
                    time.sleep(e.value)
                except MessageNotModified:
                    pass 
                    return

                end_two = datetime.now()
                time_taken_for_upload = (end_two - end_one).seconds
                media_album_p = []
                try:
                    await bot.edit_message_text(
                        text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download,
                                                                                time_taken_for_upload),
                        chat_id=chat_id,
                        message_id=message_id,
                        disable_web_page_preview=True
                    )
                except MessageNotModified:
                    pass
                return
            else:
                is_w_f = False
                images = await generate_screen_shots(
                    path,
                    tmp_directory_for_each_user,
                    is_w_f,
                    Config.DEF_WATER_MARK_FILE,
                    300,
                    9
                )
                try:
                    await bot.edit_message_text(
                        text=Translation.UPLOAD_START,
                        chat_id=chat_id,
                        message_id=message_id
                    )
                except:
                    pass

                start_time = time.time()

                try:
                    if tg_send_type == "audio":
                        duration = get_duration(path)
                        thumb_image_path = os.path.join(
                                               Config.DOWNLOAD_DIR,
                                               chat_id,
                                               chat_id + ".jpg")
                        if os.path.exists(thumb_image_path):
                            thumb = thumb_image_path
                        else:
                            thumb = get_thumbnail(path, './' + Config.DOWNLOAD_DIR, duration / 4)
                        await message.reply_to_message.reply_chat_action(ChatAction.UPLOAD_AUDIO)
                        copy = await bot.send_audio(
                            chat_id=chat_id,
                            audio=path,
                            caption=caption,
                            duration=duration,
                            thumb=thumb,
                            reply_to_message_id=message.reply_to_message.id,
                            reply_markup=reply_markup,
                            progress=progress_bar,
                            progress_args=(
                                Translation.UPLOAD_START,
                                message,
                                start_time
                            )
                        )
                    elif tg_send_type == "vm":
                        duration = get_duration(path)
                        width, height = get_width_height(path)
                        thumb_image_path = os.path.join(
                                               Config.DOWNLOAD_DIR,
                                               chat_id,
                                               chat_id + ".jpg")
                        if os.path.exists(thumb_image_path):
                            thumb = thumb_image_path
                        else:
                            thumb = get_thumbnail(path, './' + Config.DOWNLOAD_DIR, duration / 4)
                        await message.reply_to_message.reply_chat_action(ChatAction.UPLOAD_VIDEO_NOTE)
                        copy = await bot.send_video_note(
                            chat_id=chat_id,
                            video_note=path,
                            duration=duration,
                            length=width,
                            thumb=thumb,
                            reply_to_message_id=message.reply_to_message.id,
                            reply_markup=reply_markup,
                            progress=progress_bar,
                            progress_args=(
                                Translation.UPLOAD_START,
                                message,
                                start_time
                            )
                        )
                    elif tg_send_type == "file":
                        copy = await bot.send_document(
                            chat_id=chat_id,
                            document=path,
                            caption=caption,
                            reply_to_message_id=message.reply_to_message.id,
                            reply_markup=reply_markup,
                            progress=progress_bar,
                            progress_args=(
                                Translation.UPLOAD_START,
                                message,
                                start_time
                            )
                        )
                    elif 1 == 0:
                        thumb_image_path = os.path.join(
                                               Config.DOWNLOAD_DIR,
                                               chat_id,
                                               chat_id + ".jpg")
                        if os.path.exists(thumb_image_path):
                            thumb = thumb_image_path
                        else:
                            thumb = get_thumbnail(path, './' + Config.DOWNLOAD_DIR, duration / 4)
                        await message.reply_to_message.reply_chat_action(ChatAction.UPLOAD_DOCUMENT)
                        copy = await bot.send_document(
                            chat_id=chat_id, 
                            document=path,
                            thumb=thumb,
                            caption=caption,
                            reply_to_message_id=message.reply_to_message.id,
                            reply_markup=reply_markup,
                            progress=progress_bar,
                            progress_args=(
                                Translation.UPLOAD_START,
                                message,
                                start_time
                            )
                        )
                    else:
                        duration = get_duration(path)
                        width, height = get_width_height(path)
                        thumb_image_path = os.path.join(
                                               Config.DOWNLOAD_DIR,
                                               chat_id,
                                               chat_id + ".jpg")
                        if os.path.exists(thumb_image_path):
                            thumb = thumb_image_path
                        elif "youtu" in yt_dlp_url:
                            url = response_json.get("thumbnail")
                            thumb = "ytthumbfoto.jpg"
                            img = Image.open(requests.get(url, stream = True).raw)
                            img.save(thumb)  
                        else:
                            thumb = get_thumbnail(path, './' + Config.DOWNLOAD_DIR, duration / 4)
                        await message.reply_to_message.reply_chat_action(ChatAction.UPLOAD_VIDEO)
                        copy = await bot.send_video(
                            chat_id=chat_id,
                            video=path,
                            caption=caption,
                            duration=duration,
                            width=width,
                            height=height,
                            supports_streaming=True,
                            reply_markup=reply_markup,
                            thumb=thumb,
                            reply_to_message_id=message.reply_to_message.id,
                            progress=progress_bar,
                            progress_args=(
                                Translation.UPLOAD_START,
                                message,
                                start_time
                            )
                        )
                except FloodWait as e:
                    print(f"Sleep of {e.value} required by FloodWait ...")
                    time.sleep(e.value)
                except MessageNotModified:
                    pass
                end_two = datetime.now()
                time_taken_for_upload = (end_two - end_one).seconds
                media_album_p = []
                try:
                    await bot.edit_message_text(
                        text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download,
                                                                                time_taken_for_upload),
                        chat_id=chat_id,
                        message_id=message_id,
                        disable_web_page_preview=True
                    )
                except MessageNotModified:
                    pass
                return

                end_two = datetime.now()
                time_taken_for_upload = (end_two - end_one).seconds
                
    try:
        os.remove(thumb_image_path)
    except:
        pass
    try:
        shutil.rmtree(tmp_directory_for_each_user)
    except:
        pass
    try:
        os.remove(path)
    except:
        pass
