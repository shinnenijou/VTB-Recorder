import os
import time

path = os.getcwd()
drive = "little:Record_Files"
copied_path = os.getcwd() + "/copiedVideo"

while(1):
    os.system("clear")
    # load the streamers list from a external file "streamers.txt"
    save_dir = os.listdir()
    with open('{}/streamers.txt'.format(path)) as streamers:
        for line in streamers.readlines():
            strs = line.split(' ')
            streamer_name = strs[0]
            print("Checking {}'s record files...".format(streamer_name), end = '')
            if streamer_name in save_dir:
                # try to copy files to the cloud drive
                record_files = os.listdir("{}/{}".format(path, streamer_name))
                if record_files:
                    print("START to copy {}'s record files".format(streamer_name))
                    cmd = "rclone copy --progress --max-age 1h {}/{} {}/{}".format(
                        path, streamer_name, drive, streamer_name)
                    fail = os.system(cmd)

                # copy successed
                    if not fail:
                        for record_file in record_files:
                            os.system("mv {}/{}/{} {}/{}".format(
                                path, streamer_name, record_file, copied_path, record_file))
                else:
                    print("NOT FOUND {}'s record files".format(streamer_name))
            else:
                print("NOT FOUND dictory named {}".format(streamer_name))

    # clean old archive files(at least 2 days ago)
    copied_files = os.listdir(copied_path)
    date_1 = time.strftime("%Y%m%d", time.gmtime(time.time() + 8 * 60 * 60))
    date_2 = time.strftime("%Y%m%d", time.gmtime(time.time() - 16 * 60 * 60))
    date_3 = time.strftime("%Y%m%d", time.gmtime(time.time() - 40 * 60 * 60))
    for copied_file in copied_files:
        if not(date_1 in copied_file or date_2 in copied_file or date_3 in copied_file):
            os.system("rm {}/{}".format(copied_path, copied_file))
            
    print("done")
    time.sleep(60)