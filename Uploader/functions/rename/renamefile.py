#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K


# the secret configuration specific things
import os,shutil
if bool(os.environ.get("WEBHOOK", False)):
  from Uploader.config import Config
else:
  from Uploader.config import Config

import pyrogram

import time
import json
from Uploader.utitles import *
from Uploader.script import Translation
from Uploader.functions.ran_text import random_char
from Uploader.functions.progress2 import progress_for_pyrogram
from Uploader.functions import database

video_formats = [
  "MP4", "MOV", "WMV", "AVI", "AVCHD", "FLV", "F4V", "SWF", "MKV"
]
audio_formats = ["MP3", "WAV", "AIFF", "FLAC", "AAC", "WMA", "OGG", "M4A"]


@pyrogram.Client.on_message(pyrogram.filters.command(["rename"]))
async def rename_doc(bot, update):

  if (" " in update.text) and (update.reply_to_message is not None):

    cmd, file_name = update.text.split(" ", 1)
    rendem = random_char(5)
    
    tmp_directory_for_each_user = f"{Config.DOWNLOAD_LOCATION}/{rendem}-{str(update.from_user.id)}"

    if not os.path.isdir(tmp_directory_for_each_user):
      os.makedirs(tmp_directory_for_each_user)
    
    
    sent_message = await update.reply_text(text="Processing...")
    status = f"{Config.DOWNLOAD_LOCATION}/{rendem}-{str(update.from_user.id)}-status.json"
    
    
    MSG = update.reply_to_message
    media_msg = MSG.video or MSG.document or MSG.audio or MSG.animation
    real_filename = media_msg.file_name
    print(50,real_filename)
    

    extension = os.path.splitext(real_filename)[1]
    if extension == '':
      extension = '.zip'
      file_name += '.zip'

    else:
      pass #file_name+=extension

    print(61,file_name)

      
    extension = extension.replace('.', '')
    download_location = f"{tmp_directory_for_each_user}/{file_name}"
    print(download_location)

    description = file_name
    try:
      with open(status, 'w') as f:
        statusMsg = {'running': True, 'message': sent_message.id}
        json.dump(statusMsg, f, indent=2)

    except:
      pass
    c_time = time.time()
    
    download_location = await bot.download_media(
      message=update.reply_to_message,
      file_name=download_location,
      progress=progress_for_pyrogram,
      progress_args=("Downloading...\n", sent_message, c_time, bot, id,
                     status))
    print(download_location)
    # return
    if download_location is not None:
      
      # new_file_name = download_location + file_name
      # os.rename(the_real_download_location, new_file_name)
      await bot.edit_message_text(text="Uploading file",
                                  chat_id=update.chat.id,
                                  message_id=sent_message.id)
      # logger.info(the_real_download_location)
      thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(
        update.from_user.id) + ".jpg"

      # STart Time of Uploading
      c_time = time.time()

      if extension.upper() in video_formats:

        width, height, duration = await Mdata01(download_location)
        if not os.path.exists(thumb_image_path):
          thumb_image_path = await make_thumb(thumb_image_path, width, height)

        await bot.send_video(
          chat_id=update.chat.id,
          video=download_location,
          thumb=thumb_image_path,
          caption=description,
          duration=duration,
          width=width,
          height=height,
          supports_streaming=True,
          progress=progress_for_pyrogram,
          progress_args=(Translation.UPLOAD_START.format(file_name),
                         sent_message, c_time, bot, id, status))

      elif extension.upper() in audio_formats:
        if not os.path.exists(thumb_image_path):
          thumb_image_path = None
        duration = await Mdata03(download_location)
        await bot.send_audio(
          chat_id=update.chat.id,
          audio=download_location,
          thumb=thumb_image_path,
          caption=description,
          duration=duration,
          progress=progress_for_pyrogram,
          progress_args=(Translation.UPLOAD_START.format(file_name),
                         sent_message, c_time, bot, id, status))

      else:
        if not os.path.exists(thumb_image_path):
          thumb_image_path = None
        await bot.send_document(
          chat_id=update.chat.id,
          document=download_location,
          thumb=thumb_image_path,
          caption=description,
          progress=progress_for_pyrogram,
          progress_args=(Translation.UPLOAD_START.format(file_name),
                         sent_message, c_time, bot, id, status))

      try:
        # os.remove(download_location)
        # os.remove(thumb_image_path)
        shutil.rmtree(download_location)
      except:
        pass
        
      await bot.edit_message_text(text="Uploaded file",
                                  chat_id=update.chat.id,
                                  message_id=sent_message.id,
                                  disable_web_page_preview=True)
  else:
    await bot.send_message(chat_id=update.chat.id,
                           text=Translation.REPLY_TO_DOC_FOR_REN,
                           reply_to_message_id=update.id)




async def rename_cb(bot, msg,file_name):
  
  if 5==5:

    description = file_name
    rendem = random_char(5)
    download_location = Config.DOWNLOAD_LOCATION + \
      "/" + str(msg.from_user.id) + rendem

    tmp_directory_for_each_user = f"{Config.DOWNLOAD_LOCATION}/{str(msg.from_user.id)}"

    if not os.path.isdir(tmp_directory_for_each_user):
      os.makedirs(tmp_directory_for_each_user)
    download_location = f"{tmp_directory_for_each_user}/{file_name}"
    
    sent_message = await msg.reply_text(text="Processing...")
    
    status = Config.DOWNLOAD_LOCATION + f"/{str(msg.chat.id)}-status.json"
    MSG = msg
    
    media_msg = MSG.video or MSG.audio or MSG.document or MSG.animation
    real_filename = media_msg.file_name

    extension = os.path.splitext(real_filename)[1]
    if extension == '':
      file_name += '.zip'
    extension = extension.replace('.', '')

  
    try:
      with open(status, 'w') as f:
        statusMsg = {'running': True, 'message': sent_message.id}
        json.dump(statusMsg, f, indent=2)

    except:
      pass
    c_time = time.time()
    the_real_download_location = await bot.download_media(
      message=msg,
      file_name=download_location,
      progress=progress_for_pyrogram,
      progress_args=("Downloading...\n", sent_message, c_time, bot, id,
                     status))
    if the_real_download_location is not None:
      new_file_name = download_location + file_name
      os.rename(the_real_download_location, new_file_name)

      
      await bot.edit_message_text(text="Uploading file",
                                  chat_id=msg.chat.id,
                                  message_id=sent_message.id)
      # logger.info(the_real_download_location)
      thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(
        msg.from_user.id) + ".jpg"

      # STart Time of Uploading
      c_time = time.time()

      if extension.upper() in video_formats:

        width, height, duration = await Mdata01(new_file_name)
        if not os.path.exists(thumb_image_path):
          thumb_image_path = await make_thumb(thumb_image_path, width, height)

        await bot.send_video(
          chat_id=msg.chat.id,
          video=new_file_name,
          thumb=thumb_image_path,
          caption=description,
          duration=duration,
          width=width,
          height=height,
          supports_streaming=True,
          progress=progress_for_pyrogram,
          progress_args=(Translation.UPLOAD_START.format(file_name),
                         sent_message, c_time, bot, id, status))

      elif extension.upper() in audio_formats:
        if not os.path.exists(thumb_image_path):
          thumb_image_path = None
        duration = await Mdata03(new_file_name)
        await bot.send_audio(
          chat_id=msg.chat.id,
          audio=new_file_name,
          thumb=thumb_image_path,
          caption=description,
          duration=duration,
          progress=progress_for_pyrogram,
          progress_args=(Translation.UPLOAD_START.format(file_name),
                         sent_message, c_time, bot, id, status))

      else:
        if not os.path.exists(thumb_image_path):
          thumb_image_path = None
        await bot.send_document(
          chat_id=msg.chat.id,
          document=new_file_name,
          thumb=thumb_image_path,
          caption=description,
          progress=progress_for_pyrogram,
          progress_args=(Translation.UPLOAD_START.format(file_name),
                         sent_message, c_time, bot, id, status))

      try:
        os.remove(new_file_name)
        # os.remove(thumb_image_path)
        shutil.rmtree(download_location)
      except:
        pass
        
      await bot.edit_message_text(text="Uploaded file",
                                  chat_id=msg.chat.id,
                                  message_id=sent_message.id,
                                  disable_web_page_preview=True)
  else:
    await bot.send_message(chat_id=msg.chat.id,
                           text=Translation.REPLY_TO_DOC_FOR_REN,
                           reply_to_message_id=msg.id)
