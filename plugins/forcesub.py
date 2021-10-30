import asyncio
from config import Config
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

async def handle_force_subscribe(bot, message):
    try:
        invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return 400
    try:
        user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), message.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=message.from_user.id,
                text="Üzgünüm Dostum Banlandın. İletişime geç [Destek](https://t.me/mmagneto)ile.",
                parse_mode="markdown",
                disable_web_page_preview=True,
                reply_to_message_id=message.message_id,
            )
            return 400
    except UserNotParticipant:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="**Lütfen beni kullanabilmek için Kanalıma Katıl!**\n\nAşırı Yükleme Nedeniyle Beni Yalnızca Kanal Aboneleri Kullanabilir!",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Katıl işte 🤖", url=invite_link.invite_link)
                    ],
                    [
                        InlineKeyboardButton("🔄 Yenile 🔄", callback_data="refreshmeh")
                    ]
                ]
            ),
            parse_mode="markdown",
            reply_to_message_id=message.message_id,
        )
        return 400
    except Exception:
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Bir Şeyler Ters Gitti. İletişime geçin [Destek](https://t.me/mmagneto) ile.",
            parse_mode="markdown",
            disable_web_page_preview=True,
            reply_to_message_id=message.message_id,
        )
        return 400

