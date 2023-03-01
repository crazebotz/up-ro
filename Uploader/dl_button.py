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
import json
import time
import aiohttp
import asyncio
import math
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Uploader.functions.display_progress import humanbytes, TimeFormatter
from Uploader.functions.progress2 import progress_for_pyrogram as progress2
from Uploader.utitles import *
from Uploader.script import Translation
if bool(os.environ.get("WEBHOOK")):
  from Uploader.config import Config
else:
  from sample_config import Config

from Uploader.config import TASKS

video_formats = [
  "MP4", "MOV", "WMV", "AVI", "AVCHD", "FLV", "F4V", "SWF", "MKV"
]
audio_formats = ["MP3", "WAV", "AIFF", "FLAC", "AAC", "WMA", "OGG", "M4A"]



# sourcery skip: low-code-quality
async def ddl_call_back(bot, update, url_with_name, file_x):
  id = update.chat.id
  TASKS[id]=1
  
  youtube_dl_ext = file_x
  youtube_dl_url = url_with_name.split("|")[0]

  custom_file_name = url_with_name.split("|")[-1]

  description = custom_file_name
  if f".{youtube_dl_ext}" not in custom_file_name:
    custom_file_name += f'.{youtube_dl_ext}'

  start = datetime.now()
  sent_message = await update.reply_text(
    text=Translation.DOWNLOAD_START.format(custom_file_name))

  tmp_directory_for_each_user = f"{Config.DOWNLOAD_LOCATION}/{str(update.from_user.id)}"

  if not os.path.isdir(tmp_directory_for_each_user):
    os.makedirs(tmp_directory_for_each_user)
  download_directory = f"{tmp_directory_for_each_user}/{custom_file_name}"
  status = tmp_directory_for_each_user + f"/{str(id)}-status.json"

  try:
      with open(status, 'w') as f:
        statusMsg = {'running': True, 'message': sent_message.id}
        json.dump(statusMsg, f, indent=2)

  except:
      pass
  async with aiohttp.ClientSession() as session:
    c_time = time.time()
    try:
      await download_coroutine(bot, session, youtube_dl_url,
                               download_directory, update.chat.id,
                               sent_message.id, c_time,status)

    except asyncio.TimeoutError:
      await sent_message.edit_text(text=Translation.SLOW_URL_DECED)
      return False

  if os.path.exists(download_directory):
    save_ytdl_json_path = f"{Config.DOWNLOAD_LOCATION}/{str(update.chat.id)}.json"
    download_location = f"{Config.DOWNLOAD_LOCATION}/{update.from_user.id}.jpg"
    thumb = download_location if os.path.isfile(download_location) else None

    if os.path.exists(save_ytdl_json_path):
      os.remove(save_ytdl_json_path)
    end_one = datetime.now()
    try:
      await sent_message.edit_text(
      text=Translation.UPLOAD_START.format(custom_file_name))
    except:
      pass

    file_size = Config.TG_MAX_FILE_SIZE + 1
    try:
      file_size = os.stat(download_directory).st_size
    except FileNotFoundError:
      download_directory = f"{os.path.splitext(download_directory)[0]}.mkv"
      file_size = os.stat(download_directory).st_size

    

    if file_size > Config.TG_MAX_FILE_SIZE:
      await sent_message.edit_text(text=Translation.RCHD_TG_API_LIMIT)

    else:
      start_time = time.time()
      if file_x.upper() in video_formats:
        width, height, duration = await Mdata01(download_directory)
        await bot.send_video(
          chat_id=update.chat.id,
          video=download_directory,
          thumb=thumb,
          caption=description,
          duration=duration,
          width=width,
          height=height,
          supports_streaming=True,
          progress=progress2,
          progress_args=(Translation.UPLOAD_START.format(custom_file_name),
                         sent_message, start_time, bot, id, status))

      elif file_x.upper() in audio_formats:
        duration = await Mdata03(download_directory)
        await bot.send_audio(
          chat_id=update.chat.id,
          audio=download_directory,
          thumb=thumb,
          caption=description,
          duration=duration,
          progress=progress2,
          progress_args=(Translation.UPLOAD_START.format(custom_file_name),
                         sent_message, start_time, bot, id, status))

      else:
        await bot.send_document(
          chat_id=update.chat.id,
          document=download_directory,
          thumb=thumb,
          caption=description,
          progress=progress2,
          progress_args=(Translation.UPLOAD_START.format(custom_file_name),
                         sent_message, start_time, bot, id, status))

      end_two = datetime.now()
      try:
        os.remove(download_directory)
      except Exception:
        pass
      time_taken_for_download = (end_one - start).seconds
      time_taken_for_upload = (end_two - end_one).seconds
      try:
        await sent_message.edit_text(
          text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(
            time_taken_for_download, time_taken_for_upload),
          disable_web_page_preview=True)
      except:
        pass

      print(f"Downloaded in: {str(time_taken_for_download)}")
      print(f"Uploaded in: {str(time_taken_for_upload)}")
      try:
        TASKS.pop(id)
      except:
        pass
  else:
    await sent_message.edit_text(
      text=Translation.NO_VOID_FORMAT_FOUND.format("Incorrect Link"),
      disable_web_page_preview=True)
    try:
        TASKS.pop(id)
    except:
        pass


async def download_coroutine(bot, session, url, file_name, chat_id, message_id,
                             start, status):
  downloaded = 0
  # display_message = ""
  cancel_button = InlineKeyboardButton("Cancel",
                                         callback_data=f"cancel_upload#{status}")

  reply_markup = InlineKeyboardMarkup([[cancel_button]])
  name = file_name.split("/")[-1]

  ud_type = f"**File Name:** {name}\n\n**Downloading...**\n"
  async with session.get(url, timeout=Config.PROCESS_MAX_TIMEOUT) as response:
    total_length = int(response.headers["Content-Length"])
    content_type = response.headers["Content-Type"]    #Content-Type
    if "text" in content_type or total_length < 500:
      print("Returned")
      return await response.release()
    with open(file_name, "wb") as f_handle:
      while True:
        chunk = await response.content.read(Config.CHUNK_SIZE)
        if not chunk:
          break
        f_handle.write(chunk)
        downloaded += Config.CHUNK_SIZE

        now = time.time()
        diff = now - start
        if round(diff % 5.0) == 0 or downloaded == total_length:
          if os.path.exists(status):
            with open(status, 'r+') as f:
              statusMsg = json.load(f)
              if not statusMsg["running"]:
                return await response.release()
                # bot.stop_transmission()
                print("STOPPED")
          percentage = downloaded * 100 / total_length
          speed = downloaded / diff
          # print(speed)
          elapsed_time = round(diff) * 1000
          time_to_completion = (round(
            (total_length - downloaded) / speed) * 1000)
          estimated_total_time = elapsed_time + time_to_completion
          progress = "[{0}{1}]\n**Progress :** {2}%\n".format(
      ''.join(["◾️" for i in range(math.floor(percentage / 10))]),  #7.6923
      ''.join(["◽️" for i in range(10 - math.floor(percentage / 10))]),
      round(percentage, 2))

          tmp = progress + "**Completed :** {0} of {1}\n**Speed :** {2}/s\n**ETA :** {3}\n".format(
      humanbytes(downloaded), humanbytes(total_length), humanbytes(speed), TimeFormatter(time_to_completion))

          
          text = "{}{}".format(ud_type,tmp)
          try:
               await bot.edit_message_text(chat_id,
                                          message_id,
                                          text=text,reply_markup = reply_markup)
          except Exception as e:
                print(184, str(e))
    return await response.release()
