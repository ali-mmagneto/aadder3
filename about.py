from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class About(object):

    ABOUT_TEXT = """
**Bot :** `Video Subtitle Merger`
**Creator :** [Tellybots_4u](https://telegram.me/tellybots_4u)
**Channel :** [Tellybots_4u](https://telegram.me/tellybots_4u)
**Credits :** `Everyone in this journey`
**Language :** [Python3](https://python.org)
**Library :** [Pyrogram v1.2.0](https://pyrogram.org)
**Server :** [Heroku](https://heroku.com)
"""
    ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🏠 Home', callback_data='home'),
        InlineKeyboardButton('Close 🔐', callback_data='close')
        ]]
    )
