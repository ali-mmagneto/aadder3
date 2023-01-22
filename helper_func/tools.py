import os
import shlex
import asyncio
from bs4 import BeautifulSoup
from typing import Tuple
import httpx
import string
import shutil
import random


def get_file_attr(message: Message):

    """
    Combine audio or video or document
    """

    media = message.audio or \
            message.video or \
            message.document

    return media

async def katbin_paste(text: str) -> str:
    """
	paste the text in katb.in website.
	"""

    katbin_url = "https://katb.in"
    client = httpx.AsyncClient()
    response = await client.get(katbin_url)

    soup = BeautifulSoup(response.content, "html.parser")
    csrf_token = soup.find('input', {"name": "_csrf_token"}).get("value")

    try:
        paste_post = await client.post(katbin_url, data={"_csrf_token": csrf_token, "paste[content]": text},
                                       follow_redirects=False)
        output_url = f"{katbin_url}{paste_post.headers['location']}"
        await client.aclose()
        return output_url

    except:
        return "something went wrong while pasting text in katb.in."


def get_readable_time(seconds: int) -> str:
    """
    Return a human-readable time format
    """

    result = ""
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)

    if days != 0:
        result += f"{days}d "
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)

    if hours != 0:
        result += f"{hours}h "
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)

    if minutes != 0:
        result += f"{minutes}m "

    seconds = int(seconds)
    result += f"{seconds}s "
    return result


def get_readable_bytes(value, digits=2, delim="", postfix=""):
    """
    Return a human-readable file size.
    """

    if value is None:
        return None
    chosen_unit = "B"
    for unit in ("KiB", "MiB", "GiB", "TiB"):
        if value > 1000:
            value /= 1024
            chosen_unit = unit
        else:
            break
    return f"{value:.{digits}f}" + delim + chosen_unit + postfix


def get_readable_size(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}

    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def get_readable_bitrate(bitrate_kbps):
    if bitrate_kbps > 10000:
        bitrate = str(round(bitrate_kbps / 1000, 2)) + ' ' + 'Mb/s'
    else:
        bitrate = str(round(bitrate_kbps, 2)) + ' ' + 'kb/s'

    return bitrate


def get_readable_filesize(num):
    for x in {'bytes', 'KB', 'MB', 'GB', 'TB'}:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)

        num /= 1024.0

    return "%3.1f %s" % (num, 'TB')

async def execute(cmnd: str) -> Tuple[str, str, int, int]:
    cmnds = shlex.split(cmnd)
    process = await asyncio.create_subprocess_exec(
        *cmnds,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (stdout.decode('utf-8', 'replace').strip(),
            stderr.decode('utf-8', 'replace').strip(),
            process.returncode,
            process.pid)

async def clean_up(input1, input2=None):
    try:
        os.remove(input1)
    except:
        pass
    try:
        os.remove(input2)
    except:
        pass
