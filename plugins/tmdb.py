# Coded by :d
from pyrogram import Client, filters
import requests
import json
from PIL import Image

@Client.on_message(filters.command('tmdb'))
async def tmdbgetir(bot, message):
    try:
        sayi = 2 # benim uygun gördüğüm gösterilecek film sayısı
        mes = message.text.split(" ", 1)
        if len(mes) == 1:
            await message.reply_text("Hatalı Kullanım :/ Doğru kullanım:\n\n`/tmdb Bullet Train`")
            return
        else:
            aranacak = mes[1]
        url = f"https://api.themoviedb.org/3/search/movie?api_key=f2d91ec751ea4b19fbdc66650232b17b&query={aranacak}&language=tr" 
        response = requests.get(url)
        data = response.json()
        text = ""
        say = 0
        for i in data["results"]:
            say += 1
            poster = f"{i['poster_path']}"
            photo1 = f"https://image.tmdb.org/t/p/w1280{poster}"
            img = Image.open(requests.get(photo1, stream = True).raw)
            img.save(f"downloads/photo.jpg")
            text += f"**İsim**: `{i['original_title']}`\n\n**Dil**: `{i['original_language']}`\n\n**Konu**: `{i['overview']}`\n\n**Tmdb Puanı**: `{i['vote_average']}`/10\n\n**Oylayan Sayısı**: `{i['vote_count']}`\n\n**Yayın Tarihi**: `{i['release_date']}`"
            await bot.send_photo(
                chat_id = message.chat.id,
                photo = "downloads/photo.jpg",
                caption = text)
            text = ""
            if int(say) == int(sayi):
                return
    except Exception as e:
        await message.reply_text(f"`{e}`")
