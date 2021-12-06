import os
import time

save_path = os.getcwd() + "/saveVideo"
drive = "little:mitagun"
copied_path = os.getcwd() + "/copiedVideo"

while(1):
    os.system("clear")
    print("checking to upload")

    # copy files to online drive
    files = os.listdir(save_path)
    if(files):
        for file in files:
            cmd = "rclone copy --progress --max-age 1h {} {}".format(save_path, drive)
            result = os.system(cmd)
                
            # tranference successed
            if result == 0:
                os.system("mv {}/{} {}/{}".format(save_path, file, copied_path, file))

    # clean old archive files(at least 2 days ago)
    files = os.listdir(copied_path)
    date_1 = time.strftime("%Y%m%d", time.gmtime(time.time() + 8 * 60 * 60))
    date_2 = time.strftime("%Y%m%d", time.gmtime(time.time() - 16 * 60 * 60))
    date_3 = time.strftime("%Y%m%d", time.gmtime(time.time() - 40 * 60 * 60))
    for file in files:
        if not(date_1 in file or date_2 in file or date_3 in file):
            os.system("rm {}/{}".format(copied_path, file))
            
    print("done")
    time.sleep(60)