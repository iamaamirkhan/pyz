# from datetime import datetime
# import asyncio
from bson.json_util import dumps,RELAXED_JSON_OPTIONS
# import json
import time
from telegraph import upload_file
# from pymongo.mongo_client import MongoClient
# import pymongo.errors
from pymongo.errors import *
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
BOT_USERNAME = "AltbalajiCheckerBot"
from datetime import datetime
@Client.on_message(filters.command(['cmds','gates' ,'commands', f'gates@{BOT_USERNAME}' , f'cmds@{BOT_USERNAME}', f'commands@{BOT_USERNAME}'],prefixes=['.','/','!'],case_sensitive=False) & filters.text)
async def cmds(Client,message):
    try:
        await Client.send_chat_action(message.chat.id, "typing")
        await message.reply_text(f"<b>There are using commands\n\nAlt Balaji Checker - /alt  - reply txt combo</b>", parse_mode="html")
    except Exception as e:
        print(e)