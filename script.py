from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Script(object):

    START_TEXT = """<b>Hey,</b>\n
<b>This is a Telegram Bot to Merge Subtitle into a video</b>

<b>Send me a Telegram file to Get started</b>

Use help Command for more details..

    """
    START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🤔 Help', callback_data='help'),
        InlineKeyboardButton('🤖 About', callback_data='about'),
        ],[
        InlineKeyboardButton('Close🔐', callback_data='close')
        ]]
    )
    
    
