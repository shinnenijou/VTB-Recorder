#!/usr/bin/python3
import time
import os
import sys
import requests
import json
from config import *
from tools import *
import threading

input = sys.argv[-1]
# read live url from a external file "{streamer}.json"
with open(f"{CONFIG_PATH}/{input}.json") as file:
    STREAMER_CONFIG = json.loads(file.read())
    STREAMER_NAME = STREAMER_CONFIG["OFFICIAL_NAME"]
    ROOM_URL = STREAMER_CONFIG["BILI_URL"].strip()
    ROOM_ID = ROOM_URL[ROOM_URL.rfind('/') + 1:]
    FINAL_PATH = f"{RECORD_PATH}/{STREAMER_NAME}"
# mkdir
os.system(f"mkdir {RECORD_PATH}")
os.system(f"mkdir {RECORD_PATH}/{STREAMER_NAME}")
os.system(f"mkdir {TEMP_PATH}")
os.system(f"mkdir {LOG_PATH}")
os.system(f"mkdir {RECORD_LOG_PATH}")
os.system(f"mkdir {RECORD_LOG_PATH}/{STREAMER_NAME}")
os.system(f"mkdir {TRANS_LOG_PATH}")
os.system(f"mkdir {TRANS_LOG_PATH}/{STREAMER_NAME}")
# fetch API to listen live status
API = BILI_API(ROOM_ID)
while True:
    # get live info from bilibili api
    while True:
        try:
            os.system("clear")
            print(ROOM_ID)
            print(STREAMER_NAME)
            resp = requests.get(API, HEADERS)
            live_info = json.loads(resp.text)
            if "data" in live_info:
                status = live_info['data']['live_status']
                title = live_info['data']['title'].replace(' ', '_')
                if status == 1:
                    break
            print("The stream is offline.")
        except Exception as e:
            with open(f"{RECORD_LOG_PATH}/{STREAMER_NAME}/errors.log", 'a') as file:
                file.write(f"Error Occurs at {gmt8time()}: {str(e)}\r\n")
        time.sleep(LISTEN_INTERVAL)

    # record stream
    os.system("clear")
    print(f"Start to record the stream: {STREAMER_NAME} from bilibili.com")
    filename = f"{gmt8time()}_{title}_{STREAMER_NAME}.{RECORD_FORMAT}"
    options = ['streamlink', ROOM_URL, 'best', f'-o {TEMP_PATH}/{filename}']
    os.system(' '.join(option for option in options))

    # transcode after recording done
    thread = threading.Thread(
        target=transcode,
        args=(filename, TRANSCODE_FORMAT,
            TEMP_PATH, FINAL_PATH, f'{TRANS_LOG_PATH}/{STREAMER_NAME}')
    )
    thread.start()