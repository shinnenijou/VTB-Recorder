import os
import time

url = "https://live.bilibili.com/21186547"
streamName = "shuang"
format = 'ts'

path = os.getcwd()
while(1):
    #os.system("clear")
    os.system("cls")
    time_gmt8 = time.time() + 8 * 60 * 60
    t = time.strftime("%Y%m%d_%H%M%S", time.gmtime(time_gmt8))
    fileName = "{}\\saveVideo\\{}_{}.{}".format(path, streamName, t, format)
    cmd = "E:\\software\\录像工具\\recorder\\streamlink\\bin\\streamlink {} best -o {}".format(url, fileName)
    print(cmd)
    r = os.popen(cmd)
    logName = "{}\\log\\{}_{}.log".format(path, streamName, t)
    with open(logName, 'w') as logfile:
        logfile.write(r.read())
    time.sleep(20)
