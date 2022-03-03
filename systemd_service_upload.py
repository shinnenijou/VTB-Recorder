#!/usr/bin/python3
import os
import time
from config import *
from tools import *
import json

os.system(f"mkdir {UPLOAD_LOG_PATH}")
# save exist record file for each streamer
streamers_files_lists = {}
while True:
    os.system("clear")
    streamers_list = os.listdir(CONFIG_PATH)
    for streamer in streamers_list:
        # read streamer config
        with open(f"{CONFIG_PATH}/{streamer}", 'r') as file:
            streamer_config = json.loads(file.read())
            streamer_name = streamer_config["OFFICIAL_NAME"]
            drive_path = streamer_config["ONEDRIVE"]
            # if there is a new config
            if streamer_name not in streamers_files_lists:
                streamers_files_lists[streamer_name] = []
                os.system(f"rclone mkdir {drive_path}/{streamer_name}")
        # print previously exist files
        print(f"Checking {streamer_name}'s record files...", end="")
        print(f"{len(streamers_files_lists[streamer_name])} files exist: ")
        for filename in streamers_files_lists[streamer_name]:
            print(f"    {filename}")
        
        # check new files
        try:
            current_files = os.listdir(f"{RECORD_PATH}/{streamer_name}")
        except FileNotFoundError:
            current_files = []
        
        # clean old files if not official record
        if "OFFICIAL_PATH" not in streamer_config:
            for filename in current_files:
                record_time = extract_time(filename)
                if time.time() + 8 * 60 * 60 - record_time > EXPIRATION * 24 * 60 * 60:
                    os.system(f"rm {RECORD_PATH}/{streamer_name}/{filename}")

        # try to copy files to the cloud drive
        for filename in current_files:
            if filename not in streamers_files_lists[streamer_name]:
                print(f"START to copy {streamer}'s record files")
                cmd = f"rclone copy --progress "\
                    + f"{RECORD_PATH}/{streamer_name} {drive_path}/{streamer_name}"
                os.system(cmd)
                streamers_files_lists[streamer_name].append(filename)

                # transfer record file to remote host if it is official record
                # if "OFFICIAL_PATH" in streamer_config:
                #     thread = threading.Thread(
                #         target=transfer_to_remote,
                #         args=(
                #             f"{RECORD_PATH}/{streamer_name}",
                #             f"{drive_path}/{streamer_name}"
                #         )
                #     )
                #     thread.start()
            
    time.sleep(config.UPLOAD_INTERVAL)