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

import os, json

from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message
from Uploader.script import Translation,check_time
from Uploader.button import youtube_dl_call_back
from Uploader.dl_button import ddl_call_back
from Uploader.functions.database import *
from Uploader.bypasser import *

video_formats = [
  "MP4", "MOV", "WMV", "AVI", "AVCHD", "FLV", "F4V", "SWF", "MKV"
]
audio_formats = ["MP3", "WAV", "AIFF", "FLAC", "AAC", "WMA", "OGG", "M4A"]

if bool(os.environ.get("WEBHOOK")):
  from Uploader.config import Config
else:
  from sample_config import Config
from Uploader.config import TASKS,DONT_SEND_TASK
from Uploader.rename.renamefile import rename_cb


# @Client.on_message(filters.private)


# from datetime import datetime
@Client.on_message(
  filters.command("start") & filters.private, )
async def start_bot(_, m: Message):
  API = find_any(m.chat.id, '_id')
  if API:
    pass
  else:
    insert(m.chat.id,m.chat.first_name)
  return await m.reply_text(
    Translation.START_TEXT.format(m.from_user.mention),
    reply_markup=Translation.START_BUTTONS,
    disable_web_page_preview=True,
    quote=True,
  )


@Client.on_message(filters.command("help") & filters.private, )
async def help_bot(_, m: Message):
  return await m.reply_text(
    Translation.HELP_TEXT,
    reply_markup=Translation.HELP_BUTTONS,
    disable_web_page_preview=True,
  )

@Client.on_message(filters.media & filters.private & ~filters.photo & ~filters.video)
async def file_to_vid_qry(_, m: Message):
  media_msg = m.video or m.audio or m.document or m.animation
  # print(media_msg)
  real_filename = media_msg.file_name
  
  filesize = media_msg.file_size
  filesize = (filesize / (1024 * 1024))
  filesize = str(round(filesize, 2))
  
  extension = os.path.splitext(real_filename)[1]
  if extension == '':
      real_filename += '.zip'
  extension = extension.replace('.', '')

  if extension.upper() not in video_formats:
    return await m.reply_text(
    Translation.DOC_TEXT.format(real_filename,filesize,m.from_user.dc_id),
    reply_markup=Translation.BTN_FOR_OTHER,
    disable_web_page_preview=True,
    quote=True
  )
  
  return await m.reply_text(
    Translation.DOC_TEXT.format(m.document.file_name,filesize,m.from_user.dc_id),
    reply_markup=Translation.BTN_FOR_DOC_VID,
    disable_web_page_preview=True,
    quote=True
  )

@Client.on_message(filters.video & filters.private, )
async def vid_to_file_qry(_, m: Message):
  # print(m)
  filesize = m.video.file_size
  filesize = (filesize / (1024 * 1024))
  filesize = str(round(filesize, 2))
  return await m.reply_text(
    Translation.DOC_TEXT.format(m.video.file_name,filesize,m.from_user.dc_id),
    reply_markup=Translation.BTN_FOR_VID,
    disable_web_page_preview=True,
    quote=True
  )


@Client.on_message(
  filters.command("about") & filters.private, )
async def aboutme(_, m: Message):
  return await m.reply_text(
    Translation.ABOUT_TEXT,
    reply_markup=Translation.ABOUT_BUTTONS,
    disable_web_page_preview=True,
  )


# @Client.on_message(filters.private & filters.reply)
async def reply_echo(bot, update):
  print('Reply Echod')
  reply_msg = update.reply_to_message
  print(reply_msg.date)
  res = await check_time(str(reply_msg.date))
  
  if res == False:
    return 
  if not reply_msg:
    return
  if not reply_msg.text:
    return
    
  m_id = reply_msg.reply_to_message_id
  
  if "Send new name for this file" not in reply_msg.text:
    print(97)
    return
  details = await bot.get_messages(update.chat.id, m_id)
  url = details.text
  name = update.text

  url = await final_url(url)
  url_with_name = f"{url}|{name}"
  file_name, file_size = await get_details(url)
  file_x = (file_name.strip('"')).split(".")[-1]
  await youtube_dl_call_back(bot, reply_msg,url_with_name, file_x)



@Client.on_message(filters.private & filters.reply & ~filters.command(['rename']))
async def reply_2(bot, update):
  reply_msg = update.reply_to_message  
  if not reply_msg:
    return
  res = await check_time(str(reply_msg.date))
  if res == False:
    return
  if not reply_msg.text:
    print(reply_msg)
    return
  
  m_id = reply_msg.reply_to_message_id
  id = update.from_user.id
  if id in TASKS:
      return await update.reply_text(DONT_SEND_TASK)
  
  if "Send new name for this file" in reply_msg.text:
    pass
  elif "Send new name to rename this file" in reply_msg.text:
    pass 

  else:
    return
  details = await bot.get_messages(update.chat.id, m_id)
  name = update.text
  if not details.text:
    return await rename_cb(bot,details,name)
    
  url = details.text
  try:
    url = await final_url(url)
    url_with_name = f"{url}|{name}"
    file_name, file_size = await get_details(url)
    file_x = (file_name.strip('"')).split(".")[-1]

  except BaseException as ex:
    return await update.reply_text(str(ex))
    
  await ddl_call_back(bot, reply_msg,url_with_name, file_x)
