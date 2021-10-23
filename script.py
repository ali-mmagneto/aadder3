from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Script(object):

    START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🤔 Help', callback_data='help'),
        InlineKeyboardButton('🤖 About', callback_data='about'),
        ],[
        InlineKeyboardButton('Close🔐', callback_data='close')
        ]]
    )
    
    
