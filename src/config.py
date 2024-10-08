from string import ascii_letters, ascii_lowercase, ascii_uppercase
from datetime import datetime

from loguru import logger

DefaultTimeLessons = (
    "8.30 - 10.05",
    "10.15 - 11.50",
    "12.20 - 13.55",
    "14.10 - 15.45",
    "15.55 - 17.30",
    "17.40 - 19.15"
    )

ShortTimeLessons = (
    "8.30 - 9.15",
    "9.20 - 10.05",
    "11.15 - 11.50",
    "12.20 - 13.05",
    "13.10 - 13.55",
    "14.10 - 14.55",
    "15.00 - 15.45"
)

Days = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота"
}

LessonCells = (
    (11, 15, 19, 23, 27, 31),
    (36, 40, 44, 48, 52, 56), 
    (61, 65, 69, 73, 77, 81),
    (86, 90, 94, 98, 102, 106), 
    (111, 115, 119, 123, 127, 131), 
    (136, 140, 144, 148, 152, 156)
)

AccessLevels = list(range(5))

StartDate = datetime(year=2024, month=2, day=19) 

DATABASE = ".files/ssb/database.sqlite"
TIMETABLES = ".files/ssb/"
IMAGES = ".files/images/"
FONTS = ".files/fonts/"
TEMP = ".files/temp/"
LOGGER = ".files/ssb/ssb.log"
KEYLIST = ascii_letters + ascii_lowercase + ascii_uppercase
CELLLIST = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
KEYS = ".files/keys/"

DefaultCacheSize = 512
Cache = 64
TimetablesCache = 512
BordersCache = 1024
TeacherCache = 256
LowLevelCache = 8 
DDoSCache = 1024 
StundetsBuildCache = 64
TeachersBuildCache = StundetsBuildCache / 4

LOGS_SIZE = "10MB"

HTTP_TIMEOUT = 5.0

X, Y = [10 for _ in range(2)]
SCALING_Y, SCALING_X = 25, 10

TCP_PORT = 9999
TCP_IP = "127.0.0.1"
MAX_BUFFER_LENGHT = 8196

MAX_TEACHER_NAME_LEN = 20
MAX_TEACHER_NAME_UNIQUE_LEN = MAX_TEACHER_NAME_LEN - 2
MIN_TEACHER_NAME_LEN = 5
MAX_LESSON_LEN = 20
MIN_LESSON_LEN = 3

MAX_GROUP_LEN = 8
MIN_GROUP_LEN = 3

DEFAULT_BUFF_SIZE = 6

ROW1 = 11
ROW2 = 12
ROW3 = 13
ROW4 = 14
ROW5 = 15

ALLOWED_ALIGNS = "right", "left", "center"

TIMES = "7.00", "21.00", None

NAMES_TIMETABLE_SOURCE = {
    "s.xls": map(lambda name: f"bolshoe-raspisanie-{name}", ("s", "c")),
    "p.xls": ("bolshoe-raspisanie-p", ),
    "uchilishhe.xls": ("bolshoe-raspisanie-uchilishhe", )
}

MAX_DOWNLOAD_ATTEMPS = 3

MAX_ATTEMPS = 3

APITOKEN = ""

logger.add(
    sink = LOGGER,
    level = "INFO",
    format = "{time:MMMM D, YYYY > HH:mm:ss} | <{level}> x <{message}>",
    rotation = LOGS_SIZE
)