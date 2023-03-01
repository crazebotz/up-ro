import math
import time, os, json

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cancel_button = InlineKeyboardButton("Cancel", callback_data="cancel_upload")
reply_markup = InlineKeyboardMarkup([[cancel_button]])

# TASKS = {}
 
file_size = 1024  # In MB
download_speed = 0  # In MBPS


# Calculate the time in seconds if download_speed is not zero
async def progress_for_pyrogram(current, total, ud_type, message, start, bot,
                                uid, status):
  now = time.time()
  # print(now)
  # print(start)
  diff = now - start

  if round(diff % 10.00) == 0 or current == total:

    percentage = current * 100 / total

    if os.path.exists(status):
      with open(status, 'r+') as f:
        statusMsg = json.load(f)
        if not statusMsg["running"]:
          bot.stop_transmission()
          print("STOPPED")
    speed = current / diff
    elapsed_time = round(diff) * 1000
    time_to_completion = round((total - current) / speed) * 1000
    estimated_total_time = elapsed_time + time_to_completion

    elapsed_time = TimeFormatter(milliseconds=elapsed_time)
    estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
    file_size = total - current
    if speed != 0:
      download_time = (file_size * 1024 * 1024) / (speed * 1024 * 1024 / 1)
      minutes, seconds = divmod(download_time, 60)
      hours, minutes = divmod(int(minutes), 60)
      REMAIN_TIME = (f"{hours:02d}H {minutes:02d}M {int(seconds):02d}s")
    else:
      REMAIN_TIME = ("00:00:00")

    progress = "[{0}{1}]\n**Progress :** {2}%\n".format(
      ''.join(["◾" for i in range(math.floor(percentage / 10))]),  #7.6923
      ''.join(["◽" for i in range(10 - math.floor(percentage / 10))]),
      round(percentage, 2))

    tmp = progress + "**Completed :** {0} of {1}\n**Speed :** {2}/s\n**ETA :** {3}\n".format(
      humanbytes(current), humanbytes(total), humanbytes(speed), REMAIN_TIME)

    #estimated_total_time if estimated_total_time != '' else "0 s")

    cancel_button = InlineKeyboardButton(
      "Cancel", callback_data=f"cancel_upload#{status}")

    reply_markup = InlineKeyboardMarkup([[cancel_button]])

    try:
      await message.edit_text("{}{}".format(ud_type, tmp),
                              reply_markup=reply_markup)
    except Exception as ex:
      print(ex)


def humanbytes(size):
  # 2**10 = 1024
  if not size:
    return ""
  power = 2**10
  n = 0
  Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
  while size > power:
    size /= power
    n += 1
  return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
  seconds, milliseconds = divmod(int(milliseconds), 1000)
  minutes, seconds = divmod(seconds, 60)
  hours, minutes = divmod(minutes, 60)
  days, hours = divmod(hours, 24)
  tmp = ((str(days) + "d, ") if days else "") + \
      ((str(hours) + "h, ") if hours else "") + \
      ((str(minutes) + "m, ") if minutes else "") + \
      ((str(seconds) + "s, ") if seconds else "") + \
      ((str(milliseconds) + "ms, ") if milliseconds else "")
  return tmp[:-2]
