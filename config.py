# INTERVALS
LISTEN_INTERVAL = 30
UPLOAD_INTERVAL = 60
TRANSCODE_INTERVAL = 30

# FORMAT
RECORD_FORMAT = "ts"
TRANSCODE_FORMAT = "mp4"
TIME_FORMAT = "%Y%m%d_%H%M%S"

# PATHS
PATH = "."
CONFIG_PATH = f"{PATH}/config"
RECORD_PATH = f"{PATH}/record"
TEMP_PATH = f"{RECORD_PATH}/temp"
LOG_PATH = f"{PATH}/log"
RECORD_LOG_PATH = f"{LOG_PATH}/record"
TRANS_LOG_PATH = f"{LOG_PATH}/transcode"
UPLOAD_LOG_PATH = f"{LOG_PATH}/upload"
OFFICIAL_SERVERNAME = "124.221.163.165"

# UPLOAD
EXPIRATION = 2 # days

# REQUEST HEADERS
HEADERS = {}
HEADERS["Connection"] = "close"

# API
def TWITCAS_API(room_id):
    return f"https://twitcasting.tv/streamserver.php?target={room_id}&mode=client"
def BILI_API(room_id):
    return f"https://api.live.bilibili.com/room/v1/Room/get_info?room_id={room_id}&from=room"