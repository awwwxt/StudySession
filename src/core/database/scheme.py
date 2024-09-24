from config import FONTS

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from random import choice
from os import listdir

DB = declarative_base()

class User(DB):
    __tablename__ = 'users'

    UserID = Column(Integer, primary_key=True)
    Group = Column(String, nullable = True)
    AccessLevel = Column(Integer, nullable = False)
    RegistrationDate = Column(DateTime, nullable = False)
    Banned = Column(Boolean, default = False)
    AuthToken = Column(String, nullable = False)
    PrivateProfile = Column(Boolean, default = False)
    InvitedBy = Column(Integer, nullable = True)
    PromotedBy = Column(Integer, nullable = True)

    EnableExtentedFormatInTimetable = Column(Boolean, default = True)
    EnableTimeInTimetable = Column(Boolean, default = False)
    MailingTime = Column(String, nullable = True) 
    Name = Column(String, nullable = True) 
    EnableImageFormatTimetable = Column(Boolean, default = False)
    FontColorForImage = Column(String, default = "grey")
    BackgroundColorForImage = Column(String, default = "white")
    FontNameForImage = Column(String, default = choice(listdir(FONTS)))
    AlignTextForImage = Column(String, default = "center")

class ChangedLesson(DB):
    __tablename__ = 'changedlessons'
    
    CreationDate = Column(DateTime, primary_key = True)
    LessonDate = Column(String, nullable = False)
    LessonNumber = Column(Integer, nullable = False)
    NewLesson = Column(String, nullable = False)
    Group = Column(String, nullable = False)
    CreatorID = Column(Integer, nullable = False)
    Teacher = Column(String, nullable = True)

class Homework(DB):
    __tablename__ = 'homeworks'

    CreationDate = Column(String, primary_key = True)
    LessonDate = Column(String, nullable = False)
    LessonNumber = Column(Integer, nullable = False)
    Homework = Column(String, nullable = False)
    Group = Column(String, nullable = False)
    CreatorID = Column(Integer, nullable = False)
    Teacher = Column(String, nullable = True)

class InviteKeys(DB):
    __tablename__ = 'invitekeys'
    
    DateOfCreation = Column(DateTime, primary_key = True)
    CreatorID = Column(Integer, nullable = False)
    Key = Column(String, primary_key = True) 
    Role = Column(Integer, nullable = False)

class ShortDays(DB):
    __tablename__ = 'shortdays'

    DateOfCreation = Column(String, primary_key = True)
    CreatorID = Column(Integer, nullable = False)
    Date = Column(String, nullable = False)
    Group = Column(String, nullable = False)
    
class Chat(DB):
    __tablename__ = 'chats'

    creator_id = Column(Integer, primary_key = True)
    chat_id = Column(Integer, primary_key = True)
    link = Column(Integer, nullable = True)
    group = Column(String, nullable = False)
    opened = Column(Boolean, default = False)
    mailing = Column(String, nullable = True)