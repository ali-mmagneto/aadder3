
# (c) Shrimadhav uk | @Tellybots_4u

import os

import pyrogram
from config import Config
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from plugins.forcesub import handle_force_subscribe
from script import Script

@pyrogram.Client.on_message(pyrogram.filters.command("h"))
async def help(bot, message, cb=False):
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, message)
      if fsub == 400:
        return
    me = await bot.get_me()
    button = [[
        InlineKeyboardButton(f'🏡 Ev', callback_data='back'),
        InlineKeyboardButton(f'👲 Hakkımda', callback_data='about')
        ],[
        InlineKeyboardButton(f'👥 Kaynak', url='https://t.me/mmagneto'),
        InlineKeyboardButton(f'⛔ Kapat', callback_data='close')
        ]]
    reply_markup = InlineKeyboardMarkup(button)
    if cb:
        await message.message.edit(
            text=Script.HELP_USER.format(bot_name=me.mention),
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
    else:
        await message.reply_text(
            text=Script.HELP_USER.format(bot_name=me.mention),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )


@pyrogram.Client.on_message(pyrogram.filters.command("s"))
async def start(bot, message, cb=False):
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, message)
      if fsub == 400:
        return
    me = await bot.get_me()
    owner = await bot.get_users(Config.OWNER_ID)
    owner_username = owner.username if owner.username else 'AsmSafone'
    button = [[
        InlineKeyboardButton(f'💡 Yardım', callback_data='help'),
        InlineKeyboardButton(f'👲 Hakkımda', callback_data="about")
        ],[
        InlineKeyboardButton(f'🥰 Kaynak', url='https://t.me/mmagneto'),
        InlineKeyboardButton(f'⛔ Kapat', callback_data="close")
        ]]
    reply_markup = InlineKeyboardMarkup(button)
    if cb:
        await message.message.edit(
            text=Script.START_TEXT.format(user_mention=message.from_user.mention, bot_name=me.mention, bot_owner=owner.mention), 
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
    else:
        await message.reply_text(
            text=Script.START_TEXT.format(user_mention=message.from_user.mention, bot_name=me.mention, bot_owner=owner.mention), 
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        ) 


@pyrogram.Client.on_message(pyrogram.filters.command("a"))
async def about(bot, message, cb=False):
    if Config.UPDATES_CHANNEL:
      fsub = await handle_force_subscribe(bot, message)
      if fsub == 400:
        return
    me = await bot.get_me()
    button = [[
        InlineKeyboardButton(f'🏡 Ev', callback_data='back'),
        InlineKeyboardButton(f'❔ Yardım', callback_data='help')
        ],[
        InlineKeyboardButton(f'👥 Güncelleme', url='https://t.me/quickwaste'),
        InlineKeyboardButton(f'⛔ Kapat', callback_data="close")
        ]]
    reply_markup = InlineKeyboardMarkup(button)
    if cb:
        await message.message.edit(
            text=Script.ABOUT.format(bot_name=me.mention),
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
    else:
        await message.reply_text(
            text=Script.ABOUT.format(bot_name=me.mention),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            quote=True
        )
@pyrogram.Client.on_callback_query(pyrogram.filters.regex('^help$'))
async def help_cb(bot, message):
    await message.answer()
    await help(bot, message, True)


@pyrogram.Client.on_callback_query(pyrogram.filters.regex('^close$'))
async def close_cb(bot, message):
    await message.message.delete()
    await message.message.reply_to_message.delete()


@pyrogram.Client.on_callback_query(pyrogram.filters.regex('^back$'))
async def back_cb(bot, message):
    await message.answer()
    await start(bot, message, True)


@pyrogram.Client.on_callback_query(pyrogram.filters.regex('^about$'))
async def about_cb(bot, message):
    await message.answer()
    await about(bot, message, True)


@pyrogram.Client.on_callback_query(pyrogram.filters.regex('^refreshmeh$'))
async def refreshmeh_cb(bot, message):
    if Config.UPDATES_CHANNEL:
        invite_link = await bot.create_chat_invite_link(int(Config.UPDATES_CHANNEL))
        try:
            user = await bot.get_chat_member(int(Config.UPDATES_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await message.message.edit(
                    text="Sorry Sir, You are Banned. Contact My [Support Group](https://t.me/safothebot).",
                    parse_mode="enums.MARKDOWN",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await message.message.edit(
                text="**Lan Sen Hala Benim Kanalıma Katılmamışsın!**\n\nYopun Yüklenmeden Dolayı Sadece Kanal Üyeleri Kullanabilir Botu!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🤖 Benim Kanalım 🤖", url=invite_link.invite_link)
                        ],
                        [
                            InlineKeyboardButton("🔄 Yenile 🔄", callback_data="refreshmeh")
                        ]
                    ]
                ),
                parse_mode="enums.MARKDOWN"
            )
            return
        except Exception:
            await message.message.edit(
                text="Birşeyler Ters Gitti. İletişime geç [Destek](https://t.me/mmagneto) ile.",
                parse_mode=enums.MARKDOWN,
                disable_web_page_preview=True
            )
            return
    await message.answer()
    await start(bot, message, True)

