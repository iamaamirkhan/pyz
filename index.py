#pylint:disable=C0114
import logging
import os
from pyrogram import Client
from pyrogram.errors import RPCError
from pyrogram.errors import BadRequest
from pyrogram.errors import FloodWait

logging.basicConfig(level=logging.INFO)



bot = Client(
    'bot',
    api_id= 8131280, #get it from https://my.telegram.org/auth
    api_hash="b8bae4ec39d070dad7d0a1245111d154", #get it from https://my.telegram.org/auth
    bot_token="5530967960:AAENYomDlFCHyW3N88G13IW6CYPHfaovZEU", #get it from @Botfather
    plugins=dict(root="plugins"),
    parse_mode="html")


try:
    bot.run()
except Exception as e:
    print(e)
        