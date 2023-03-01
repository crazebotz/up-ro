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
from Uploader.functions.database import *

video_formats = [
  "MP4", "MOV", "WMV", "AVI", "AVCHD", "FLV", "F4V", "SWF", "MKV"
]
audio_formats = ["MP3", "WAV", "AIFF", "FLAC", "AAC", "WMA", "OGG", "M4A"]



async def change_thumb_func(bot, update):

    tmp_directory_for_each_user = f"{Config.DOWNLOAD_LOCATION}/{str(update.from_user.id)}"
    
    if not os.path.isdir(tmp_directory_for_each_user):
      os.makedirs(tmp_directory_for_each_user)
    
    
    sent_message = await update.reply_text(text="Processing...")
    
    status = Config.DOWNLOAD_LOCATION + f"/{str(update.chat.id)}-status.json"
    MSG = update.reply_to_message
    
    if MSG.video:
      real_filename = MSG.video.file_name

    if MSG.audio:
      real_filename = MSG.audio.file_name

    if MSG.animation:
      real_filename = MSG.animation.file_name

    if MSG.document:
      real_filename = MSG.document.file_name


    extension = os.path.splitext(real_filename)[1]
    if extension == '':
      extension = '.zip'
      real_filename += '.zip'
    
    extension = extension.replace('.', '')


    download_location = f"{tmp_directory_for_each_user}/{real_filename}"
   
    description = real_filename
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
      progress=progress_for_pyrogram,
      progress_args=("Downloading...\n", sent_message, c_time, bot, id,
                     status))
    if the_real_download_location is not None:
      await bot.edit_message_text(text="Uploading file",
                                  chat_id=update.chat.id,
                                  message_id=sent_message.id)
      # logger.info(the_real_download_location)
      real_ph_path = Config.DOWNLOAD_LOCATION + "/" + str(
        update.from_user.id) + ".jpg"

      thumb_id = find_any(update.chat.id,"PHOTO_THUMB")
      if thumb_id:
        ph_path = await bot.download_media(thumb_id,real_ph_path)

      else:
        ph_path = None
          

      # STart Time of Uploading
      c_time = time.time()
      new_file_name = the_real_download_location
      file_name = real_filename

      if extension.upper() in video_formats:

        width, height, duration = await Mdata01(new_file_name)


        await bot.send_video(
          chat_id=update.chat.id,
          video=the_real_download_location,
          thumb=ph_path,
          caption=description,
          duration=duration,
          width=width,
          height=height,
          supports_streaming=True,
          progress=progress_for_pyrogram,
          progress_args=(Translation.UPLOAD_START.format(file_name),
                         sent_message, c_time, bot, id, status))

      elif extension.upper() in audio_formats:
        duration = await Mdata03(new_file_name)
        await bot.send_audio(
          chat_id=update.chat.id,
          audio=the_real_download_location,
          thumb=ph_path,
          caption=description,
          duration=duration,
          progress=progress_for_pyrogram,
          progress_args=(Translation.UPLOAD_START.format(file_name),
                         sent_message, c_time, bot, id, status))

      else:
        await bot.send_document(
          chat_id=update.chat.id,
          document=the_real_download_location,
          thumb=ph_path,
          caption=description,
          progress=progress_for_pyrogram,
          progress_args=(Translation.UPLOAD_START.format(file_name),
                         sent_message, c_time, bot, id, status))

      try:
        # os.remove(new_file_name)
        # os.remove(thumb_image_path)
        shutil.rmtree(download_location)
      except:
        pass
        
      await bot.edit_message_text(text="Uploaded file",
                                  chat_id=update.chat.id,
                                  message_id=sent_message.id,
                                  disable_web_page_preview=True)
