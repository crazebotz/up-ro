#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import os
import time
import shutil
import asyncio
from Uploader.utitles import make_thumb

import json
# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
  from Uploader.config import Config
else:
  from Uploader.config import Config

import pyrogram
from Uploader.functions.ran_text import random_char
from Uploader.functions.progress2 import progress_for_pyrogram
from Uploader.script import Translation

@pyrogram.Client.on_message(pyrogram.filters.command(["convert2file"]))
async def convert_to_file(bot, update):
  

  if update.reply_to_message:
    # print(update.reply_to_message)
    nfh = random_char(5)
    download_location = Config.DOWNLOAD_LOCATION + "/" + f'{nfh}' + "/"
    status = Config.DOWNLOAD_LOCATION + f"/{str(update.chat.id)}-status.json"
    sent_message = await update.reply_text(text="Processing...")

    try:
      with open(status, 'w') as f:
        statusMsg = {'running': True, 'message': sent_message.id}
        json.dump(statusMsg, f, indent=2)

    except:
      pass

    c_time = time.time()
    the_real_download_location = await bot.download_media(
      message=update.reply_to_message,
      file_name=download_location,
      block = False,
      progress=progress_for_pyrogram,
      progress_args=("Downloading\n\n", sent_message, c_time, bot, id,
                     status))

    if the_real_download_location is not None:

      await sent_message.edit_text(text="Uploading...", )

      width = 90
      height = 90
      thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"

      if not os.path.exists(thumb_image_path):
        thumb_image_path = await make_thumb(thumb_image_path, width, height)

      await asyncio.sleep(1)
      # try to upload file
      c_time = time.time()
      await bot.send_document(
        chat_id=update.chat.id,
        document=the_real_download_location,
        caption='Document',
        block=False,
        thumb=thumb_image_path,
        reply_to_message_id=update.reply_to_message.id,
        progress=progress_for_pyrogram,
        progress_args=("Uploading...\n", sent_message, c_time, bot, id,
                       status))
      
      # removing all temp files from storage
      try:
        os.remove(the_real_download_location)
        os.remove(thumb_image_path)
        shutil.rmtree(download_location)
      except:
        pass

      # end_two = time.time()
      # time_taken_for_upload = (end_two - end_one).seconds
        
      await bot.edit_message_text(
        text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS,
        chat_id=update.chat.id,
        message_id=sent_message.id,
        disable_web_page_preview=True)
      
  else:
    await bot.send_message(chat_id=update.chat.id,
                           text=Translation.REPLY_TO_DOC_FOR_C2F,
                           reply_to_message_id=update.id)
