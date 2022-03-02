import time
import calendar
import config
import os
def extract_time(filename : str) -> float:
    # extract timestamp from a given filename to GMT+8 time zone
    i = filename.rfind('.')
    # YYYYmmdd_HHMMSS.format, at least 15 chars before '.'
    if i < 15: 
        return -1.0
    else:
        return calendar.timegm(time.strptime(
            filename[i - 15 : i], config.TIME_FORMAT))

def gmt8time(secs:float=None) -> str:
    if not secs:
        secs = time.time() +8 * 60 * 60
    return time.strftime(config.TIME_FORMAT, time.gmtime(secs))

def transcode(path:str, save_path:str, log_path, trans_format:str)->None:
    # transcode
    filename = path[path.rfind('/') + 1 : path.rfind('.')]
    new_file = f"{filename}.{trans_format}"
    cmd = f"ffmpeg -i {path} -y -c:v copy -c:a copy {save_path}/{new_file}"\
        + f">{log_path}/{filename}.log 2>&1"
    status = os.system(cmd)
    # clean old file after transcode done
    if not status:
        # delete origin file
        os.system(f"rm {path}")
    else:
        # delete failed transcode file
        os.system(f"rm {save_path}/{new_file}")
        # move origin file as final file
        os.system(f"mv {path} {save_path}/{path[path.rfind('/') + 1:]}")
