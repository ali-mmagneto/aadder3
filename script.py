from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Script(object):
  ABOUT = """
🤖 **Adım:** {bot_name}

📝 **Dil:** [Python](https://www.python.org)

📚 **Kütüphane:** [Pyrogram](https://docs.pyrogram.org)

📡 **Sunucu:** [Napçan](https://heroku.com)

🧑‍💻 **Geliştirici:** [Napçan](https://t.me/mmagneto)

👥 **Destek:** [Napçan](https://t.me/mmagneto)

📢 **Kanalım:** [Napçan](https://t.me/quickwaste)
"""

  HELP_USER = """
Ben **{bot_name}**

Yardım Kısmına Hoşgeldin

1.) Bir Video Dosyası Gönder.
2.) Bir Ses Dosyası Gönder. (ass Yada srt)
3.) /sesekle komutunu kullan!
"""

  START_TEXT = """
HOŞGELDİN **{user_mention}**\n
Ben Bir video dosyası ile ses dosyasını tek bir videoda birleștiren bir botum iyi kullanımlar.\n\nKullanmayı bilmiyorsan /help komutunu kullan..
"""

    
    
