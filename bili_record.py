import time
import os
import requests
import json
import config

streamer_name = input("Enter the streamer's name you want to record: ").strip().replace(' ', '_').lower()

# load the streamers list from a external file "streamers.txt"
with open(f"{config.CONFIG_PATH}/{streamer_name}") as urls:
    for url in urls.readlines():
        if "bilibili" in url:
            room_id = url[26:].strip()
            room_url = url.strip()
            break

# mkdir for record files
os.system(f"mkdir {streamer_name}")

API = config.BILI_API(room_id)
while True:
    # get live info from bilibili api
    while True:
        try:
            os.system("clear")
            print(room_url)
            print(room_id)
            resp = requests.get(API)
            resp.encoding = "UTF-8"
            info = json.loads(resp.text)
            if "data" in info:
                live_status = info['data']['live_status']
                live_title = info['data']['title']
                if live_status == 1:
                    break
            print("The stream is offline.")
        except Exception as e:
            time_stamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime(time.time() + 8 * 60 * 60))
            with open(f"{config.LOG_PATH}/room_id.log", 'a') as log_file:
                log_file.write(f"Error Occurs at {time_stamp}: {str(e)}\r\n")
        time.sleep(config.LISTEN_INTERVAL)

    # record stream
    os.system("clear")
    print(f"Start to record the stream: {streamer_name} from bilibili.com")
    time_stamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime(time.time() + 8 * 60 * 60))
    file_name = f"{live_title,}_{streamer_name}_{time_stamp}.{config.RECORD_FORMAT}"
    os.system(f"streamlink {room_url} best -o {config.RECORD_PATH}/{file_name}")
    os.system(f"mv {config.RECORD_PATH}/{file_name} {config.ENCODE_PATH}/{file_name}")