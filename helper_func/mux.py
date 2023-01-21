
from config import Config
import time
import re
import asyncio


progress_pattern = re.compile(
    r'(frame|fps|size|time|bitrate|speed)\s*\=\s*(\S+)'
)

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

async def read_stderr(start, msg, process):
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
                        await msg.edit(text=text)
                    except Exception as e:
                        print(e)

async def sesekle_vid(vid_filename, aud_filename, msg):

    start = time.time()
    vid = Config.DOWNLOAD_DIR+'/'+vid_filename  + '.mp4'
    sub = Config.DOWNLOAD_DIR+'/'+aud_filename

    out_file = '.'.join(vid_filename.split('.')[:-1])
    output = out_file+'1.mkv'
    out_location = Config.DOWNLOAD_DIR+'/'+output
    aud_ext = aud_filename.split('.').pop()
    command = [
            'ffmpeg','-hide_banner',
            '-i',vid,
            '-i',sub,
            '-map','0:v','-map','1:a',
            '-c:v','copy',
            '-y',out_location
            ]

    process = await asyncio.create_subprocess_exec(
            *command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )

    # https://github.com/jonghwanhyeon/python-ffmpeg/blob/ccfbba93c46dc0d2cafc1e40ecb71ebf3b5587d2/ffmpeg/ffmpeg.py#L114
    
    await asyncio.wait([
            read_stderr(start,msg, process),
            process.wait(),
        ])
    
    if process.returncode == 0:
        await msg.edit('Ses Ekleme Başarı İle Tamamlandı!\n\nGeçen Süre : {} saniye'.format(round(start-time.time())))
    else:
        await msg.edit('Ses Eklenirken Bir Hata Oluştu!')
        return False
    time.sleep(2)
    return output
