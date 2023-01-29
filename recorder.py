import config
import json
import os
import requests
from loguru import logger
import time
import utils
from abc import ABCMeta, abstractmethod

class Recorder(metaclass = ABCMeta):
    __instance = None

    def __new__(cls, streamer_config):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, streamer_config: str) -> None:

        self.__streamer = streamer_config["OFFICIAL_NAME"]
        self.__url = streamer_config["URL"].strip()
        self.__type = utils.get_type(self.__url)
        self.__id = self.__url[self.__url.rfind('/') + 1:]
        self.__record_path = f"{config.RECORD_PATH}/{self.__streamer}"
        self.__log_path = f"{config.LOG_PATH}/{self.__streamer}"
        self.__api = utils.get_api(self.__type, self.__id)

        self.__logger = logger
        self.__logger.add(f"{self.__log_path}" + "/runtime_{time}.log", encoding='utf-8',
                          rotation='1 week', retention='1 month')

        utils.Mkdir(self.__record_path)
        utils.Mkdir(self.__log_path)

    def get_streamer(self) -> str:
        return self.__streamer

    def get_url(self) -> str:
        return self.__url

    def get_record_path(self) -> str:
        return self.__record_path

    def get_log_path(self) -> str:
        return self.__log_path

    def listen(self) -> str:
        while True:
            try:
                resp = requests.get(self.__api, config.HEADERS)
            except (requests.ConnectTimeout, requests.ConnectionError) as e:
                self.__logger.error(f"Requests Connection Error: {str(e)}")
                time.sleep(config.LISTEN_INTERVAL)
                continue

            if resp.status_code != 200:
                self.__logger.error(
                    f"Requests Response Error, status code: {resp.status_code}")
                time.sleep(config.LISTEN_INTERVAL)
                continue

            if not resp.text:
                self.__logger.error(f"Requests Response Error, no text")
                time.sleep(config.LISTEN_INTERVAL)
                continue

            live_info = json.loads(resp.text)
            if not self.check_resp(live_info):
                self.__logger.error("Response body error")
                time.sleep(config.LISTEN_INTERVAL)
                continue

            status = self.get_live_status(live_info)
            title = self.get_live_title(live_info)
            if status == utils.StreamStatus.online:
                self.__logger.info(f"Stream Starting: {self.__streamer}")
                return title
            
            time.sleep(config.LISTEN_INTERVAL)

    def record(self, path) -> None:
        self.__logger.info(f"Start to record the stream: {self.__streamer}")
        options = ['streamlink', self.__url, 'best',
                   '-o', path]
        self.add_options(options)
        os.system(' '.join(option for option in options))

    @abstractmethod
    def check_resp(self, body) -> bool:
        pass

    @abstractmethod
    def get_live_status(self, body) -> utils.StreamStatus:
        pass

    @abstractmethod
    def get_live_title(self, body) -> str:
        pass

    @abstractmethod
    def add_options(self, options:list) -> None:
        pass

class BiliRecorder(Recorder):

    def check_resp(self, body):
        if 'data' not in body:
            return False

        return True

    def get_live_status(self, body):
        if body['data']['live_status'] == 1:
            return utils.StreamStatus.online
        
        return utils.StreamStatus.offline

    def get_live_title(self, body):
        return body['data']['title'].replace(' ', '_')

    def add_options(self, options: list):
        pass

class TwiCasRecorder(Recorder):

    def __init__(self, streamer_config: str) -> None:
        super().__init__(streamer_config)
        self.__password = streamer_config["PASSWORD"]

    def check_resp(self, body):
        if 'movie' not in body:
            return False

        return True

    def get_live_status(self, body):
        if body['movie']['live'] == 1:
            return utils.StreamStatus.online
        
        return utils.StreamStatus.offline

    def get_live_title(self, body):
        return ''

    def add_options(self, options: list):
        if not self.__password:
            return
        
        options.insert(2, "--twitcasting-password")
        options.insert(3, self.__password)

def create_recorder(config) -> Recorder:
    stream_type = utils.get_type(config['URL'])
    return recorder_map[stream_type](config)

recorder_map = {
    utils.StreamType.none: None,
    utils.StreamType.bilibili: BiliRecorder,
    utils.StreamType.twitcast: TwiCasRecorder
}