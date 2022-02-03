import time
import os
import requests
import json
import config

streamer = input("Enter the streamer's name you want to record: ").strip().replace(' ', '_').lower()

# read live url from a external file "{streamer}.txt"
with open(f"{config.CONFIG_PATH}/{streamer}") as urls:
    for url in urls.readlines():
        if "twitcasting" in url:
            room_id = url[23:].strip()
            room_url = url.strip()
            break

# mkdir for record files 
os.system(f"mkdir {streamer}")

API = config.TWITCAS_API(room_id)
while True:
    # get live info from twitcasting api
    while True:
        os.system("clear")
        # set password if exists
        try:
            with open("{}/{}_tc_password".format(config.PATH, streamer)) as f:
                pw = f.readline().strip()
        except FileNotFoundError:
            pw = ""
        if pw:
            print(f"Detect the password: {pw}")
            pw = f"--twitcasting-password {pw}"

        # Listen the stream status    
        print(room_url)
        print(room_id)
        try:
            resp = requests.get(API)
            resp.encoding = "UTF-8"
            info = json.loads(resp.text)
            if "movie" in info:
                live_status = info['movie']['live']
                if live_status:
                    break
            print("The stream is offline.")
        except Exception as e:
            print(e)
            time_stamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime(time.time() + 8 * 60 * 60))
            with open(f"{config.LOG_PATH}/room_id.log", 'a') as log_file:
                log_file.write(f"Error Occurs at {time_stamp}: {str(e)}\r\n")

        time.sleep(config.LISTEN_INTERVAL)
        

    # record stream
    os.system("clear")
    print(f"Start to record the stream: {streamer} from twitcasting.tv")
    time_stamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime(time.time() + 8 * 60 * 60))
    file_name = f"{streamer}_{time_stamp}.{config.RECORD_FORMAT}"
    os.system(f"streamlink {room_url} best {pw} -o {config.RECORD_PATH}/{file_name}")
    os.system(f"mv {config.RECORD_PATH}/{file_name} {config.ENCODE_PATH}/{file_name}")