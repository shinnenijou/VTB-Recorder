import time
import calendar
import config
import os
from enum import IntEnum

# API
def twicas_api(room_id):
    return f"https://twitcasting.tv/streamserver.php?target={room_id}&mode=client"
def bili_api(room_id):
    return f"https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}&from=room"

class StreamType(IntEnum):
    none = 0
    bilibili = 1
    twitcast = 2

class StreamStatus(IntEnum):
    none = 0
    online = 1
    offline = 2

def get_type(url: str):
    if 'bilibili' in url:
        return StreamType.bilibili
    elif 'twitcast' in url:
        return StreamType.twitcast

    return StreamType.none

def get_api(type: StreamType, id: str):
    api_map = {
        StreamType.none: None,
        StreamType.bilibili: bili_api,
        StreamType.twitcast: twicas_api
    }
    if api_map[type]:
        return api_map[type](id)

    return ""

def extract_time(filename : str) -> float:
    # extract timestamp from a given filename to GMT+8 time zone
    i = filename.rfind('.')
    # YYYYmmdd_HHMMSS.format, at least 15 chars before '.'
    if i < 15: 
        return 3000000000
    else:
        #return calendar.timegm(time.strptime(filename[i - 15 : i], config.TIME_FORMAT))
        return calendar.timegm(time.strptime(filename[:15], config.TIME_FORMAT))

def gmt8time(secs:float=None) -> str:
    if not secs:
        secs = time.time() +8 * 60 * 60
    return time.strftime(config.TIME_FORMAT, time.gmtime(secs))

def transcode(filename:str, trans_format:str, path:str, new_path:str, log_path : str)->None:
    # transcode
    new_file = f"{filename.rpartition('.')[0]}.{trans_format}"

    cmd = f"{config.BIN_PATH}/ffmpeg -i {path}/{filename} -y -c:v copy -c:a copy {path}/{new_file}"\
        + f">{log_path}/{filename.rpartition('.')[0]}.log 2>&1"
    status = os.system(cmd)
    #########
    # 提取音频(初配信临时功能)
    #audio_file = f"{filename.rpartition('.')[0]}.mp3"
    #cmd = f"{config.BIN_PATH}/ffmpeg -i {path}/{filename} -y {path}/{audio_file}"
    #status = os.system(cmd)
    #if not status:
    #    os.system(f"mv {path}/{audio_file} {new_path}/{audio_file}")
    ########
    # clean old file after transcode done
    if not status:
        # delete origin file
        os.system(f"mv {path}/{new_file} {new_path}/{new_file}")
        os.system(f"rm {path}/{filename}")
        return new_file
    else:
        # delete failed transcode file
        os.system(f"rm {path}/{new_file}")
        # move origin file as final file
        os.system(f"mv {path}/{filename} {new_path}/{filename}")
        return filename

def transfer_to_remote(src, dst):
    cmd = f"scp {src} {dst}"
    os.system(cmd)

def upload_baidu(path, filename, target_path):
    cmd = f'BaiduPCS-Go upload {path}/{filename} {target_path}'
    os.system(cmd)

def Mkdir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

# dir init
def dir_init():
    Mkdir(config.RECORD_PATH)
    Mkdir(config.TEMP_PATH)
    Mkdir(config.LOG_PATH)