import os
import time
import config
import calendar
import json

# save exist record file for each streamer
streamers_files = {}
while True:
    os.system("clear")
    config_files = os.listdir(config.CONFIG_PATH)
    for config_file in config_files:
        # read streamer config for each streamer
        with open(f"{config.CONFIG_PATH}/{config_file}", 'r') as file:
            streamer_config = json.loads(file.read())
            streamer = streamer_config["OFFICIAL_NAME"]
            drive_path = streamer_config["DRIVE"]
            # if there is a new config
            if streamer not in streamers_files:
                streamers_files[streamer] = []
                os.system(f"rclone mkdir {drive_path}/{streamer}")
        # print previously exist files
        print(f"Checking {streamer}'s record files...", end="")
        print(f"{len(streamers_files[streamer])} files exist: ")
        for filename in streamers_files[streamer]:
            print(f"    {filename}")
        
        # check new files
        try:
            current_files = os.listdir(f"{config.PATH}/{streamer}")
        except FileNotFoundError:
            current_files = []
        
        # try to copy files to the cloud drive
        for filename in current_files:
            if filename not in streamers_files[streamer]:
                print(f"START to copy {streamer}'s record files")
                cmd = f"rclone copy --progress --max-age 1h {config.PATH}/{streamer} {drive_path}/{streamer}"
                os.system(cmd)
                streamers_files[streamer].append(filename)
                if "OFFICIAL_PATH" in streamer_config:
                    os.system(f"scp {config.PATH}/{streamer}/{filename} root@{config.OFFICIAL_SERVERNAME}:{streamer_config['OFFICIAL_PATH']}") 
    
        # delete old record files of current streamer(expiration loaded from config.py)
        time_now = time.time()
        for filename in current_files:
            timestr = filename[-len(config.TRANSCODE_FORMAT) - 16:-len(config.TRANSCODE_FORMAT) - 1]
            # convert to GMT (8h time gap)
            record_time = calendar.timegm(time.strptime(timestr, "%Y%m%d_%H%M%S")) - 8 * 60 * 60
            if time_now - record_time > config.EXPIRATION * 24 * 60 * 60:
                os.system(f"rm {config.PATH}/{streamer}/{filename}")
                streamers_files[streamer].remove(filename)
            
    time.sleep(config.UPLOAD_INTERVAL)