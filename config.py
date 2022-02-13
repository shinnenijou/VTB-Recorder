# INTERVALS
LISTEN_INTERVAL = 30
UPLOAD_INTERVAL = 60
TRANSCODE_INTERVAL = 30

# FORMAT
RECORD_FORMAT = "ts"
TRANSCODE_FORMAT = "mp4"

# PATHS
PATH = "."
CONFIG_PATH = f"{PATH}/config"
RECORD_PATH = f"{PATH}/temp/record"
ENCODE_PATH = f"{PATH}/temp/encode"
LOG_PATH = f"{PATH}/log"
COPIED_PATH = f"{PATH}/temp/copied"
DRIVE = "shinnen:Record_Files"

# REQUEST HEADERS
HEADERS = {}
HEADERS["Connection"] = "close"

# API
def TWITCAS_API(room_id):
    return f"https://twitcasting.tv/streamserver.php?target={room_id}&mode=client"
def BILI_API(room_id):
    return f"https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}&from=room"