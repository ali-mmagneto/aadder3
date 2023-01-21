import time
import mimetypes
import traceback
from pyrogram import Client, filters
from pyrogram import filters
from pyrogram.file_id import FileId
from pyrogram.types import Message
from helper_func.tools import (
    get_media_file_id,
    get_media_file_size,
    get_media_file_name,
    get_file_type,
    get_file_attr,
    handle_big_rename, 
    handle_not_big
)
from configs import Config
from helper_func.progress_bar import progress_bar


@Client.on_message(filters.command(["rename", "r"]) & filters.private & ~filters.edited)
async def rename_handler(c: Client, m: Message):
    # Ișlem
    editable = await m.reply_text("Şimdi Bana Yeni Dosya Adı Gönder!", quote=True)
    user_input_msg: Message = await c.listen(m.chat.id)
    if user_input_msg.text is None:
        await editable.edit("İşlem İptal Edildi! Text rename yapamiyorum")
        return await user_input_msg.continue_propagation()
    if user_input_msg.text and user_input_msg.text.startswith("/"):
        await editable.edit("İşlem İptal Edildi!")
        return await user_input_msg.continue_propagation()
    _raw_file_name = get_media_file_name(m.reply_to_message)
    if not _raw_file_name:
        _file_ext = mimetypes.guess_extension(get_file_attr(m.reply_to_message).mime_type)
        _raw_file_name = "UnknownFileName" + _file_ext
    if user_input_msg.text.rsplit(".", 1)[-1].lower() != _raw_file_name.rsplit(".", 1)[-1].lower():
        file_name = user_input_msg.text.rsplit(".", 1)[0][:255] + "." + _raw_file_name.rsplit(".", 1)[-1].lower()
    else:
        file_name = user_input_msg.text[:255]
    await editable.edit("Lütfen Bekle ...")
    is_big = get_media_file_size(m.reply_to_message) > (10 * 1024 * 1024)
    if not is_big:
        _default_thumb_ = await db.get_thumbnail(m.from_user.id)
        if not _default_thumb_:
            _m_attr = get_file_attr(m.reply_to_message)
            _default_thumb_ = _m_attr.thumbs[0].file_id \
                if (_m_attr and _m_attr.thumbs) \
                else None
        await handle_not_big(c, m, get_media_file_id(m.reply_to_message), file_name,
                             editable, get_file_type(m.reply_to_message), _default_thumb_)
        return
    file_type = get_file_type(m.reply_to_message)
    _c_file_id = FileId.decode(get_media_file_id(m.reply_to_message))
    try:
        c_time = time.time()
        file_id = await c.custom_upload(
            file_id=_c_file_id,
            file_size=get_media_file_size(m.reply_to_message),
            file_name=file_name,
            progress=progress_bar
            progress_args=(
                "`Yükleniyor..`\n"
                f"DC: {_c_file_id.dc_id}",
                editable,
                c_time
            )
        )
        if not file_id:
            return await editable.edit("Yeniden Adlandırma Başarısız!\n\n"
                                       "Dosyanız Bozulmuş Olabilir :(")
        await handle_big_rename(c, m, file_id, file_name, editable, file_type)
    except Exception as err:
        await editable.edit("Dosya Yeniden Adlandırılamadı!\n\n"
                            f"**Hata:** `{err}`\n\n"
                            f"**Traceback:** `{traceback.format_exc()}`")
