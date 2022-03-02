import time
import os
import requests
import json
from config import *
from tools import *
import threading

input = input("Enter the streamer's name: ").strip().replace(' ', '_').lower()
# read live url from a external file "{streamer}.json"
with open(f"{CONFIG_PATH}/{input}.json") as file:
    STREAMER_CONFIG = json.loads(file.read())
    STREAMER_NAME= STREAMER_CONFIG["OFFICIAL_NAME"]
    ROOM_URL = STREAMER_CONFIG["TWITCAS_URL"].strip()
    ROOM_ID = ROOM_URL[ROOM_URL.rfind('/') + 1:]
    FINAL_PATH = f"{RECORD_PATH}/{STREAMER_NAME}"
# mkdir
os.system(f"mkdir {RECORD_PATH}")
os.system(f"mkdir {RECORD_PATH}/{STREAMER_NAME}")
os.system(f"mkdir {TEMP_PATH}")
os.system(f"mkdir {LOG_PATH}")
os.system(f"mkdir {LOG_PATH}/{STREAMER_NAME}")
# fetch API to listen live status
API = TWITCAS_API(ROOM_ID)
while True:
    # get live info from twitcasting api
    while True:
        os.system("clear")
        # set password if exists
        with open(f"{CONFIG_PATH}/{input}.json") as file:
            pswd = json.loads(file.read())["TWITCAS_PASSWORD"]
        if pswd:
            print(f"Detect the password: {pswd}")
            pswd = f"--twitcasting-password {pswd}"

        # Listen the stream status    
        print(ROOM_URL)
        print(STREAMER_NAME)
        try:
            resp = requests.get(API, headers=HEADERS)
            live_info = json.loads(resp.text)
            if "movie" in live_info:
                status = live_info['movie']['live']
                if status:
                    break
            print("The stream is offline.")
        except Exception as e:
            with open(f"{LOG_PATH}/tc_{STREAMER_NAME}.log", 'a') as file:
                file.write(f"Error Occurs at {gmt8time()}: {str(e)}\r\n")
        time.sleep(LISTEN_INTERVAL)
        
    # record stream
    os.system("clear")
    print(f"Start to record the stream: {STREAMER_NAME} from twitcasting.tv")
    filename = f"{STREAMER_NAME}_{gmt8time()}.{RECORD_FORMAT}"
    os.system(f"streamlink {ROOM_URL} best {pswd} -o {TEMP_PATH}/{filename}")

    # transcode after recording done
    thread = threading.Thread(
        target=transcode,
        args=(f"{TEMP_PATH}/{filename}", 
              FINAL_PATH, f"{LOG_PATH}/{STREAMER_NAME}",
              TRANSCODE_FORMAT)
    )
    thread.start()