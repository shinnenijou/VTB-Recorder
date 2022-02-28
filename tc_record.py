import time
import os
import requests
import json
import config

streamer = input("Enter the streamer's name you want to record: ").strip().replace(' ', '_').lower()

# read live url from a external file "{streamer}.json"
with open(f"{config.CONFIG_PATH}/{streamer}.json") as file:
    streamer_config = json.loads(file.read())
    room_url = streamer_config["TWITCAS_URL"].strip()
    room_id = room_url[room_url.find('/') + 1:]

# mkdir
os.system(f"mkdir {streamer}")
os.system(f"mkdir {config.TEMP_DIR_PATH}")
os.system(f"mkdir {config.ENCODE_PATH}")
os.system(f"mkdir {config.RECORD_PATH}")

API = config.TWITCAS_API(room_id)
while True:
    # get live info from twitcasting api
    while True:
        os.system("clear")
        # set password if exists
        pw = streamer_config["TWITCAS_PASSWORD"]
        if pw:
            print(f"Detect the password: {pw}")
            pw = f"--twitcasting-password {pw}"

        # Listen the stream status    
        print(room_url)
        print(room_id)
        try:
            resp = requests.get(API, headers=config.HEADERS)
            resp.encoding = "UTF-8"
            info = json.loads(resp.text)
            if "movie" in info:
                live_status = info['movie']['live']
                if live_status:
                    break
            print("The stream is offline.")
        except Exception as e:
            time_stamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime(time.time() + 8 * 60 * 60))
            with open(f"{config.LOG_PATH}/tc_{room_id}.log", 'a') as log_file:
                log_file.write(f"Error Occurs at {time_stamp}: {str(e)}\r\n")

        time.sleep(config.LISTEN_INTERVAL)
        

    # record stream
    os.system("clear")
    print(f"Start to record the stream: {streamer} from twitcasting.tv")
    time_stamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime(time.time() + 8 * 60 * 60))
    file_name = f"{streamer}_{time_stamp}.{config.RECORD_FORMAT}"
    os.system(f"streamlink {room_url} best {pw} -o {config.RECORD_PATH}/{file_name}")
    os.system(f"mv {config.RECORD_PATH}/{file_name} {config.ENCODE_PATH}/{file_name}")