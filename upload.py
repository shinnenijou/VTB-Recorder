import os
import time
from xml.dom import NOT_FOUND_ERR

# const
INTERVAL = 60

path = os.getcwd()
config_path = path + "/config"
drive = "shinnen:Record_Files"
copied_path = path + "/temp/copied"

while True:
    os.system("clear")
    # load the streamers list from a external file "streamers.txt"
    config_files = os.listdir(config_path)
    for config_file in config_files:
        if "password" in config_file:
            continue
        streamer_name = config_file[:-4]
        print("Checking {}'s record files...".format(streamer_name), end = '')
        record_files = []
        try:
            record_files = os.listdir("{}/{}".format(path, streamer_name))
        except FileNotFoundError:
            pass
        
        # try to copy files to the cloud drive
        if record_files:
            print("START to copy {}'s record files".format(streamer_name))
            cmd = "rclone copy --progress --max-age 1h {}/{} {}/{}".format(
                path, streamer_name, drive, streamer_name)
            fail = os.system(cmd)

        # copy successed
            if not fail:
                for record_file in record_files:
                    os.system("mv {}/{}/{} {}/{}".format(path, streamer_name, record_file, copied_path, record_file))
        else:
            print("NOT FOUND")

    # clean old archive files(at least 2 days ago)
    copied_files = os.listdir(copied_path)
    date_1 = time.strftime("%Y%m%d", time.gmtime(time.time() + 8 * 60 * 60))
    date_2 = time.strftime("%Y%m%d", time.gmtime(time.time() - 16 * 60 * 60))
    date_3 = time.strftime("%Y%m%d", time.gmtime(time.time() - 40 * 60 * 60))
    for copied_file in copied_files:
        if not(date_1 in copied_file or date_2 in copied_file or date_3 in copied_file):
            os.system("rm {}/{}".format(copied_path, copied_file))

    time.sleep(INTERVAL)