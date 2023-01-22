# :d

import os

import pyrogram
from config import Config
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

from script import Script
from pyrogram import enums

buttons=ReplyKeyboardMarkup(
            [
                ["Help⚡️"],
                ["Status😔"]
                        
            ],
            resize_keyboard=True
        )

buttonh=ReplyKeyboardMarkup(
            [
                ["Start⚡️"],
                ["Status😔"]
                        
            ],
            resize_keyboard=True
        )


@pyrogram.Client.on_message(pyrogram.filters.command("video") | pyrogram.filters.regex('Tlou1'))
async def video(bot, message, cb=False):
    bot.send_video(message.chat.id, "BAACAgQAAxkBAAETvetjzXW6_qdazTy47BRoIanhhAOYbAACGhAAAkBOYVJHRbNadlzefS0E")


@pyrogram.Client.on_message(pyrogram.filters.command("help") | pyrogram.filters.regex('Help⚡️'))
async def help(bot, message, cb=False):
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
            text=Script.HELP_USER,
            disable_web_page_preview=True,
            reply_markup=buttonh
        )
    else:
        await message.reply_text(
            text=Script.HELP_USER,
            disable_web_page_preview=True,
            reply_markup=buttonh,
            quote=True
        )


@pyrogram.Client.on_message(pyrogram.filters.command("start") | pyrogram.filters.regex('Start⚡️'))
async def start(bot, message, cb=False):
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
            text=Script.START_TEXT, 
            disable_web_page_preview=True,
            reply_markup=buttons
        )
    else:
        await message.reply_text(
            text=Script.START_TEXT, 
            disable_web_page_preview=True,
            reply_markup=buttons,
            quote=True
        ) 


@pyrogram.Client.on_message(pyrogram.filters.command("about"))
async def about(bot, message, cb=False):
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
            text=Script.ABOUT,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
    else:
        await message.reply_text(
            text=Script.ABOUT,
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

