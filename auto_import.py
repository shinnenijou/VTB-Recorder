#!/usr/bin/python3
from socket import *
import os
import time

def send_msg(serverName, serverPort, request, headers, data):
    message = request
    for key, value in headers.items():
        message += f"{key}: {value}\r\n"
    message += "\r\n"
    message += data
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    clientSocket.send(message.encode())
    recv = clientSocket.recv(2048)
    clientSocket.close()
    return recv.decode()

# CONSTANT
SERVER_NAME = "127.0.0.1"
SERVER_PORT = 5212
FILES_PATH = "/www/mycloud/uploads/2/record"
LISTEN_INTERVAL = 60
USERNAME = "*******"
PASSWORD = "*******"
########## 

login_request = "POST /api/v3/user/session HTTP/1.1\r\n"
login_data = '{"userName":"' + USERNAME + '","Password":"' + PASSWORD + '","captchaCode":""}'
login_headers = {
    "Host": f"{SERVER_NAME}",
    "Connection": "keep-alive",
    "Content-Length": f"{len(login_data.encode())}",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76",
    "Content-Type": "application/json",
    "Origin": f"http://{SERVER_NAME}",
    "Referer": f"http://{SERVER_NAME}",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

import_request = "POST /api/v3/admin/task/import HTTP/1.1\r\n"
import_data = '{"uid":2,"policy_id":1,"src":"uploads/2/record","dst":"/record","recursive":true}'
import_headers = {
    "Host":f"{SERVER_NAME}",
    "Connection": "keep-alive",
    "Content-Length": f"{len(import_data.encode())}",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76",
    "Content-Type": "application/json",
    "Origin": f"http://{SERVER_NAME}",
    "Referer": "http://{SERVER_NAME}/admin/file/import",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,ja;q=0.5",
}

prev_files = []
curr_files = []

while True:
    os.system("clear")
    curr_files = os.listdir(FILES_PATH)
    for filename in curr_files:
        if filename not in prev_files:
            recv = send_msg(SERVER_NAME, SERVER_PORT, import_request, import_headers, import_data)
            if '"code":401' in recv:
                recv = send_msg(SERVER_NAME, SERVER_PORT, login_request, login_headers, login_data)
                print(recv)
                for word in recv.split():
                    if "cloudreve-session" in word:
                        import_headers["Cookie"] = f"{word[:-1]}"
                recv = send_msg(SERVER_NAME, SERVER_PORT, import_request, import_headers, import_data)
            break
    prev_files = curr_files
    time.sleep(LISTEN_INTERVAL)