print("Bot RunninG")

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

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
u_downloads = {}



import asyncio
from datetime import datetime

async def check_time(date_str):
    current_time = datetime.now()
    timestamp_now = int(current_time.timestamp())

    date_time = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    timestamp_old = int(date_time.timestamp())

    difference_seconds = timestamp_now - timestamp_old
    six_hours_in_seconds = 6 * 60 * 60

    await asyncio.sleep(0.1)  # simulate some async work

    if difference_seconds <= six_hours_in_seconds:
        return True
    else:
        return False


class Translation(object):

  START_TEXT = """
Hi {} 

I am Powerful Url Uploader Bot
 
"""

  HELP_TEXT = """

# Send me the Google Drive | ytdl | direct links.

# Select the desired option.

# Then be relaxed your file will be uploaded soon..
 
"""

  # give credit to developer

  ABOUT_TEXT = """
<b>♻️ My Name</b> : Url Uploader Bot

<b>🌀 Channel</b> : <a href="https://t.me/TMWAD">@TMWAD</a>

<b>🌺 Heroku</b> : <a href="https://heroku.com/">Heroku</a>

<b>📑 Language :</b> <a href="https://www.python.org/">Python 3.10.5</a>

<b>🇵🇲 Framework :</b> <a href="https://docs.pyrogram.org/">Pyrogram 2.0.30</a>

<b>👲 Developer :</b> <a href="https://t.me/kinu6">@kinu6</a>

"""
  GET_DETAILS = """📤 How would you like to upload this link?

**Title:** `{}`
**Size:** `{}`"""

  PROGRESS = """
🔰 Speed : {3}/s\n\n
🌀 Done : {1}\n\n
🎥 Tᴏᴛᴀʟ sɪᴢᴇ  : {2}\n\n
⏳ Tɪᴍᴇ ʟᴇғᴛ : {4}\n\n
"""
  ID_TEXT = """
🆔 Your Telegram ID 𝐢𝐬 :- <code>{}</code>
"""

  INFO_TEXT = """

 🤹 First Name : <b>{}</b>

 🚴‍♂️ Second Name : <b>{}</b>

 🧑🏻‍🎓 Username : <b>@{}</b>

 🆔 Telegram Id : <code>{}</code>

 📇 Profile Link : <b>{}</b>

 📡 Dc : <b>{}</b>

 📑 Language : <b>{}</b>

 👲 Status : <b>{}</b>
"""

  START_BUTTONS = InlineKeyboardMarkup([[
    InlineKeyboardButton('❓ Help', callback_data='help'),
    InlineKeyboardButton('🦊 About', callback_data='about')
  ], [InlineKeyboardButton('📛 Close', callback_data='close')]])
  CANCEL_BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton('📛 Close', callback_data='cancel')]])
  HELP_BUTTONS = InlineKeyboardMarkup([[
    InlineKeyboardButton('🏠 Home', callback_data='home'),
    InlineKeyboardButton('🦊 About', callback_data='about')
  ], [InlineKeyboardButton('📛 Close', callback_data='close')]])

  # Call back for rename
  rename_btn = InlineKeyboardButton("✏️ Rename", callback_data="rename_file")
  c2f_btn = InlineKeyboardButton("📂 Convert to document", callback_data="conv_to_doc")
  c2v_btn = InlineKeyboardButton("🎞 Convert to video", callback_data="conv_to_vid")
  change_thumb_btn = InlineKeyboardButton("🏞 Change thumbnail", callback_data="change_thumb")
  BTN_FOR_VID = InlineKeyboardMarkup([[rename_btn],[c2f_btn],[change_thumb_btn]])
  BTN_FOR_DOC_VID = InlineKeyboardMarkup([[rename_btn],[c2v_btn],[change_thumb_btn]])
  
  BTN_FOR_OTHER = InlineKeyboardMarkup([[rename_btn],[change_thumb_btn]])

  DOC_TEXT = """**What you want to do with this file?**

**Name:** `{}`
**Size:** {} MB
**Data Center:** `{}`"""
 

  
  ABOUT_BUTTONS = InlineKeyboardMarkup([[
    InlineKeyboardButton('🏠 Home', callback_data='home'),
    InlineKeyboardButton('❓ Help', callback_data='help')
  ], [InlineKeyboardButton('📛 Close', callback_data='close')]])
  BUTTONS = InlineKeyboardMarkup(
    [[InlineKeyboardButton('📛 Close', callback_data='close')]])
  FORMAT_SELECTION = "Now Select the desired formats"
  SET_CUSTOM_USERNAME_PASSWORD = """"""
  DOWNLOAD_START = "Downloading... ⌛\n\n `{}`"
  UPLOAD_START = "File Name: `{}`\n\n**Uploading...**\n"
  RCHD_TG_API_LIMIT = "Downloaded in {} seconds.\nDetected File Size: {}\nSorry. But, I cannot upload files greater than 2GB due to Telegram API limitations."
  AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS = "**Dᴏᴡɴʟᴏᴀᴅᴇᴅ ɪɴ** {} sᴇᴄᴏɴᴅs.\n**Uᴘʟᴏᴀᴅᴇᴅ ɪɴ** {} sᴇᴄᴏɴᴅs\n\nTʜᴀɴᴋs Fᴏʀ Usɪɴɢ Mᴇ"
  FF_MPEG_DEL_ETED_CUSTOM_MEDIA = "✅ Media cleared succesfully."
  CUSTOM_CAPTION_UL_FILE = " "
  NO_VOID_FORMAT_FOUND = "ERROR... <code>{}</code>"
  SLOW_URL_DECED = "Gosh that seems to be a very slow URL. Since you were screwing my home, I am in no mood to download this file. Meanwhile, why don't you try this:==> fast URL so that I can upload to Telegram, without me slowing down for other users."
  REPLY_TO_DOC_FOR_REN = """**Reply to file which you want to rename in following format**

/rename new_filename

**Example:** `/rename my_file.zip`"""
  REPLY_TO_DOC_FOR_C2F = "Reply to file with /convert2file which you want to convert into file"
  REPLY_TO_DOC_FOR_C2V = "Reply to file with /convert2video which you want to convert into video"


