import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

load_dotenv()

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7696888023:AAEI5zizXTD1xq7xAnwTYC7iET8wOnja4xI")

APP_ID = int(os.environ.get("APP_ID", "17417255"))

API_HASH = os.environ.get("API_HASH", "73d424d9847f968130cd5b41946f7a5d")

CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002415067779"))

OWNER_ID = int(os.environ.get("OWNER_ID", "7086472788"))

PORT = os.environ.get("PORT", "8080")

DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://nitinkumardhundhara:DARKXSIDE78@cluster0.wdive.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "RNK")

FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1002513795136"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "-1002680415419"))
JOIN_REQUEST_ENABLE = os.environ.get("JOIN_REQUEST_ENABLED", True)

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

#start message
START_PIC = os.environ.get("START_PIC","https://wallpapersok.com/images/hd/one-piece-4k-nami-7ohlpm3jletqrctu.jpg")
START_MSG = os.environ.get("START_MESSAGE", "<b>ʙᴀᴋᴀ!!! </b><b>{mention}</b>\n<b>ɪ ᴀᴍ [ɴᴀᴍɪ](t.me/TheNamiRobot) ᴀ ꜰɪʟᴇ ꜱᴛᴏʀᴇ ʙᴏᴛ ᴄʀᴇᴀᴛᴇᴅ ʙʏ [𝘈𝘯𝘪𝘮𝘦𝘔𝘰𝘯𝘵𝘩](t.me/AnimeMonth) ᴛᴏ ꜱʜᴀʀᴇ ᴀɴɪᴍᴇ ᴛᴏ ᴀ ʟᴀʀɢᴇ ɴᴜᴍʙᴇʀ ᴏꜰ ꜰᴀɴꜱ ᴠɪᴀ ꜱᴘᴇᴄɪᴀʟ ʟɪɴᴋꜱ...\n\n🇵​🇴​🇼​🇪​🇷​🇪​🇩​ 🇧​🇾​ [RNK Anime](t.me/RNK_Anime)</b>")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message
FORCE_PIC = os.environ.get("FORCE_PIC","https://wallpapers.com/images/hd/nami-one-piece-3oxrzmms9vf06umc.jpg")
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "<b>ʜᴇʟʟᴏ ᴅᴇᴀʀ {mention}</b>\n\n<b>ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟ ᴡʜɪᴄʜ ᴀʀᴇ ꜱʜᴏᴡɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ꜱᴡᴇᴇᴛ ꜱᴡᴇᴇᴛ ᴀɴɪᴍᴇ.</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "True") == "True" else False

# Auto delete time in seconds.
AUTO_DELETE_TIME = int(os.getenv("AUTO_DELETE_TIME", "0"))
AUTO_DELETE_MSG = os.environ.get("AUTO_DELETE_MSG", "This file will be automatically deleted in {time} seconds. Please ensure you have saved any necessary content before this time.")
AUTO_DEL_SUCCESS_MSG = os.environ.get("AUTO_DEL_SUCCESS_MSG", "Your file has been successfully deleted. Thank you for using our service. ✅")

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "<b>ɢɪᴠᴇ ᴍᴇ ᴏɴᴇ ʙɪʟʟɪᴏɴ ʙᴇʀʀɪᴇꜱ ᴀɴᴅ ɪ ᴡɪʟʟ ꜱᴛᴀʀᴛ ᴡᴏʀᴋɪɴɢ ꜰᴏʀ ʏᴏᴜ... ɴᴇxᴛ ᴏᴡɴᴇʀ</b>"

ADMINS.append(OWNER_ID)
ADMINS.append(1250450587)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
