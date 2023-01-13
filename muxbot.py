
# (c) Tellybots | Shrimadhavuk


import os

from config import Config

from helper_func.dbhelper import Database as Db
db = Db().setup()

import pyrogram
from pyrogram import Client


if __name__ == '__main__':

    if not os.path.isdir(Config.DOWNLOAD_DIR):
        os.mkdir(Config.DOWNLOAD_DIR)
    if not os.path.isdir(Config.ENCODE_DIR):
        os.mkdir(Config.ENCODE_DIR)
