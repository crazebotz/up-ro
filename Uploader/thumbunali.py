# MIT License

# Copyright (c) 2022 Hash Minner

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

import os
from telegraph import upload_file
from pyrogram import Client, filters

if bool(os.environ.get("WEBHOOK")):
    from Uploader.config import Config
else:
    from sample_config import Config
from Uploader.functions.database import *

@Client.on_message(filters.photo & filters.incoming & filters.private)
async def save_photo(bot, msg):
    # medianame = Config.DOWNLOAD_LOCATION + str(msg.from_user.id)
    # await msg.download(medianame)
 
    # response = upload_file(medianame)
    # photo = f"https://telegra.ph{response[0]}"
    addDATA(msg.chat.id,"PHOTO_THUMB",msg.photo.file_id)

  
    await msg.reply_text(
        text="Your custom thumbnail is saved",
        quote=True
    )


@Client.on_message(filters.command("thumb") & filters.incoming & filters.private)
async def send_photo(bot, msg):
    # download_location = f"{Config.DOWNLOAD_LOCATION}/{message.from_user.id}.jpg"
    THUMB = find_any(msg.chat.id,"PHOTO_THUMB")

    if THUMB:
        await msg.reply_photo(
            photo=THUMB,
            caption="👆 Custom thumbnail",
            quote=True
        )
    else:
        await msg.reply_text(text="you don't have set thumbnail yet!. send .jpg img to save as thumbnail.", quote=True)


@Client.on_message(filters.command("delthumb") & filters.incoming & filters.private)
async def delete_photo(bot, message):
    download_location = f"{Config.DOWNLOAD_LOCATION}/{message.from_user.id}.jpg"
    if os.path.isfile(download_location):
        os.remove(download_location)
        await message.reply_text(text="your thumbnail removed successfully.", quote=True)
    else:
        await message.reply_text(text="you don't have set thumbnail yet!. send .jpg img to save as thumbnail.", quote=True)
