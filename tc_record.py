import time
import os
import requests
import json

# const
INTERVAL = 30
RECORD_FORMAT = 'ts'

streamer_name = input("Enter the streamer's name you want to record: ").strip().replace(' ', '_').lower()
path = os.getcwd()
config_path = path + "/config"

# load the streamers list from a external file "streamers.txt"
with open('{}/{}.txt'.format(config_path, streamer_name)) as urls:
    for url in urls.readlines():
        if "twitcasting" in url:
            room_id = url[23:].strip()
            room_url = url.strip()
            break

# mkdir for record files
os.system("mkdir {}".format(streamer_name))
#save_path = path + "/{}".format(streamer_name)
record_path = path + "/temp/record"
encode_path = path + "/temp/encode"
log_path = path + "/log"

api_url = "https://twitcasting.tv/streamserver.php?target={}&mode=client".format(room_id)

while True:
    # get live info from twitcasting api
    while True:
        # set password if exists
        pw = ""
        try:
            with open("{}/{}_password.txt".format(config_path, streamer_name)) as f:
                pw = f.readline().strip()
        except FileNotFoundError:
            pass
        if pw:
            print("Detect the password: {}".format(pw))
            pw = " --twitcasting-password {}".format(pw)

        # Detect stream status    
        os.system("clear")
        print(room_url)
        print(room_id)
        try:
            resp = requests.get(api_url)
            resp.encoding = "UTF-8"
            info = json.loads(resp.text)
            if "movie" in info:
                live_status = info['movie']['live']
                if live_status:
                    break
            print("The stream is offline.")
        except Exception as e:
            time_stamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime(time.time() + 8 * 60 * 60))
            with open(f"{log_path}/room_id.log", 'a') as log_file:
                log_file.write(f"Error Occurs at {time_stamp}: {str(e)}\r\n")

        time.sleep(INTERVAL)
        

    # record stream
    os.system("clear")
    print("Start to record the stream: {} from twitcasting.tv".format(streamer_name))
    time_stamp = time.strftime("%Y%m%d_%H%M%S", time.gmtime(time.time() + 8 * 60 * 60))
    file_name = "{}_{}.{}".format(streamer_name, time_stamp, RECORD_FORMAT)
    cmd = "streamlink {} best{} -o {}/{}".format(room_url, pw, record_path, file_name)
    os.system(cmd)
    os.system("mv {}/{} {}/{}".format(record_path, file_name, encode_path, file_name))