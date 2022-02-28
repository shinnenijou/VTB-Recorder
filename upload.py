import os
import time
import config
import calendar
import json

while True:
    os.system("clear")
    # load the streamers list from a external file "streamers.txt"
    config_files = os.listdir(config.CONFIG_PATH)
    for config_file in config_files:
        with open(f"{config.CONFIG_PATH}/{config_file}", 'r') as file:
            streamer_config = json.loads(file.read())
            streamer = streamer_config["OFFICLAL_NAME"]
        print(f"Checking {streamer}'s record files...", end = '')
        try:
            record_files = os.listdir(f"{config.PATH}/{streamer}")
        except FileNotFoundError:
            record_files = []
        
        # try to copy files to the cloud drive
        if record_files:
            print(f"START to copy {streamer}'s record files")
            cmd = f"rclone copy --progress --max-age 1h \
                {config.PATH}/{streamer} {streamer_config['drive']}/{streamer}"
            fail = os.system(cmd)

            # if copy successed
            # clean old files(expiration set by config.py)
            if not fail:
                time_now = time.time()
                for file in record_files:
                    timestr = file[-len(config.TRANSCODE_FORMAT) - 16:-len(config.TRANSCODE_FORMAT) - 1]
                    # convert to GMT (8h time gap)
                    record_time = calendar.timegm(time.strptime(timestr, "%Y%m%d_%H%M%S")) - 8 * 60 * 60
                    if time_now - record_time > config.EXPIRATION * 24 * 60 * 60:
                        os.system(f"rm {config.PATH}/{streamer}/{file}")

        else:
            print("NOT FOUND")
  
    time.sleep(config.UPLOAD_INTERVAL)