import time
import os
import requests
import json
import config

input = input("Enter the streamer's name you want to record: ").strip().replace(' ', '_').lower()
with open(f"{config.CONFIG_PATH}/{input}.json") as file:
    streamer_config = json.loads(file.read())
    room_url = streamer_config["BILI_URL"].strip()
    room_id = room_url[room_url.find('/') + 1:]
    streamer = streamer_config["OFFICIAL_NAME"]

# mkdir
os.system(f"mkdir {streamer}")
os.system(f"mkdir {config.TEMP_DIR_PATH}")
os.system(f"mkdir {config.ENCODE_PATH}")
os.system(f"mkdir {config.RECORD_PATH}")

API = config.BILI_API(room_id)
while True:
    # get live info from bilibili api
    while True:
        try:
            os.system("clear")
            print(room_url)
            print(room_id)
            resp = requests.get(API, config.HEADERS)
            resp.encoding = "UTF-8"
            info = json.loads(resp.text)
            if "data" in info:
                live_status = info['data']['live_status']
                live_title = info['data']['title'].replace(' ', '_')
                if live_status == 1:
                    break
            print("The stream is offline.")
        except Exception as e:
            time_stamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime(time.time() + 8 * 60 * 60))
            with open(f"{config.LOG_PATH}/bili_{room_id}.log", 'a') as log_file:
                log_file.write(f"Error Occurs at {time_stamp}: {str(e)}\r\n")
        time.sleep(config.LISTEN_INTERVAL)

    # record stream
    os.system("clear")
    print(f"Start to record the stream: {streamer} from bilibili.com")
    time_stamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime(time.time() + 8 * 60 * 60))
    file_name = f"{live_title}_{streamer}_{time_stamp}.{config.RECORD_FORMAT}"
    os.system(f"streamlink {room_url} best -o {config.RECORD_PATH}/{file_name}")
    os.system(f"mv {config.RECORD_PATH}/{file_name} {config.ENCODE_PATH}/{file_name}")