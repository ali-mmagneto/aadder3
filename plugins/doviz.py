from pyrogram import Client, filters
import requests

dovizurl = "https://api.genelpara.com/embed/doviz.json"

@Client.on_message(filters.command('doviz'))
async def dovizcek(bot, message):
    try:
        distek = requests.get(dovizurl)
        dveri = distek.json()
        dsonuc = dveri['USD']
        eistek = requests.get(dovizurl)
        everi = eistek.json()
        esonuc = everi['EUR']
        dyön = f"{dsonuc['d_yon']}"
        eyön = f"{esonuc['d_yon']}"
        artis = "caret-up"
        azalis = "caret-down"
        if dyön == azalis:
            demoji = "📉" 
        else:
            demoji = "📈"
        if eyön == azalis:
            eemoji = "📉" 
        else:
            eemoji = "📈"
        text = f"{demoji} Dolar:\nAlış: `₺{dsonuc['alis']}`\nSatış: `₺{dsonuc['satis']}`\nDeğişim: `{dsonuc['d_oran']}%`\n\n{eemoji} Euro:\nAlış: `₺{esonuc['alis']}`\nSatış: `₺{esonuc['satis']}`\nDeğişim: `{esonuc['d_oran']}%`"
        await bot.send_message(
            chat_id=message.chat.id,
            text=text)
    except Exception as e:
        print(e)
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"`{e}`")

@Client.on_message(filters.command('bitcoin'))
async def bitcoincek(bot, message):
    try:
        bistek = requests.get(dovizurl)
        bveri = bistek.json()
        bsonuc = bveri['BTC']
        etistek = requests.get(dovizurl)
        etveri = etistek.json()
        etsonuc = etveri['ETH']
        byön = f"{bsonuc['d_yon']}"
        etyön = f"{etsonuc['d_yon']}"
        artis = "caret-up"
        azalis = "caret-down"
        if byön == azalis:
            bemoji = "📉" 
        else:
            bemoji = "📈"
        if etyön == azalis:
            etemoji = "📉" 
        else:
            etemoji = "📈"
        text = f"{bemoji} Bitcoin:\nAlış: `₺{bsonuc['alis']}`\nSatış: `₺{bsonuc['satis']}`\nDeğişim: `{bsonuc['d_oran']}%`\n\n{etemoji} Ethereum:\nAlış: `₺{etsonuc['alis']}`\nSatış: `₺{etsonuc['satis']}`\nDeğişim: `{etsonuc['d_oran']}%`"
        await bot.send_message(
            chat_id=message.chat.id,
            text=text)
    except Exception as e:
        print(e)
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"`{e}`")


@Client.on_message(filters.command('altin'))
async def altincek(bot, message):
    try:
        aistek = requests.get(dovizurl)
        averi = aistek.json()
        asonuc = averi['C']
        gistek = requests.get(dovizurl)
        gveri = gistek.json()
        gsonuc = gveri['GA']
        artis = "caret-up"
        azalis = "caret-down"
        gyön = f"{gsonuc['d_yon']}"
        ayön = f"{asonuc['d_yon']}"
        if ayön == azalis:
            aemoji = "📉" 
        else:
            aemoji = "📈"
        if gyön == azalis:
            gemoji = "📉" 
        else:
            gemoji = "📈"
        text = f"{aemoji} Çeyrek Altın:\nAlış: `₺{asonuc['alis']}`\nSatış: `₺{asonuc['satis']}`\nDeğişim: `{asonuc['d_oran']}%`\n\n{gemoji} Gram Altın:\nAlış: `₺{gsonuc['alis']}`\nSatış: `₺{gsonuc['satis']}`\nDeğişim: `{gsonuc['d_oran']}%`"
        await bot.send_message(
            chat_id=message.chat.id,
            text=text)
    except Exception as e:
        print(e)
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"`{e}`")
