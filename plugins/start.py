import time
from pyrogram import Client
import requests
from requests.exceptions import ProxyError
import re
# import bs4
from pyrogram import Client, filters
import json

@Client.on_message(filters.command(["start", "make"], prefixes=[".", "/", "!"], case_sensitive=False) & filters.text)
async def gen(Client , message):
    try:
        await Client.send_chat_action(message.chat.id, "typing")
        await message.reply_text(f"<b>Hey @{message.from_user.username}!\nIf you are interested in knowing my commands send /cmds By the way, your UserID is:  </b><code>{message.from_user.id}</code>", parse_mode="html")
    
    except Exception as e:
        print(e)