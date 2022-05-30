
import os

class Config:

    ENCODE_DIR = os.environ.get("ENCODE_DIR", "encodes")
    BOT_TOKEN = "1974636862:AAG2upXULcE2bjqQRXgk1B1XifQzTL-CP5I"
    APP_ID = 2374174
    API_HASH = "c23db4aa92da73ff603666812268597a"

    #comma seperated user id of users who are allowed to use
    #ALLOWED_USERS = [x.strip(' ') for x in os.environ.get('ALLOWED_USERS','1098504493').split(',')]

    DOWNLOAD_DIR = 'downloads'
    OWNER_ID = 1276627253
    UPDATES_CHANNEL = -1001157048481
    
