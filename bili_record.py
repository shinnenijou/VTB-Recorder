import time
import os
import requests
import json

# const
INTERVAL = 30
RECORD_FORMAT = 'ts'

streamer_name = input("Enter the streamer's name you want to record: ").strip().replace(' ', '_').lower()
path = os.getcwd()

# load the streamers list from a external file "streamers.txt"
with open('{}/config/{}.txt'.format(path, streamer_name)) as urls:
    for url in urls.readlines():
        if "bilibili" in url:
            room_id = url[26:].strip()
            room_url = url.strip()
            break

# mkdir for record files
os.system("mkdir {}".format(streamer_name))
#save_path = path + "/{}".format(streamer_name)
record_path = path + "/temp/record"
encode_path = path + "/temp/encode"

api_url = "https://api.live.bilibili.com/room/v1/Room/get_info?room_id={}&from=room".format(room_id)

while True:
    # get live info from bilibili api
    while True:
        try:
            os.system("clear")
            print(room_url)
            print(room_id)
            resp = requests.get(api_url)
            resp.encoding = "UTF-8"
            info = json.loads(resp.text)
            live_status = info['data']['live_status']
            live_title = info['data']['title']
            if live_status == 1:
                break
            print("The stream is offline.")
            time.sleep(INTERVAL)
        except ConnectionError:
            pass

    # record stream
    os.system("clear")
    print("Start to record the stream: {} from bilibili.com".format(streamer_name))
    time_stamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime(time.time() + 8 * 60 * 60))
    file_name = "{}_{}_{}.{}".format(live_title, streamer_name, time_stamp, RECORD_FORMAT)
    cmd = "streamlink {} best -o {}/{}".format(room_url, record_path, file_name)
    os.system(cmd)
    os.system("mv {}/{} {}/{}".format(record_path, file_name, encode_path, file_name))