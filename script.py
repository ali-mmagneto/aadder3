from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Script(object):
  ABOUT = """
🤖 **Adım:** {bot_name}

📝 **Dil:** [Python](https://www.python.org)

📚 **Kütüphane:** [Pyrogram](https://docs.pyrogram.org)

📡 **Sunucu:** [Heroku](https://heroku.com)

🧑‍💻 **Geliştirici:** [Napçan](https://t.me/mmagneto)

👥 **Destek:** [Napçan](https://t.me/mmagneto)

📢 **Kanalım:** [Napçan](https://t.me/quickwaste)
"""

  HELP_USER = """
Ben **{bot_name}**

Yardım Kısmına Hoşgeldin

1.) Bir Video Dosyası Gönder.
2.) Bir Altyazı Dosyası Gönder. (ass Yada srt)
3.) Altyazı Türünü Seç!

Dosyaya özel ad vermek için url ile ayrılmış olarak gönderin.|
url|custom_name.mp4

Note :Hardmux'ta yalnızca İngilizce yazı tiplerinin desteklendiğini lütfen unutmayın, diğer komut dosyaları videoda boş bloklar olarak gösterilecektir! 

**Oluşturan 💕 @mmagneto**
"""

  START_TEXT = """
**Hey** {user_mention}

HOŞLGELDİN **{bot_name}**\n
Sana Videolara Altyazı Eklemen Konusumda Yardımcı Olacağım\n
**Oluşturan 💕 @mmagneto
"""

    
    
