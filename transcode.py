import os
import time
import config
import json

while True:
    os.system("clear")
    encode_files = os.listdir(config.ENCODE_PATH)
    config_files = os.listdir(config.CONFIG_PATH)
    if not encode_files:
        print("NOT FOUND file to transcode")
    for encode_file in encode_files:
        if config.RECORD_FORMAT in encode_file:
            print("Check and transcode the record file: {file}")
            # transcode
            new_file = encode_file[:-len(config.RECORD_FORMAT)] + config.TRANSCODE_FORMAT
            cmd = f"ffmpeg -i {config.ENCODE_PATH}/{encode_file} -y -c:v copy -c:a copy {config.ENCODE_PATH}/{new_file}"
            os.system(cmd)
            # move files
            for config_file in config_files:
                with open(f"{config.CONFIG_PATH}/{config_file}", 'r') as file:
                    streamer_config = json.loads(file.read())
                    streamer = streamer_config["OFFICIAL_NAME"]
                if streamer in encode_file:
                    os.system(f"mv {config.ENCODE_PATH}/{new_file} {config.PATH}/{streamer}/{new_file}")
                    os.system(f"rm {config.ENCODE_PATH}/{encode_file}")
    time.sleep(config.TRANSCODE_INTERVAL)