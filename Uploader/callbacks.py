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

import os,json

if bool(os.environ.get("WEBHOOK")):
  from Uploader.config import Config
else:
  from sample_config import Config

from Uploader.config import TASKS
from Uploader.functions.database import *
from Uploader.rename.conv2file import convert_to_file
from Uploader.rename.conv2vid import convert_to_video
from Uploader.rename.thum_cb import change_thumb_func
from Uploader.dl_button import ddl_call_back
# from Uploader.button import youtube_dl_call_back
from Uploader.fast_dl import fast_dl_url
from Uploader.script import Translation,check_time
from Uploader.bypasser import get_details,final_url
from pyrogram import Client,filters

from pyrogram.types import ForceReply
import logging

logging.basicConfig(
  level=logging.DEBUG,
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)





@Client.on_callback_query(filters.regex(r'^conv_to_doc$'))
async def conv_to_doc_cb(client, cb):
    await cb.message.delete()  
    await convert_to_file(client,cb.message)

@Client.on_callback_query(filters.regex(r'^conv_to_vid$'))
async def conv_to_vid_cb(client, cb):
    await cb.message.delete()  
    await convert_to_video(client,cb.message)
  

@Client.on_callback_query(filters.regex(r'^change_thumb$'))
async def change_thumb_cb(client, cb):
    THUMB = find_any(cb.from_user.id,"PHOTO_THUMB")
    if not THUMB:
      return await cb.answer("Please /set_thumbnail before using this function.")
    await cb.message.delete()  
    await change_thumb_func(client,cb.message)


# Handle the callback query for the "Cancel" button
@Client.on_callback_query(filters.regex(r'^cancel_upload$'))
async def handle_callback_query(client, callback_query):
        
          status = callback_query.data.split("#")[1]
          if os.path.isfile(status):
                with open(status, 'r+') as f:
                    statusMsg = json.load(f)
                    statusMsg['running'] = False
                    f.seek(0)
                    json.dump(statusMsg, f, indent=2)
                    if 'pid' in statusMsg.keys():
                        try:
                            os.kill(statusMsg["pid"], 9)

                        except Exception as ex:
                          print(63,ex)
                            
                        delete_downloads(status)
                    try:
                        await client.delete_messages(callback_query.message.chat.id, statusMsg["message"])
                        await callback_query.message.reply_text("Cancelled")
                    except:
                        pass

          else:
            pass
               

def delete_downloads(USER):
  os.system(f'rm -rf {USER}')


@Client.on_callback_query()
async def button(bot, update):
  if update.data == "home":
    await update.message.edit(
      text=Translation.START_TEXT.format(update.from_user.mention),
      reply_markup=Translation.START_BUTTONS,
      disable_web_page_preview=True
    )
  elif update.data == "help":
    await update.message.edit(
      text=Translation.HELP_TEXT,
      reply_markup=Translation.HELP_BUTTONS,
      disable_web_page_preview=True
    )
  elif update.data == "about":
    await update.message.edit(
      text=Translation.ABOUT_TEXT,
      reply_markup=Translation.ABOUT_BUTTONS,
      disable_web_page_preview=True
    )
  elif "close" in update.data:
    await update.message.delete(True)

  elif update.data == "rename_cb":
    res = await check_time(str(update.message.date)) 
    if res == False:
      return await update.answer("You are replying to too old message, Please send me that message again.", show_alert=True)

    
    id = update.from_user.id
    if id in TASKS:
      return await update.answer("Please don't send new task until the previous one has been completed.", show_alert=True)
    reply_msg = update.message.reply_to_message
    m_id = reply_msg.id
    url = reply_msg.text
    url = await final_url(url)
    file_name,file_size = await get_details(url)
    await update.message.delete()
    
    
    TEXT = '''**Title:** `{}`

Send new name for this file'''
    await update.message.reply_text(
      text=TEXT.format(file_name),
      reply_to_message_id = m_id,
      reply_markup=ForceReply(True,placeholder="Enter file name"),
      quote=True)


  elif update.data == "rename_file":
    res = await check_time(str(update.message.date)) 
    if res == False:
      return await update.answer("You are replying to too old message, Please send me that message again.", show_alert=True)
    
    id = update.from_user.id
    if id in TASKS:
      return await update.answer("Please don't send new task until the previous one has been completed.", show_alert=True)
    reply_msg = update.message.reply_to_message
    
    await update.message.delete()
    mediamsg = reply_msg.video or reply_msg.document or reply_msg.audio
    file_name = mediamsg.file_name
    real_file_size = mediamsg.file_size
    filesize = (real_file_size / (1024 * 1024))
    filesize = str(round(filesize, 2))
    
    
    TEXT = '''**Title:** `{}`

Send new name to rename this file'''
    await update.message.reply_text(
      text=TEXT.format(file_name),
      reply_to_message_id = reply_msg.id,
      reply_markup=ForceReply(True,placeholder="Enter file name"),
      quote=True)


  
  elif update.data == "default_cb":
    res = await check_time(str(update.message.date)) 
    if res == False:
      return await update.answer("You are replying to too old message, Please send me that url again.", show_alert=True)

    id = update.from_user.id
    # if id in TASKS:
    #   return await update.answer("Please don't send new task until the previous one has been completed.", show_alert=True)
    reply_msg = update.message.reply_to_message
    m_id = reply_msg.id
    url = reply_msg.text
    url = await final_url(url)
    file_name,file_size = await get_details(url)
    url_with_name = f"{url}|{file_name}"
    await update.message.delete()
    
    file_x = (file_name.strip('"')).split(".")[-1]
    await ddl_call_back(bot, reply_msg,url_with_name, file_x)


  elif "cancel" in update.data:
    await handle_callback_query(bot, update)

    
  elif "|" in update.data:
    print(131, 'called')
    await fast_dl_url(bot, update)
  elif "=" in update.data:
    await ddl_call_back(bot, update)
  

  else:
    await update.message.delete()
