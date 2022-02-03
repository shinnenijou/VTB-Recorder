import os
import time
import config

while True:
    os.system("clear")
    # load the streamers list from a external file "streamers.txt"
    streamers = os.listdir(config.CONFIG_PATH)
    for streamer in streamers:
        print(f"Checking {streamer}'s record files...", end = '')
        try:
            record_files = os.listdir(f"{config.PATH}/{streamer}")
        except FileNotFoundError:
            record_files = []
        
        # try to copy files to the cloud drive
        if record_files:
            print(f"START to copy {streamer}'s record files")
            cmd = f"rclone copy --progress --max-age 1h {config.PATH}/{streamer} {config.DRIVE}/{streamer}"
            fail = os.system(cmd)

        # copy successed
            if not fail:
                for file in record_files:
                    os.system(f"mv {config.PATH}/{streamer}/{file} {config.COPIED_PATH}/{file}")
        else:
            print("NOT FOUND")

    # clean old archive files(at least 2 days ago)
    copied_files = os.listdir(config.COPIED_PATH)
    date_1 = time.strftime("%Y%m%d", time.gmtime(time.time() + 8 * 60 * 60))
    date_2 = time.strftime("%Y%m%d", time.gmtime(time.time() - 16 * 60 * 60))
    date_3 = time.strftime("%Y%m%d", time.gmtime(time.time() - 40 * 60 * 60))
    for file in copied_files:
        if not(date_1 in file or date_2 in file or date_3 in file):
            os.system("rm {config.COPIED_PATH}/{file}")

    time.sleep(config.UPLOAD_INTERVAL)