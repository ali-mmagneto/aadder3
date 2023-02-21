import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

import os, time, asyncio, json
import re
from PIL import Image
from translation import Translation
from pyrogram import Client, filters
from pyrogram.enums import MessageEntityType, ChatAction
from config import Config
from functions.progress import humanbytes
from functions.aiohttp import DownLoadFile
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.database import db

progress_pattern = re.compile(
    r'(frame|fps|size|time|bitrate|speed)\s*\=\s*(\S+)'
)

async def read_stdera(start, send_message, process, update):
    async for line in readlines(process.stderr):
            line = line.decode('utf-8')
            progress = parse_progress(line)
            if progress:
                #Progress bar logic
                now = time.time()
                diff = start-now
                text = 'İLERLEME\n'
                text += 'Boyut : {}\n'.format(progress['size'])
                text += 'Süre : {}\n'.format(progress['time'])
                text += 'Hız : {}\n'.format(progress['speed'])

                if round(diff % 5)==0:
                    try:
                        await send_message.edit_text(text=text)
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

        data.extend(await stream.read(1024))

@Client.on_message(filters.command('indir')) 
async def echo(bot, update):
    if not update.from_user:
        return await update.reply_text("Seni tanımıyorum ahbap.")

    message_id = update.id
    chat_id = update.chat.id
    await update.reply_chat_action(ChatAction.TYPING)
    send_message = await update.reply(text=f"İşleniyor...⏳", disable_web_page_preview=True,
                                      reply_to_message_id=message_id)

    LOGGER.info(update.from_user)
    url = update.reply_to_message.text

    yt_dlp_username = None
    yt_dlp_password = None
    file_name = None
    random = str(time.time())

    if "|" in url:
        url_parts = url.split("|")
        if len(url_parts) == 2:
            url = url_parts[0]
            file_name = url_parts[1]
        elif len(url_parts) == 4:
            url = url_parts[0]
            file_name = url_parts[1]
            yt_dlp_username = url_parts[2]
            yt_dlp_password = url_parts[3]
        else:
            for entity in update.entities:
                if entity.type == MessageEntityType.TEXT_LINK:
                    url = entity.url
                elif entity.type == MessageEntityType.URL:
                    o = entity.offset
                    l = entity.length
                    url = url[o:o + l]
        if url is not None:
            url = url.strip()
        if file_name is not None:
            file_name = file_name.strip()
        if yt_dlp_username is not None:
            yt_dlp_username = yt_dlp_username.strip()
        if yt_dlp_password is not None:
            yt_dlp_password = yt_dlp_password.strip()
        LOGGER.info(url)
        LOGGER.info(file_name)
    else:
        for entity in update.entities:
            if entity.type == MessageEntityType.TEXT_LINK:
                url = entity.url
            elif entity.type == MessageEntityType.URL:
                o = entity.offset
                l = entity.length
                url = url[o:o + l]
    if HTTP_PROXY != "":
        command_to_exec = [
            "yt-dlp",
            "--no-warnings",
            "--youtube-skip-dash-manifest",
            "--no-check-certificate",
            "-j",
            url,
            "--proxy", HTTP_PROXY
        ]
    else:
        command_to_exec = [
            "yt-dlp",
            "--no-warnings",
            "--external-downloader","aria2c", 
            "--no-check-certificate",
            "-j",
            url
        ]
    if ".online" in url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://vidmoly.to/")
    if "storage.diziyou.co" in url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://storage.diziyou.co/episodes/")
    if ".cloud" in url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://vidmoly.to/")
    if ".mubicdn.net" in url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://mubi.com/")
    if ".space" in url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://vidmoly.to/")
    if "https://upstreamcdn.co" in url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://upstreamcdn.co")
    if "closeload" in url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://closeload.com/")
    if "mail.ru" in url:
        command_to_exec.append("--referer")
        command_to_exec.append("https://my.mail.ru/")
    if yt_dlp_username is not None:
        command_to_exec.append("--username")
        command_to_exec.append(yt_dlp_username)
    if yt_dlp_password is not None:
        command_to_exec.append("--password")
        command_to_exec.append(yt_dlp_password)
    LOGGER.info(command_to_exec)
    start = time.time()
    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    LOGGER.info(e_response)
    t_response = stdout.decode().strip()
    # LOGGER.info(t_response)
    if e_response and "nonnumeric port" not in e_response:
        # LOGGER.warn("Status : FAIL", exc.returncode, exc.output)
        error_message = e_response.replace(
            "please report this issue on  https://github.com/yt-dlp/yt-dlp/issues?q= , filling out the appropriate issue template. Confirm you are on the latest version using  yt-dlp -U",
            "")
        if "This video is only available for registered users." in error_message:
            error_message += Translation.SET_CUSTOM_USERNAME_PASSWORD
        time.sleep(1)
        await send_message.edit_text(
            text=Translation.NO_VOID_FORMAT_FOUND.format(str(error_message)),
            disable_web_page_preview=True
        )
        return False
    if t_response:
        await send_message.edit_text("Formatlar Ayıklanıyor...")
        # LOGGER.info(t_response)
        x_reponse = t_response
        response_json = []
        if "\n" in x_reponse:
            for yu_r in x_reponse.split("\n"):
                response_json.append(json.loads(yu_r))
        else:
            response_json.append(json.loads(x_reponse))
        # response_json = json.loads(x_reponse)
        save_ytdl_json_path = os.path.join(
            DOWNLOAD_LOCATION,
            str(update.from_user.id) + random + ".json"
        )
        with open(save_ytdl_json_path, "w", encoding="utf8") as outfile:
            json.dump(response_json, outfile, ensure_ascii=False)
        # LOGGER.info(response_json)
        inline_keyboard = []
        for current_r_json in response_json:

            duration = None
            if "duration" in current_r_json:
                duration = current_r_json["duration"]
            if "formats" in current_r_json:
                for formats in current_r_json["formats"]:
                    format_ext = formats.get("ext")
                    get_data = await db.get_blocked_exts(update.from_user.id)
                    if format_ext not in get_data:
                        continue 
                    format_id = formats.get("format_id")
                    format_string = formats.get("format_note")

                    if format_string is None:
                        format_string = formats.get("format")

                    approx_file_size = ""
                    if "filesize" in formats:
                        approx_file_size = humanbytes(formats["filesize"])
                    dipslay_str_uon = (
                            "🎬 "
                            + format_string
                            + " "
                            + approx_file_size
                            + " "
                            + format_ext
                            + " " 
                    ).replace("unknown", "")
                    cb_string_video = "{}|{}|{}|{}".format("video", format_id, format_ext, random)
                    ikeyboard = []
                    if "drive.google.com" in url:
                        ikeyboard = [
                            InlineKeyboardButton(
                                dipslay_str_uon,
                                callback_data=(cb_string_video).encode("UTF-8")
                            )
                        ]
                    else:
                        if format_string is not None and not "audio only" in format_string:
                            ikeyboard = [
                                InlineKeyboardButton(
                                    dipslay_str_uon,
                                    callback_data=(cb_string_video).encode("UTF-8")
                                )
                            ]
                            """if duration is not None:
                                cb_string_video_message = "{}|{}|{}".format(
                                    "vm", format_id, format_ext)
                                ikeyboard.append(
                                    InlineKeyboardButton(
                                        "VM",
                                        callback_data=(
                                            cb_string_video_message).encode("UTF-8")
                                    )
                                )"""
                        elif format_string is not None and not "jpeg" in format_string:
                            await update.reply_text("Yok")
                        else:
                            ikeyboard = [
                                InlineKeyboardButton(
                                    dipslay_str_uon,
                                    callback_data=(cb_string_video).encode("UTF-8"),
                                )
                            ]
                    inline_keyboard.append(ikeyboard)
                if duration is not None:
                    cb_string_64 = "{}|{}|{}|{}".format("audio", "64k", "mp3", random)
                    cb_string_128 = "{}|{}|{}|{}".format("audio", "128k", "mp3", random)
                    cb_string = "{}|{}|{}|{}".format("audio", "320k", "mp3", random)
                    inline_keyboard.append(
                        [
                            InlineKeyboardButton(
                                "🎵 MP3 " + "(" + "64 kbps" + ")",
                                callback_data=cb_string_64.encode("UTF-8"),
                            ),
                            InlineKeyboardButton(
                                "🎵 MP3 " + "(" + "128 kbps" + ")",
                                callback_data=cb_string_128.encode("UTF-8"),
                            ),
                        ]
                    )
                    inline_keyboard.append(
                        [
                            InlineKeyboardButton(
                                "🎵 MP3 " + "(" + "320 kbps" + ")",
                                callback_data=cb_string.encode("UTF-8"),
                            )
                        ]
                    )
            else:
                format_id = current_r_json["format_id"]
                format_ext = current_r_json["ext"]
                cb_string_video = "{}|{}|{}|{}".format("file", format_id, format_ext, random)
                inline_keyboard.append(
                    [
                        InlineKeyboardButton(
                            "🗂 File", callback_data=(cb_string_video).encode("UTF-8")
                        )
                    ]
                )
            break
        inline_keyboard.append([InlineKeyboardButton("♨ İptal et", callback_data='close')])
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
    else:
        # fallback for nonnumeric port a.k.a seedbox.io
        inline_keyboard = []
        cb_string_video = "{}={}={}={}".format("video", "OFL", "ENON", random)
        inline_keyboard.append([
            InlineKeyboardButton(
                "🗂 File",
                callback_data=(cb_string_video).encode("UTF-8")
            )
        ])
        inline_keyboard.append([InlineKeyboardButton("♨ İptal et", callback_data='close')])
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        # LOGGER.info(reply_markup)
    thumbnail = DEF_THUMB_NAIL_VID_S
    thumbnail_image = DEF_THUMB_NAIL_VID_S

    if "thumbnail" in current_r_json:
        if current_r_json["thumbnail"] is not None:
            thumbnail = current_r_json["thumbnail"]
            thumbnail_image = current_r_json["thumbnail"]
    thumb_image_path = DownLoadFile(
        thumbnail_image,
        DOWNLOAD_LOCATION + "/" +
        str(update.from_user.id) + random + ".webp",
        CHUNK_SIZE,
        None,  # bot,
        Translation.DOWNLOAD_START,
        message_id,
        chat_id
    )

    if os.path.exists(thumb_image_path):
        im = Image.open(thumb_image_path).convert("RGB")
        im.save(thumb_image_path.replace(".webp", ".jpg"), "jpeg")
    else:
        thumb_image_path = None

    await send_message.edit_text(
        text=Translation.FORMAT_SELECTION,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )
