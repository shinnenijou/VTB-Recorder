#!/usr/bin/python3
import os
import time
import config
import utils
import json
from loguru import logger

# save exist record file for each streamer
utils.dir_init()
utils.Mkdir(config.UPLOAD_LOG_PATH)
streamers_files_lists = {}
logger.add(f"{config.UPLOAD_LOG_PATH}" + "/runtime_{time}.log", encoding='utf-8',
            rotation='1 week', retention='1 month')
# main loop
while True:
    os.system("clear")
    streamers_list = os.listdir(config.CONFIG_PATH)
    for streamer in streamers_list:
        # read streamer config
        with open(f"{config.CONFIG_PATH}/{streamer}", 'r') as file:
            streamer_config = json.loads(file.read())
            streamer_name = streamer_config["OFFICIAL_NAME"]
            drive_path = streamer_config["ONEDRIVE"]
            # if there is a new config
            if streamer_name not in streamers_files_lists:
                streamers_files_lists[streamer_name] = []
                utils.Rclone.mkdir(f"{drive_path}/{streamer_name}")
        # print previously exist files
        print(f"Checking {streamer_name}'s record files...", end="")
        print(f"{len(streamers_files_lists[streamer_name])} files exist: ")
        for filename in streamers_files_lists[streamer_name]:
            print(f"    {filename}")
        
        # check new files
        current_files = utils.Listdir(f"{config.RECORD_PATH}/{streamer_name}")
        
        # try to copy files to the cloud drive
        for filename in current_files:
            print()
            if filename not in streamers_files_lists[streamer_name]:
                logger.info(f"START copying {streamer}/{filename}")
                src_path = f"{config.RECORD_PATH}/{streamer_name}/{filename}"
                dest_path = f"{drive_path}/{streamer_name}/{filename}"
                status = utils.Rclone.copyto(src_path, dest_path)
                
                # delete copied files if successfully copied
                if status == 0:
                    logger.success(f"{streamer}/{filename} copied")
                    streamers_files_lists[streamer_name].append(filename)
                    os.remove(src_path)
                
    time.sleep(config.UPLOAD_INTERVAL)