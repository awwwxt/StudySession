from .validators.gets import GetColors, GetFonts, GetKeys
from .tcp.tcpserver import BaseTCPServer
from .timetables.teachers import TeachersParser
from .timetables.students import StudentsParser
from .tcp.dispatcher import Dispatcher
from .validators.weeks import WeekSearch
from .validators.timetables import *
from .validators.users import *
from .validators.changes import *
from .validators.updates import RequestUpdate
from .validators.chats import *

dispatcher = Dispatcher()