import os
import sys
import threading
from recorder import create_recorder
import utils
import config
import json

# initialize
utils.dir_init()

# create recorder
name = sys.argv[-1]
with open(f"{config.CONFIG_PATH}/{name}.json", encoding='utf-8') as file:
    streamer_config = json.loads(file.read())

recorder = create_recorder(streamer_config)
if not recorder:
    print("Stream Site is not supported")
    os._exit(-1)

while True:
    os.system("clear")
    print(recorder.get_streamer(), recorder.get_url())
    # get live info
    title = recorder.listen()

    # record stream
    filename = f"{utils.gmt8time()}_{title}_{recorder.get_streamer()}.{config.RECORD_FORMAT}"
    recorder.record(filename)

    # transcode after recording done
    thread = threading.Thread(
        target=utils.transcode,
        args=(filename, config.TRANSCODE_FORMAT,
            config.TEMP_PATH, recorder.get_record_path(), recorder.get_log_path())
    )
    thread.start()