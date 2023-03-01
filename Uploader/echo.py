# MIT License

# Copyright (c) 2023 Rahul Thakor
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
# import time
# import json
import asyncio
# import logging

from opencc import OpenCC

# from pyrogram.types import Thumbnail
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

if bool(os.environ.get("WEBHOOK")):
  from Uploader.config import Config
else:
  from sample_config import Config
from Uploader.script import Translation

# from Uploader.functions.ran_text import random_char
# from Uploader.functions.display_progress import humanbytes
from Uploader.bypasser import *

s2tw = OpenCC('s2tw.json').convert











@Client.on_message(filters.regex(pattern="http.*") & filters.private)
async def link_echo(bot, update):

  sentmsg = await update.reply_text("Processing...⏳", quote=True)
  
  if "youtu.be" in update.text:
    return await sentmsg.edit_text("**No Youtube Links Supported**")
  
  link = update.text 
  url = await final_url(link)
  await asyncio.sleep(1)
  
  
  file_name, file_size = await get_details(url)
  file_size1 = file_size
  
  file_size = file_size.replace(' MB', '')
  file_size = round(float(file_size))
  if file_size < 1:
    return await sentmsg.edit_text(
        "This link is not accessible or not direct download link",
        disable_web_page_preview=True)
 
    
  DOWN_BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton('📄 Default', callback_data=f'default_cb'),
    InlineKeyboardButton('✏️ Rename', callback_data='rename_cb')
  ]])

  return await sentmsg.edit_text(Translation.GET_DETAILS.format(file_name, file_size1),reply_markup=DOWN_BUTTONS,disable_web_page_preview=True)

  # except BaseException as ex:
  #   await sentmsg.edit_text("This link is not accessible or not direct download link")
