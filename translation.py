
class Translation (object):

    

    
    
    DOWNLOAD_SUCCESS = """Dosya Başarı İle İndirildi!

Geçen Süre : {} saniye."""
    FILE_SIZE_ERROR = "HATA : URL'den Dosya Boyutu Ayıklanamıyor!"
    MAX_FILE_SIZE = "Dosya boyutu 2 Gb'den büyük. Telegramın getirdiği sınır da bu!"
    LONG_CUS_FILENAME = """Sağladığınız dosya adı 60 karakterden büyük.
Lütfen daha kısa bir ad girin."""
    UNSUPPORTED_FORMAT = "Hata : Dosya Türü {} Desteklenmiyor!"
    START_TEXT = """Merhaba {},\n
Ben bir URL Yükleyicisiyim!
Bu Botu kullanarak HTTP/HTTPS bağlantılarını yükleyebilirsiniz!"""
    FORCE_TXT = """
**Sadece kanal aboneleri kullanabilir.**
(__Katıldıktan sonra tekrar deneyin.__)
"""
    LOGIN_TXT = """
**Öncelikle butona basarak oturum açınız.**
__(Şifreyi bilmiyor musunuz? Bilmecede saklı!..)__
"Daldan dala tırmanır, tüm muzlara saldırır."
"""
    BUTTON_TEXT = "Katıl"
    FORMAT_SELECTION = """**İstenen formatı seçin:** 👇\n--belirtilen-- __dosya boyutu yaklaşık olabilir.__"""
    SET_CUSTOM_USERNAME_PASSWORD = """\n\nBu videoyu indirmek istiyorsanız, aşağıdaki biçimi sağlayın:
    URL | dosyaadı | kullanıcıadı | parola"""
    DOWNLOAD_START = "**Dosya Adı:** {}\n\nİndiriliyor.. 📥"
    UPLOAD_START = "Yükleniyor.."
    RCHD_TG_API_LIMIT = "{} saniye içinde İndirildi.\nAlgılanan Dosya Boyutu: {}\nÜzgünüm. Ancak, Telegram API sınırlamaları nedeniyle 2000MB'den büyük dosyaları yükleyemiyorum."
    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = "{} saniye içinde İndirildi.\n{} saniye içinde yüklendi."
    AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS_PRE = "{} saniye içinde İndirildi.\n{} saniye içinde yüklendi.\n\nDosyan 2 Gb'tan büyük olduğu için PRE_LOG Değişkenine girdiğin kanalda!"
    SAVED_CUSTOM_THUMB_NAIL = "**✔️ Kapak fotoğrafı kaydedildi.**"
    DEL_ETED_CUSTOM_THUMB_NAIL = "**🗑️ Kapak fotoğrafı başarıyla temizlendi.**"
    CUSTOM_CAPTION_UL_FILE = "{}"
    NO_VOID_FORMAT_FOUND = "**YT-DLP**:\n{}"
    SETTINGS = "**Ayarlarlarınızı buradan yapabilirsiniz.**"
    HELP_TEXT = """Nasıl kullanılır? Aşağıdaki adımları izleyin!
1. URL gönderin.
2. Kapak fotoğrafı için fotoğraf gönderin. (İsteğe bağlı)
3. Buton seçin.
Bot cevap vermediyse @mmagneto ile iletişime geçin"""
    UPLOADER = ""
    THUMBNAIL_TEXT = "Thumbnail ayarlamak için bana herhangi bir fotoğraf gönderin."
    IFLONG_FILE_NAME = """Telegram tarafından izin verilen dosya adı sınırı {alimit} karakterdir.\n\nBana verilen dosya adında {num} karakter var.\nLütfen dosya adınızı kısaltın ve tekrar deneyin!"""
    SLOW_URL_DECED = "Bu url çok yavaş dostum"

    DOWNLOAD_PROGRESS = "`█`"
    UPLOAD_PROGRESS = "`░`"

    PROGRESS = """`
{0}% / {1}
P: {2}
Hız: {3}/s
ETA: {4}
    `"""
    LOG_TEXT_P = """
#YeniKullanıcı
ID - <code>{}</code>
Adı - {}
Dil - {}
Kullanıcı Adı - {}
DC - {}
Bot - @{}
"""
    START_BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('🏴‍☠ Kanal', url='https://t.me/mmagneto3'),
            InlineKeyboardButton('⚙ Ayarlar', callback_data='Settings')
        ], [
            InlineKeyboardButton('❔ Yardım Menüsü', callback_data='help')
        ]]
    )
    LOGIN_BUTTON = InlineKeyboardMarkup([
        [
            InlineKeyboardButton('Oturum Aç 🔐', callback_data='login🔑')
        ]
    ])
    HELP_BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('🔙 Geri', callback_data='home')
        ]]
    )
