from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Help(object):

HELP_TEXT ="""<b>Welcome to the Help Menu</b>

1.) Send a Video file or url.
2.) Send a subtitle file (ass or srt)
3.) Choose you desired type of muxing!

To give custom name to file send it with url seperated with |
<i>url|custom_name.mp4</i>

<b>Note : </b><b>Please note that only english type fonts are supported in hardmux other scripts will be shown as empty blocks on the video!</b>

<a href="https://github.com/sahaynitin/video-sub-merger">Repo URL</a>"""


HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('🤖 About', callback_data='about'),
        InlineKeyboardButton('Close 🔐', callback_data='close')
        ]]
    )
