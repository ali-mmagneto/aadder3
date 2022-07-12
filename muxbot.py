
# (c) Tellybots | Shrimadhavuk


import os

from config import Config

from helper_func.dbhelper import Database as Db
db = Db().setup()

import pyrogram


if __name__ == '__main__':

    if not os.path.isdir(Config.DOWNLOAD_DIR):
        os.mkdir(Config.DOWNLOAD_DIR)
    if not os.path.isdir(Config.ENCODE_DIR):
        os.mkdir(Config.ENCODE_DIR)

    plugins = dict(root='plugins')

    app = pyrogram.Client(
        'videomerger',
        string_session= Config.STRING_SESSION,
        api_id = Config.APP_ID,
        api_hash = Config.API_HASH,
        plugins = plugins
    )
    app.run()
