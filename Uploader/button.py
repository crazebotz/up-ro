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
import random
import shutil
import asyncio, json

from pyrogram.types import *
from datetime import datetime

from pyrogram.errors import MessageIdInvalid
from Uploader.utitles import *

if bool(os.environ.get("WEBHOOK")):
  from Uploader.config import Config
else:
  from sample_config import Config
from Uploader.script import Translation, u_downloads
from Uploader.functions.ran_text import random_char

from Uploader.functions.progress2 import progress_for_pyrogram as progress2, humanbytes
import pyrogram
from PIL import Image

video_formats = [
  "MP4", "MOV", "WMV", "AVI", "AVCHD", "FLV", "F4V", "SWF", "MKV"
]
audio_formats = ["MP3", "WAV", "AIFF", "FLAC", "AAC", "WMA", "OGG", "M4A"]


async def youtube_dl_call_back(bot, update, url_with_name, file_x):
  id = int(update.chat.id)
  random1 = random_char(5)
  ranom = random_char(5)
  save_ytdl_json_path = Config.DOWNLOAD_LOCATION + \
      "/" + str(update.from_user.id) + f'{ranom}' + ".json"
  try:
    with open(save_ytdl_json_path, "r", encoding="utf8") as f:
      response_json = json.load(f)
  except (FileNotFoundError) as e:
    # await update.delete()
    pass
    # return False
  youtube_dl_url = url_with_name  #update.message.reply_to_message.text
  custom_file_name = url_with_name.split("|")[1]

  # custom_file_name = str(response_json.get("title")) + \
  # "_" + file_x + "." + file_x
  cap_text = (custom_file_name)
  youtube_dl_username = None
  youtube_dl_password = None
  if "|" in youtube_dl_url:
    url_parts = youtube_dl_url.split("|")
    if len(url_parts) == 2:
      youtube_dl_url = url_parts[0]
      custom_file_name = url_parts[1]
    elif len(url_parts) == 4:
      youtube_dl_url = url_parts[0]
      custom_file_name = url_parts[1]
      youtube_dl_username = url_parts[2]
      youtube_dl_password = url_parts[3]
    else:
      for entity in update.message.reply_to_message.entities:
        if entity.type == "text_link":
          youtube_dl_url = entity.url
        elif entity.type == "url":
          o = entity.offset
          l = entity.length
          youtube_dl_url = youtube_dl_url[o:o + l]
    if youtube_dl_url is not None:
      youtube_dl_url = youtube_dl_url.strip()
    if custom_file_name is not None:
      custom_file_name = custom_file_name.strip()
    # https://stackoverflow.com/a/761825/4723940
    if youtube_dl_username is not None:
      youtube_dl_username = youtube_dl_username.strip()
    if youtube_dl_password is not None:
      youtube_dl_password = youtube_dl_password.strip()

  else:
    for entity in update.message.reply_to_message.entities:
      if entity.type == "text_link":
        youtube_dl_url = entity.url
      elif entity.type == "url":
        o = entity.offset
        l = entity.length
        youtube_dl_url = youtube_dl_url[o:o + l]
  sent_msg = await update.reply_text(
    text=Translation.DOWNLOAD_START.format(custom_file_name))
  description = Translation.CUSTOM_CAPTION_UL_FILE
  # if "fulltitle" in response_json:
  #   description = response_json["fulltitle"][:1021]
  # escape Markdown and special characters
  tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + \
      "/" + str(update.from_user.id) + f'{random1}'
  if not os.path.isdir(tmp_directory_for_each_user):
    os.makedirs(tmp_directory_for_each_user)
  download_directory = f"{tmp_directory_for_each_user}/{custom_file_name}.{file_x}"

  command_to_exec = []
  if file_x.upper() in audio_formats:
    command_to_exec = [
      "yt-dlp", "-c", "--max-filesize",
      str(Config.TG_MAX_FILE_SIZE), "--bidi-workaround", "--extract-audio",
      "--audio-format", 'mp3', "--audio-quality", '64k',
      youtube_dl_url, "-o", download_directory
    ]
  else:
    # command_to_exec = ["yt-dlp", "-f", youtube_dl_format, "--hls-prefer-ffmpeg", "--recode-video", "mp4", "-k", youtube_dl_url, "-o", download_directory]
    minus_f_format = file_x
    if "youtu" in youtube_dl_url:
      minus_f_format = f"{file_x}+bestaudio"
    command_to_exec = [
      "yt-dlp", "-c", "--max-filesize",
      str(Config.TG_MAX_FILE_SIZE), "--embed-subs", "-f", minus_f_format,
      "--bidi-workaround", youtube_dl_url, "-o", download_directory
    ]

  if Config.HTTP_PROXY != "":
    command_to_exec.append("--proxy")
    command_to_exec.append(Config.HTTP_PROXY)
  if youtube_dl_username is not None:
    command_to_exec.append("--username")
    command_to_exec.append(youtube_dl_username)
  if youtube_dl_password is not None:
    command_to_exec.append("--password")
    command_to_exec.append(youtube_dl_password)
  command_to_exec.append("--no-warnings")
  # command_to_exec.append("--quiet")

  start = datetime.now()
  process = await asyncio.create_subprocess_exec(
    *command_to_exec,
    # stdout must a pipe to be accessible as process.stdout
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE,
  )

  # Wait for the subprocess to finish
  stdout, stderr = await process.communicate()

  e_response = stderr.decode().strip()
  t_response = stdout.decode().strip()

  ad_string_to_replace = "please report this issue on https://github.com/kalanakt/All-Url-Uploader/issues"
  if e_response and ad_string_to_replace in e_response:
    error_message = e_response.replace(ad_string_to_replace, "")
    await update.message.edit_caption(text=error_message)
    return False

  if t_response:

    try:
      os.remove(save_ytdl_json_path)
    except FileNotFoundError as exc:
      pass

    end_one = datetime.now()
    time_taken_for_download = (end_one - start).seconds
    file_size = Config.TG_MAX_FILE_SIZE + 1
    try:
      file_size = os.stat(download_directory).st_size
    except FileNotFoundError as exc:
      download_directory = os.path.splitext(
        download_directory)[0] + "." + 'mp4'
      # https://stackoverflow.com/a/678242/4723940
      file_size = os.stat(download_directory).st_size

    download_location = f"{Config.DOWNLOAD_LOCATION}/{update.from_user.id}.jpg"
    thumb = download_location if os.path.isfile(download_location) else None

    if ((file_size > Config.TG_MAX_FILE_SIZE)):
      await update.message.edit_caption(
        caption=Translation.RCHD_TG_API_LIMIT.format(time_taken_for_download,
                                                     humanbytes(file_size)))
    else:
      sent_message = await sent_msg.edit_text(
        text=Translation.UPLOAD_START.format(custom_file_name))

      start_time = time.time()
      file_x = (download_directory.strip('"')).split(".")[-1]
      status = tmp_directory_for_each_user + f"/{str(id)}-status.json"

      try:
        with open(status, 'w') as f:
            statusMsg = {'running': True, 'message': sent_message.id}
            json.dump(statusMsg, f, indent=2)

      except Exception as ex:
          print(ex)
    
      if file_x.upper() in video_formats:
        width, height, duration = await Mdata01(download_directory)
        thumb_img = f"{Config.DOWNLOAD_LOCATION}/{update.from_user.id}.jpg"
        thumb_size = (width, height)
        try:
          img = Image.new('RGB', thumb_size, (85, 85, 85))
          img.save('thumb_img.jpg')
        except ValueError:
          img = Image.new('RGB', (1280, 1280), (85, 85, 85))
          img.save('thumb_img.jpg')

        # DOWNLOAD_LOCATION = Config.DOWNLOAD_LOCATION

        

        await update.reply_video(
          # chat_id=update.message.chat.id,
          video=download_directory,
          caption=cap_text,
          duration=duration,
          width=width,
          height=height,
          supports_streaming=True,
          progress=progress2,
          progress_args=(Translation.UPLOAD_START.format(custom_file_name),
                         sent_msg, start_time, bot, id,status))

      elif file_x.upper() in audio_formats:
        duration = await Mdata03(download_directory)
        await update.reply_audio(
          # chat_id=update.message.chat.id,
          audio=download_directory,
          caption=description,
          duration=duration,
          thumb=None,
          # reply_to_message_id=update.id,
          progress=progress2,
          progress_args=(Translation.UPLOAD_START.format(custom_file_name),
                         sent_msg, start_time, bot, id,status))

      elif file_x.upper() in "vm":
        width, duration = await Mdata02(download_directory)
        await update.reply_video_note(
          # chat_id=update.message.chat.id,
          video_note=download_directory,
          duration=duration,
          length=width,
          thumb=thumb,
          # reply_to_message_id=update.id,
          progress=progress2,
          progress_args=(Translation.UPLOAD_START.format(custom_file_name),
                         sent_msg, start_time, bot, id,status))

      else:
        await update.reply_document(
          # chat_id=update.message.chat.id,
          document=download_directory,
          caption=description,
          # parse_mode=enums.ParseMode.HTML,
          # reply_to_message_id=update.id,
          thumb=thumb,
          progress=progress2,
          progress_args=(Translation.UPLOAD_START.format(custom_file_name),
                         sent_msg, start_time, bot, id,status))

      end_two = datetime.now()
      time_taken_for_upload = (end_two - end_one).seconds
      try:
        shutil.rmtree(tmp_directory_for_each_user)
      except Exception:
        pass
      try:
        await sent_msg.edit_text(
          text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(
            time_taken_for_download, time_taken_for_upload))
      except MessageIdInvalid:
        pass

      print(f"Downloaded in: {str(time_taken_for_download)}")
      print(f"Uploaded in: {str(time_taken_for_upload)}")
