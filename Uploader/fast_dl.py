import os
import json
import time
import shutil
import asyncio
import logging
from pyrogram.types import *
from datetime import datetime
from Uploader.bypasser import *
from Uploader.functions.progress2 import progress_for_pyrogram as progress2, humanbytes
from Uploader.utitles import *

from Uploader.script import Translation
from Uploader.functions.ran_text import random_char
from Uploader.functions.display_progress import progress_for_pyrogram
from pyrogram.errors import MessageIdInvalid


if bool(os.environ.get("WEBHOOK")):
  from Uploader.config import Config
else:
  from sample_config import Config
  


video_formats = [
  "MP4", "MOV", "WMV", "AVI", "AVCHD", "FLV", "F4V", "SWF", "MKV"
]
audio_formats = ["MP3", "WAV", "AIFF", "FLAC", "AAC", "WMA", "OGG", "M4A"]

file_extensions = ['PY', 'TXT', 'CSV', 'JSON', 'XML', 'HTML', 'PDF', 'JPG', 'JPEG', 'PNG', 'GIF', 'WAV', 'MP3', 'MP4', 'ZIP', 'TAR.GZ', 'TGZ', 'TAR.BZ2', 'TBZ2']

file_extensions.extend(video_formats)
file_extensions.extend(audio_formats)



logging.basicConfig(
  level=logging.DEBUG,
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

logging.basicConfig(
  level=logging.DEBUG,
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def fast_dl_url(bot, update):
  id = int(update.from_user.id)
  cb_data = update.data
  print(cb_data)
  # youtube_dl extractors
  tg_send_type, youtube_dl_format, youtube_dl_ext, ranom = cb_data.split("|")

  msg_len = update.message.reply_to_message.text.split()
  # file_ext = update.message.reply_to_message.text.split(".")[-1]
  print(youtube_dl_ext)
  
  if youtube_dl_ext.upper() not in file_extensions:
    print("No valid File")
    return
  
  if len(msg_len) < 2:
    
    return

  if len(msg_len) == 2:
    url = update.message.reply_to_message.text.split()[1]
    

  else:
    url = update.message.reply_to_message.text[6:]
    
  # url = update.message.reply_to_message.text.split()[1]
  random1 = random_char(5)
  
  youtube_dl_url = url # update.message.reply_to_message.text
  
  url = await final_url(url)
  file_name = update.message.reply_to_message.text.split("|")
  if len(file_name) > 1:
    file_name = update.message.reply_to_message.text.split("|")[-1]
  else:
    file_name, file_size = await get_details(url)
                                          
  custom_file_name = file_name + '.' + youtube_dl_ext #str(response_json.get("title")) + "." + youtube_dl_ext
  print(67,custom_file_name)
  youtube_dl_username = None
  youtube_dl_password = None
  if "|" in youtube_dl_url:
    url_parts = youtube_dl_url.split("|")
    if len(url_parts) == 2:
      youtube_dl_url = url_parts[0]
      custom_file_name = url_parts[1]
      print(95,custom_file_name)
      
    elif len(url_parts) == 4:
      youtube_dl_url = url_parts[0]
      custom_file_name = url_parts[1]
      print(100,custom_file_name)
      
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
      print(116,custom_file_name)
      
    # https://stackoverflow.com/a/761825/4723940
    if youtube_dl_username is not None:
      youtube_dl_username = youtube_dl_username.strip()
    if youtube_dl_password is not None:
      youtube_dl_password = youtube_dl_password.strip()
    # logger.info(youtube_dl_url)
    # logger.info(custom_file_name)
  else:
    for entity in update.message.reply_to_message.entities:
      if entity.type == "text_link":
        youtube_dl_url = entity.url
      elif entity.type == "url":
        o = entity.offset
        l = entity.length
        youtube_dl_url = youtube_dl_url[o:o + l]
  start_dl = await update.message.edit_caption(
    caption=Translation.DOWNLOAD_START.format(custom_file_name))
  # print("download started")
  description = Translation.CUSTOM_CAPTION_UL_FILE
  # if "fulltitle" in response_json:
  description = custom_file_name # response_json["fulltitle"][:1021]
    # escape Markdown and special characters
  tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + \
      "/" + str(update.from_user.id) + f'{random1}'
  if not os.path.isdir(tmp_directory_for_each_user):
    os.makedirs(tmp_directory_for_each_user)
  download_directory = f"{tmp_directory_for_each_user}/{custom_file_name}"
  print(145,download_directory)
  

  command_to_exec = []
  print(youtube_dl_ext,youtube_dl_format)
  if tg_send_type == "audio":
    print(151)
    command_to_exec = [
      "yt-dlp", "-c", "--max-filesize",
      str(Config.TG_MAX_FILE_SIZE), "--bidi-workaround", "--extract-audio",
      "--audio-format", youtube_dl_ext, "--audio-quality", youtube_dl_format,
      youtube_dl_url, "-o", download_directory
    ]
  else:
    # command_to_exec = ["yt-dlp", "-f", youtube_dl_format, "--hls-prefer-ffmpeg", "--recode-video", "mp4", "-k", youtube_dl_url, "-o", download_directory]
    minus_f_format = youtube_dl_format
    if "youtu" in youtube_dl_url:
      minus_f_format = f"{youtube_dl_format}+bestaudio"
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
  # logger.info(command_to_exec)
  start = datetime.now()
  # print(start)
  """
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
  """
  process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
  try:
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout = 880)
        e_response = stderr.decode().strip()
        t_response = stdout.decode().strip()
        
  except asyncio.TimeoutError:
        
        process.kill()
        await process.wait()
        await start_dl.edit_text("Too Slow Link Failed to Download")
        return
    
  # logger.info(e_response)
  # logger.info(t_response)
  ad_string_to_replace = "please report this issue on https://github.com/kalanakt/All-Url-Uploader/issues"
  if e_response and ad_string_to_replace in e_response:
    error_message = e_response.replace(ad_string_to_replace, "")
    await update.message.edit_caption(text=error_message)
    return False

  if t_response:
    
    end_one = datetime.now()
    time_taken_for_download = (end_one - start).seconds
    file_size = Config.TG_MAX_FILE_SIZE + 1
    """
    try:
      file_size = os.stat(download_directory).st_size
    except FileNotFoundError as exc:
      download_directory = os.path.splitext(
        download_directory)[0] + "." + "mp4"
      # https://stackoverflow.com/a/678242/4723940
      file_size = os.stat(download_directory).st_size
    """
    url = await final_url(url)
  
    file_name, file_size = await get_details(url)
    file_size = file_size.replace(' MB','')
    file_size = round(float(file_size))
    

    download_location = f"{Config.DOWNLOAD_LOCATION}/{update.from_user.id}.jpg"
    thumb = download_location if os.path.isfile(download_location) else None

    status = tmp_directory_for_each_user + f"/{str(id)}-status.json"


    if ((file_size > Config.TG_MAX_FILE_SIZE)):
      await update.message.edit_caption(
        caption=Translation.RCHD_TG_API_LIMIT.format(time_taken_for_download,
                                                     humanbytes(file_size)))
      
    else:
      sent_msg = await update.message.edit_caption(
        caption=Translation.UPLOAD_START.format(custom_file_name))
      try:
        with open(status, 'w') as f:
          statusMsg = {'running': True, 'message': sent_msg.id}
          json.dump(statusMsg, f, indent=2)
      except Exception as ex:
          print(ex)
      start_time = time.time()
      print(267,custom_file_name)
      print(youtube_dl_ext)
      if tg_send_type == "video":
        print("VIDEO")
        width, height, duration = await Mdata01(download_directory)
        await update.message.reply_video(
          # chat_id=update.message.chat.id,
          video=download_directory,
          caption=description,
          duration=duration,
          width=width,
          height=height,
          supports_streaming=True,
          thumb=thumb,
          # reply_to_message_id=update.id,
          progress=progress2,
          progress_args=(Translation.UPLOAD_START.format(custom_file_name),
                         sent_msg, start_time, bot, id,status))
      elif tg_send_type == "audio":
        print("AUDIO")
        # new = download_directory.replace('mp4','mp3')
        # os.rename(download_directory, new)
        duration = await Mdata03(download_directory)
        await update.message.reply_audio(
          # chat_id=update.message.chat.id,
          audio=download_directory,
          caption=description,
          duration=duration,
          thumb=thumb,
          # reply_to_message_id=update.id,
          progress=progress2,
          progress_args=(Translation.UPLOAD_START.format(custom_file_name),
                         sent_msg, start_time, bot, id,status))
      elif tg_send_type == "vm":
        width, duration = await Mdata02(download_directory)
        await update.message.reply_video_note(
          # chat_id=update.message.chat.id,
          video_note=download_directory,
          duration=duration,
          length=width,
          thumb=thumb,
          # reply_to_message_id=update.id,
          progress=progress_for_pyrogram,
          progress_args=(Translation.UPLOAD_START, update.message, start_time))
      else:
        await update.message.reply_document(
          # chat_id=update.message.chat.id,
          document=download_directory,
          caption=description,
          # parse_mode=enums.ParseMode.HTML,
          # reply_to_message_id=update.id,
          thumb=thumb,
          progress=progress_for_pyrogram,
          progress_args=(Translation.UPLOAD_START, update.message, start_time))

      end_two = datetime.now()
      time_taken_for_upload = (end_two - end_one).seconds
      try:
        shutil.rmtree(tmp_directory_for_each_user)
      except Exception:
        pass
      try:
        await update.message.edit_caption(caption=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG_WITH_TS.format(time_taken_for_download, time_taken_for_upload))
      except MessageIdInvalid:
        pass
