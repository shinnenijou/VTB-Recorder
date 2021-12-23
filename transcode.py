import os
import time

# const
INTERVAL = 20

path = os.getcwd()
config_path = path + "/config"
encode_path = path + "/temp/encode"

while True:
    os.system("clear")
    encode_files = os.listdir(encode_path)
    streamers = os.listdir(config_path)
    if not encode_files:
        print("NOT FOUND file to transcode")
    for file in encode_files:
        if ".ts" in file:
            print("Check and transcode the record file: {}".format(file))
            new_file = file[:-3] + ".mp4"
            cmd = "ffmpeg -i {}/{} -y -c:v copy -c:a copy {}/{}".format(encode_path, file, encode_path, new_file)
            os.system(cmd)
            for streamer in streamers:
                if streamer[:-4] in file:
                    os.system("mv {}/{} {}/{}/{}".format(encode_path, new_file, path, streamer[:-4], new_file))
                    os.system("rm {}/{}".format(encode_path, file))
    time.sleep(INTERVAL)