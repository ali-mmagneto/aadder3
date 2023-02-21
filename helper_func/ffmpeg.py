#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


from helper_func.tools import execute, clean_up
from helper_func.upload import upload_audio, upload_subtitle

import os
import time
import random
import asyncio

from PIL import Image
from database.database import db
from config import Config
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)


async def DocumentThumb(bot, update):
    thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
    db_thumbnail = await db.get_thumbnail(update.from_user.id)
    if db_thumbnail is not None:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
        Image.open(thumbnail).convert("RGB").save(thumbnail)
        img = Image.open(thumbnail)
        img.resize((100, 100))
        img.save(thumbnail, "JPEG")
    else:
        thumbnail = None

    return thumbnail


async def VideoThumb(bot, update, duration, path, vrandom):
    default_thumb_image_path = Config.DOWNLOAD_LOCATION + \
                               "/" + str(update.from_user.id) + f'{vrandom}' + ".jpg"
    thumb_image_path = Config.DOWNLOAD_LOCATION + \
                       "/" + str(update.from_user.id) + ".jpg"
    db_thumbnail = await db.get_thumbnail(update.from_user.id)
    if db_thumbnail is not None:
        thumbnail = await bot.download_media(message=db_thumbnail, file_name=thumb_image_path)
    else:
        if os.path.exists(default_thumb_image_path):
            thumbnail = default_thumb_image_path
        else:
            thumbnail = await take_screen_shot(path, os.path.dirname(path),
                                               random.randint(0, duration - 1))

    return thumbnail


async def VideoMetaData(download_directory):
    width = 0
    height = 0
    duration = 0
    metadata = extractMetadata(createParser(download_directory))
    if metadata is not None:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if metadata.has("width"):
            width = metadata.get("width")
        if metadata.has("height"):
            height = metadata.get("height")

    return width, height, duration


async def VMMetaData(download_directory):
    width = 0
    duration = 0
    metadata = extractMetadata(createParser(download_directory))
    if metadata is not None:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if metadata.has("width"):
            width = metadata.get("width")

    return width, duration


async def AudioMetaData(download_directory):
    duration = 0
    metadata = extractMetadata(createParser(download_directory))
    if metadata is not None:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds

    return duration


async def place_water_mark(input_file, output_file, water_mark_file):
    watermarked_file = output_file + ".watermark.png"
    metadata = extractMetadata(createParser(input_file))
    width = metadata.get("width")
    # https://stackoverflow.com/a/34547184/4723940
    shrink_watermark_file_genertor_command = [
        "ffmpeg",
        "-i", water_mark_file,
        "-y -v quiet",
        "-vf",
        "scale={}*0.5:-1".format(width),
        watermarked_file
    ]
    # print(shrink_watermark_file_genertor_command)
    process = await asyncio.create_subprocess_exec(
        *shrink_watermark_file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    commands_to_execute = [
        "ffmpeg",
        "-i", input_file,
        "-i", watermarked_file,
        "-filter_complex",
        # https://stackoverflow.com/a/16235519
        # "\"[0:0] scale=400:225 [wm]; [wm][1:0] overlay=305:0 [out]\"",
        # "-map \"[out]\" -b:v 896k -r 20 -an ",
        "\"overlay=(main_w-overlay_w):(main_h-overlay_h)\"",
        # "-vf \"drawtext=text='@FFMovingPictureExpertGroupBOT':x=W-(W/2):y=H-(H/2):fontfile=" + Config.FONT_FILE + ":fontsize=12:fontcolor=white:shadowcolor=black:shadowx=5:shadowy=5\"",
        output_file
    ]
    # print(commands_to_execute)
    process = await asyncio.create_subprocess_exec(
        *commands_to_execute,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    return output_file


async def take_screen_shot(video_file, output_directory, ttl):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + \
                        "/" + str(time.time()) + ".jpg"
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        str(ttl),
        "-i",
        video_file,
        "-vframes",
        "1",
        out_put_file_name
    ]
    # width = "90"
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None


async def cult_small_video(video_file, output_directory, start_time, end_time):
    # https://stackoverflow.com/a/13891070/4723940
    out_put_file_name = output_directory + \
                        "/" + str(round(time.time())) + ".mp4"
    file_genertor_command = [
        "ffmpeg",
        "-i",
        video_file,
        "-ss",
        start_time,
        "-to",
        end_time,
        "-async",
        "1",
        "-strict",
        "-2",
        out_put_file_name
    ]
    process = await asyncio.create_subprocess_exec(
        *file_genertor_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.lexists(out_put_file_name):
        return out_put_file_name
    else:
        return None


async def generate_screen_shots(
        video_file,
        output_directory,
        is_watermarkable,
        wf,
        min_duration,
        no_of_photos
):
    metadata = extractMetadata(createParser(video_file))
    duration = 0
    if metadata is not None:
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
    if duration > min_duration:
        images = []
        ttl_step = duration // no_of_photos
        current_ttl = ttl_step
        for looper in range(0, no_of_photos):
            ss_img = await take_screen_shot(video_file, output_directory, current_ttl)
            current_ttl = current_ttl + ttl_step
            if is_watermarkable:
                ss_img = await place_water_mark(ss_img, output_directory + "/" + str(time.time()) + ".jpg", wf)
            images.append(ss_img)
        return images
    else:
        return None


async def extract_audio(client, message, data):
    await message.edit_text("`Dosyan Ayıklanıyor...`")

    dwld_loc = data['location']
    out_loc = data['location'] + ".mp3"

    if data['name'] == "mp3":
        out, err, rcode, pid = await execute(f"ffmpeg -i '{dwld_loc}' -map 0:{data['map']} -c copy '{out_loc}' -y")
        if rcode != 0:
            await message.edit_text("**Hata Oldu.**")
            print(err)
            await clean_up(out_loc)
            return
    else:
        out, err, rcode, pid = await execute(f"ffmpeg -i '{dwld_loc}' -map 0:{data['map']} '{out_loc}' -y")
        if rcode != 0:
            await message.edit_text("**Error Occured. See Logs for more info.**")
            print(err)
            await clean_up(out_loc)
            return

    await upload_audio(client, message, out_loc)



async def extract_subtitle(client, message, data):
    await message.edit_text("`Dosyan Ayıklanıyor`")

    dwld_loc = data['location']
    out_loc = data['location'] + ".srt"   

    out, err, rcode, pid = await execute(f"ffmpeg -i '{dwld_loc}' -map 0:{data['map']} '{out_loc}' -y")
    if rcode != 0:
        await message.edit_text("**Error Occured. See Logs for more info.**")
        print(err)
        await clean_up(out_loc)
        return

    await upload_subtitle(client, message, out_loc)
    
