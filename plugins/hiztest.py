#:d

import os

import speedtest
from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command("speedtest"))
async def run_speedtest(bot, message):
    hiztesti = await message.reply_text("`⚡️ Hız Testi Yapılıyor`")
    try:
        hiztest = speedtest.Speedtest()
        hiztest.get_best_server()
        hiztesti = await hiztesti.edit("`⚡️ İndirme hızı ölçülüyor... `")
        hiztest.download()
        hiztesti = await hiztesti.edit("`⚡️ Yükleme hızı ölçülüyor...`")
        hiztest.upload()
        hiztest.results.share()
        result = hiztest.results.dict()
    except Exception as e:
        await hiztesti.edit(e)
        return
    hiztesti = await hiztesti.edit("`🔄 Sonuçlar Getiriliyor...`")
    hiztestifoto = hiztest.results.share()

    sonuccaption = f"""💡 <b>Hız Testi Sonucu</b>
    
<u><b>Şirket:<b></u>
<b>ISP:</b> {result['client']['isp']}
<b>Ülke:</b> {result['client']['country']}
  
<u><b>Sunucu:</b></u>
<b>İsim:</b> {result['server']['name']}
<b>Ülke:</b> {result['server']['country']}, {result['server']['cc']}
<b>Sponsor:</b> {result['server']['sponsor']}
⚡️ <b>Ping:</b> {result['ping']}"""
    msg = await bot.send_photo(
        chat_id=message.chat.id, photo=hiztestifoto, caption=sonuccaption
    )
    os.remove(hiztestifoto)
    await hiztesti.delete()
