import os
import time
import ffmpeg
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser


import os
import time
import asyncio
import ffmpeg
from subprocess import check_output
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from config import Config


def ReadableTime(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result

def get_codec(filepath, channel="v:0"):
    output = check_output(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            channel,
            "-show_entries",
            "stream=codec_name,codec_tag_string",
            "-of",
            "default=nokey=1:noprint_wrappers=1",
            filepath,
        ]
    )
    return output.decode("utf-8").split()


async def encode(filepath):
    path, extension = os.path.splitext(filepath)
    file_name = os.path.basename(path)
    encode_dir = os.path.join(
        Config.ENCODE_DIR,
        file_name
    )
    output_filepath = encode_dir + '.mp4'
    assert (output_filepath != filepath)
    if os.path.isfile(output_filepath):
        print('"{}" Atlanıyor: dosya zaten var'.format(output_filepath))
    print(filepath)

    # Get the audio and subs channel codec
    audio_codec = get_codec(filepath, channel='a:0')

    if not audio_codec:
        audio_opts = '-c:v copy'
    elif audio_codec[0] in 'aac':
        audio_opts = '-c:v copy'
    else:
        audio_opts = '-c:a aac -c:v copy'

    command = ['ffmpeg', '-y', '-i', filepath]
    command.extend(audio_opts.split())
    proc = await asyncio.create_subprocess_exec(
        *command, output_filepath,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await proc.communicate()
    return output_filepath

def get_thumbnail(in_filename, path, ttl):
    out_filename = os.path.join(path, str(time.time()) + ".jpg")
    open(out_filename, 'a').close()
    try:
        (
            ffmpeg
            .input(in_filename, ss=ttl)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        return out_filename
    except ffmpeg.Error as e:
      return None

def get_duration(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("duration"):
      return metadata.get('duration').seconds
    else:
      return 0

def get_width_height(filepath):
    metadata = extractMetadata(createParser(filepath))
    if metadata.has("width") and metadata.has("height"):
      return metadata.get("width"), metadata.get("height")
    else:
      return 1280, 720


