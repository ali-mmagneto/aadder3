
import os

class Config:

    ENCODE_DIR = os.environ.get("ENCODE_DIR", "encodes")
    BOT_TOKEN = os.environ.get('BOT_TOKEN', None)
    APP_ID = os.environ.get('APP_ID', None)
    API_HASH = os.environ.get('API_HASH', None)

    #comma seperated user id of users who are allowed to use
    #ALLOWED_USERS = [x.strip(' ') for x in os.environ.get('ALLOWED_USERS','1098504493').split(',')]

    DOWNLOAD_DIR = 'downloads'
    OWNER_ID = int(os.environ.get("OWNER_ID", 1316963576))
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", None)
    
