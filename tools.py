import time
import calendar
import config
import os
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

    cmd = f"ffmpeg -i {path}/{filename} -vsync cfr -x264opts force-cfr=1 -y -c:v copy -c:a libx264 {path}/{new_file}"\
        + f">{log_path}/{filename.rpartition('.')[0]}.log 2>&1"
    status = os.system(cmd)
    #########
    # 提取音频(初配信临时功能)
    #audio_file = f"{filename.rpartition('.')[0]}.mp3"
    #cmd = f"ffmpeg -i {path}/{filename} -y {path}/{audio_file}"
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