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

  HELP_USER = """/extract - Videodan Ses veya Alt Yazı ayıklar.

/mediainfo - Video veya Sesten Mediainfo alır ve hem txt olarak atar hemde Katbin'e yazdırır.

/ses - Videoya eklenecek sesi indirir.

/video - ses eklenecek videoyu indirir. 

/sesekle - ses ekleme işlemini başlatır.

/aac - Video Sesinizi aac'ye çevirir.

/ss - Yanıtladığınız Dosyadan Screenshot alır.

/status - bot durumunu gösterir.

/restart - botu tekrar başlatır.

/log - log dosyası gönderir. 

/speedtest - Sunucu Hızını Getirir.

Foto gönderince oto thumb olarak alır. 

/delthumb - thumbı siler. 

/get <dizin> - Bir dizindeki dosyaları sıralar. 

/getfile <dizin/dosya adı> - Belirtilen dosyayı getirir.

/rename <Yeni İsim> - Videoya yeni isim koyar. 

/indir - yanıtladığınız urlyi yetedelepe ile indirir.

/syukle - Streamtape'e yanıtladığınız videoyu yükler.

/sindir - Streamtape'den Video indirir.

/film {kanal id-username} {kopyalancak ilk mesaj id} {kopyalanacak son mesaj id} - Bot Üzerinden Kanal Kopyalar.

/gizlifilm {kanal id-username} {kopyalancak ilk mesaj id} {kopyalanacak son mesaj id} - User Üzerinden kanal kopyalar.
"""

  START_TEXT = """
HOŞGELDİN **{user_mention}**\n
Ben Bir video dosyası ile ses dosyasını tek bir videoda birleștiren bir botum iyi kullanımlar.\n\nKullanmayı bilmiyorsan /help komutunu kullan..
"""

    
    
