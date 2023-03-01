#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import os
import time
import shutil,asyncio
# from PIL import Image
import json
import pyrogram
# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
  from Uploader.config import Config
else:
  from Uploader.config import Config
# from Uploader.utitles import make_thumb
from Uploader.utitles import *
from Uploader.script import Translation
from Uploader.functions.database import *
from Uploader.functions.progress2 import progress_for_pyrogram
from Uploader.functions.ran_text import random_char
# from hachoir.metadata import extractMetadata
# from hachoir.parser import createParser

# the_real_download_location = await bot.download_media(
#       message=update.reply_to_message,
#       file_name=download_location,
#       block=False,
#       progress=progress_for_pyrogram,
#       progress_args=("Downloading...\n", sent_message, c_time, bot, id,
#                      status))

async def download_media_async(
  update, download_location,sent_message, c_time,bot, uid,status):
    the_real_download_location = await bot.download_media(
      message=update.reply_to_message,
      file_name=download_location,
      block=False,
      progress=progress_for_pyrogram,
      progress_args=("Downloading...\n", sent_message, c_time, bot, uid,
                     status))
      

    return the_real_download_location




@pyrogram.Client.on_message(pyrogram.filters.command(["convert2video"]))
async def convert_to_video(bot, update):

  if update.reply_to_message:
    # print(update.reply_to_message)
    if not (update.reply_to_message.video or update.reply_to_message.document):
      return await update.reply_text(Translation.REPLY_TO_DOC_FOR_C2V)
    # 524288000 - 500MB
      
    media_msg = update.reply_to_message
    filesize = media_msg.video.file_size or media_msg.document.file_size
    file_name = media_msg.video.file_name or media_msg.document.file_name
    """
    
    result = is_today(update.chat.id)
    if result == False:
      addDATA(update.chat.id, "DATE", str(date.today()))
      addDATA(update.chat.id, "U_USAGE", 524288000)
      print("Data Updated")

    U_REMAIN = find_any(update.chat.id, "U_USAGE")
    print(U_REMAIN)

    if U_REMAIN < filesize:
      return await update.reply_text("Maximum MB Excuted")

    """

    sent_message = await update.reply_text(text="Processing...")
    nfh = random_char(5)
    download_location = Config.DOWNLOAD_LOCATION + "/" + f'{nfh}' + "/"
    status = Config.DOWNLOAD_LOCATION + f"/{nfh}-{str(update.chat.id)}-status.json"

    try:
      with open(status, 'w') as f:
        statusMsg = {'running': True, 'message': sent_message.id}
        json.dump(statusMsg, f, indent=2)

    except:
      pass

    c_time = time.time()
    task = asyncio.create_task(download_media_async(update, download_location,sent_message, c_time,bot,update.chat.id,status))
    the_real_download_location = await task

    
    # await message.download(file_name, block=False)
    """
    the_real_download_location = await bot.download_media(
      message=update.reply_to_message,
      file_name=download_location,
      block=False,
      progress=progress_for_pyrogram,
      progress_args=("Downloading...\n", sent_message, c_time, bot, id,
                     status))
                     """

    if the_real_download_location is not None:

      await sent_message.edit_text(text="Uploading...", )

      real_ph_path = Config.DOWNLOAD_LOCATION + "/" + {nfh } + str(
        update.from_user.id) + ".jpg"

      width, height, duration = await Mdata01(the_real_download_location)

      # thumb_id = find_any(update.chat.id, "PHOTO_THUMB")
      # if thumb_id:
      #   ph_path = await bot.download_media(thumb_id, real_ph_path)
      #   # ph_path = await make_thumb(thumb_image_path, width, height)

      # else:
      ph_path = None  #await make_thumb(thumb_image_path, width, height)

      # new = U_REMAIN - filesize
      # addDATA(update.chat.id, "U_USAGE", new)
      # try to upload file
      c_time = time.time()
      await bot.send_video(chat_id=update.chat.id,
                           video=the_real_download_location,
                           duration=duration,
                           caption=file_name,
                           width=width,
                           height=height,
                           supports_streaming=True,
                           thumb=ph_path,
                           reply_to_message_id=update.reply_to_message.id,
                           progress=progress_for_pyrogram,
                           progress_args=("Uploading...\n", sent_message,
                                          c_time, bot, id, status))

      try:
        os.remove(the_real_download_location)
        # os.remove(thumb_image_path)
        shutil.rmtree(download_location)

      except:
        pass

      await bot.edit_message_text(
        text="Translation.AFTER_SUCCESSFUL_UPLOAD_MSG",
        chat_id=update.chat.id,
        message_id=sent_message.id,
        disable_web_page_preview=True)

  else:
    await bot.send_message(chat_id=update.chat.id,
                           text=Translation.REPLY_TO_DOC_FOR_C2V,
                           reply_to_message_id=update.id)
