import os
import time
import config

while True:
    os.system("clear")
    encode_files = os.listdir(config.ENCODE_PATH)
    streamers = os.listdir(config.CONFIG_PATH)
    if not encode_files:
        print("NOT FOUND file to transcode")
    for file in encode_files:
        if config.RECORD_FORMAT in file:
            print("Check and transcode the record file: {file}")
            new_file = file[:-len(config.RECORD_FORMAT)] + config.TRANSCODE_FORMAT
            cmd = f"ffmpeg -i {config.ENCODE_PATH}/{file} -y -c:v copy -c:a copy {config.ENCODE_PATH}/{new_file}"
            os.system(cmd)
            for streamer in streamers:
                if streamer in file:
                    os.system(f"mv {config.ENCODE_PATH}/{new_file} {config.PATH}/{streamer}/{new_file}")
                    os.system(f"rm {config.ENCODE_PATH}/{file}")
    time.sleep(config.TRANSCODE_INTERVAL)