from enum import unique
from sqlalchemy.orm import backref, relationship
from sqlalchemy import ForeignKey
from database import BaseDBMode
from datetime import datetime
from sqlalchemy import Column,String,DateTime,Integer
from sqlalchemy.orm import relationship


class User(BaseDBMode):
    __tablename__='User'
    id=Column(Integer)
    uid=Column(String(20),primary_key=True,nullable=False)
    name=Column(String(20),unique=True)
    nickname=Column(String(20))
    email=Column(String(50))
    passwords=Column(String(30))
    registertime=Column(DateTime,default=datetime.now())
    lastlogin=Column(DateTime)

class Photo(BaseDBMode):
    __tablename__='Photo'
    pid=Column(String,primary_key=True,nullable=False)
    description=Column(String)
    url=Column(String)
    height=Column(Integer)
    width=Column(Integer)
    size=Column(Integer)
    star=Column(Integer)
    downloadurl=Column(Integer)
    uploadtime=Column(DateTime,default=datetime.now())
    ownerid=Column(String,ForeignKey('User.uid'))
    owner=relationship('User',backref='photos')
    albumid=Column(String,ForeignKey('Album.aid'))
    album=relationship('Album',backref='photoes_of_album')

class Album(BaseDBMode):
    __tablename__='Album'
    aid=Column(String,primary_key=True,nullable=False)
    thumbnailurl=Column(String)
    albumname=Column(String)
    description=Column(String)
    ownerid=Column(String,ForeignKey('User.uid'))
    owner=relationship('User',backref='albums')
    amount=Column(Integer)

    
    