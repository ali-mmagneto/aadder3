from pyrogram import Client, filters 
import requests
from unidecode import unidecode
import logging
from bs4 import BeautifulSoup
import openai
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=logging.INFO)
LOGGER = logging.getLogger(__name__)

session = requests.Session()

@Client.on_message(filters.command('image'))
async def linkgetir(bot, message):
    try:
        text = unidecode(message.text).split()
        prompt = text[1]
        response = openai.Image.create(
            prompt="a white siamese cat",
            n=1,
            size="1024x1024"
            openai.api_key="org-JjKHfNWvXzd2Y5KrB7qkqIhJ"
            )
        image_url = response['data'][0]['url']
        await message.reply_text(image_url)
    except Exception as e:
        await message.reply_text(e)
        
