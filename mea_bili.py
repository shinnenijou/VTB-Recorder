import time
import os

url = "https://live.bilibili.com/12235923"
streamName = "mea"
format = 'mp4'

path = os.getcwd()
while(1):
    os.system("clear")
    time_gmt8 = time.time() + 8 * 60 * 60
    t = time.strftime("%Y%m%d_%H%M%S", time.gmtime(time_gmt8))
    fileName = "{}/saveVideo/{}_{}.{}".format(path, streamName, t, format)
    cmd = "streamlink {} best -o {}".format(url, fileName)
    os.system(cmd)
    time.sleep(20)