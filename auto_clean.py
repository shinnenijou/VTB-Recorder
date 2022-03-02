import time
import calendar
import os
import json
from socket import *

def send_msg(serverName, serverPort, request, headers, data):
    message = request
    for key, value in headers.items():
        message += f"{key}: {value}\r\n"
    message += "\r\n"
    message += data
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(message.encode())
    recv = "a"
    ret = ""
    while recv:
        recv = clientSocket.recv(2048)
        ret += recv.decode()
    clientSocket.close()
    return ret

# CONSTANT
SERVER_NAME = "127.0.0.1"
SERVER_PORT = 80
FILES_PATH = "/www/mycloud/uploads/2/record"
TRANSCODE_FORMAT = "mp4"
EXPIRATION = 7
LISTEN_INTERVAL = 60 * 60

login_request = "POST /api/v3/user/session HTTP/1.1\r\n"
login_data = '{"userName":"admin@shinnen.cloud","Password":"7A5gLduc","captchaCode":""}'
login_headers = {
    "Host": f"{SERVER_NAME}",
    "Connection": "close",
    "Content-Length": f"{len(login_data.encode())}",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76",
    "Content-Type": "application/json",
    "Origin": f"http://{SERVER_NAME}",
    "Referer": f"http://{SERVER_NAME}",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

list_request = "POST /api/v3/admin/file/list HTTP/1.1\r\n"
list_data = '{"page":1,"page_size":10,"order_by":"id desc","conditions":{},"searches":{}}'
list_headers = {
    "Host":f"{SERVER_NAME}",
    "Connection": "close",
    "Content-Length": f"{len(list_data.encode())}",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76",
    "Content-Type": "application/json",
    "Origin": f"http://{SERVER_NAME}",
    "Referer": "http://{SERVER_NAME}/admin/file/import",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5",
}

delete_request = "POST /api/v3/admin/file/delete HTTP/1.1\r\n"
delete_data = ""
delete_headers = {
    "Host": f"{SERVER_NAME}",
    "Connection": "close",
    "Content-Length": f"{len(delete_data.encode())}",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76",
    "Content-Type": "application/json",
    "Origin": f"http://{SERVER_NAME}",
    "Referer": "http://{SERVER_NAME}/admin/file",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5"
}

# main loop
while True:
    # try to fetch items list
    recv = send_msg(SERVER_NAME, SERVER_PORT, list_request, list_headers, list_data)
    # login if need
    if '"code":401' in recv:
        recv = send_msg(SERVER_NAME, SERVER_PORT, login_request, login_headers, login_data)
        for word in recv.split():
            if "cloudreve-session" in word:
                list_headers["Cookie"] = f"{word[:-1]}"
                delete_headers["Cookie"] = f"{word[:-1]}"
        # try to fecth items list again
        recv = send_msg(SERVER_NAME, SERVER_PORT, list_request, list_headers, list_data)

    # process receive data
    recv = json.loads(recv[recv.find("\r\n{") + 2 : recv.find("\r\n0\r\n")])
    time_now = time.time()
    for item in recv["data"]["items"]:
        filename = item["Name"]
        fileID = item["ID"]
        timestr = filename[-len(TRANSCODE_FORMAT) - 16:-len(TRANSCODE_FORMAT) - 1]
        record_time = calendar.timegm(time.strptime(timestr, "%Y%m%d_%H%M%S")) - 8 * 60 * 60
        if time_now - record_time > EXPIRATION * 24 * 60 * 60:
            delete_data = '{"id":[' + str(fileID) + "]}"
            delete_headers["Content-Length"] = f"{len(delete_data.encode())}"
            recv = send_msg(SERVER_NAME, SERVER_PORT, delete_request, delete_headers, delete_data)
            with open("clean.log", "a") as file:
                log = f"{time.asctime(time.gmtime(time_now+8*60*60))}: {filename} deleted\r\n"
                print(log, end = "")
                file.write(log)
    time.sleep(LISTEN_INTERVAL)
