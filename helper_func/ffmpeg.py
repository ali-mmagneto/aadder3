#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @trojanzhex


from helper_func.tools import execute, clean_up
from helper_func.upload import upload_audio, upload_subtitle

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
    
