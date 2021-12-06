import time
import os

url = "https://twitcasting.tv/mi_tagun"
streamName = "mi_tagun"
format = 'mp4'
passWord = "123456"

path = os.getcwd()
while(1):
    os.system("clear")
    time_gmt8 = time.time() + 8 * 60 * 60
    t = time.strftime("%Y%m%d_%H%M%S", time.gmtime(time_gmt8))
    fileName = "{}/saveVideo/{}_{}.{}".format(path, streamName, t, format)
    cmd = "streamlink {} best --twitcasting-password {} -o {}".format(url, passWord, fileName)
    os.system(cmd)
    time.sleep(20)