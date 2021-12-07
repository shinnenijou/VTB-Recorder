import time
import os
import subprocess

streamer_name = ""
record_name = input("Please input the name of streamer you want to record: ")
record_name = record_name.strip().replace(' ', '_').upper()
path = os.getcwd()

# load the streamers list from a external file "streamers.txt"
with open('{}/streamers.txt'.format(path)) as streamers:
    for line in streamers.readlines():
        strs = line.split(' ')
        if(strs[0].upper() == record_name):
            streamer_name = strs[0]
            stream_url = strs[1]
            file_format = strs[2].strip()

            # Password for Twitcasting locked stream
            password = ""
            if len(strs) > 3:
                password += " --twitcasting-password {}".format(strs[3].strip())
            start = 1
            break
    
    if not start:
        print("NOT FOUND the streamer name")

# if the name need to record found in the file "streamers.txt"
if streamer_name:
    file_list = os.listdir(path)
    if not streamer_name in file_list:
        os.system("mkdir {}".format(streamer_name))
    save_path = path + "/{}".format(streamer_name)

# monitor and record the stream
while streamer_name:
    os.system("clear")
    print("Now recording: {}: {}".format(streamer_name, stream_url))
    print()
    time_gmt8 = time.strftime("%Y%m%d_%H%M%S", time.gmtime(time.time() + 8 * 60 * 60))
    file_name = "{}/{}_{}.{}".format(save_path, streamer_name, time_gmt8, file_format)
    cmd = "streamlink {} best{} -o {}".format(stream_url, password, file_name)
    os.system(cmd)
    time.sleep(20)