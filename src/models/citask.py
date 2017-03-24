# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,DateTime,NVARCHAR,Integer,ForeignKey,UnicodeText,SMALLINT
from src.models.database import BaseModel
from datetime import datetime
# import appcicontroller
import time


class JENKINS_TASK(BaseModel):
 
    __tablename__ = 'JENKINS_TASK'
    JENKINS_TASK_ID = Column('JENKINS_TASK_ID', Integer,primary_key=True,nullable=False,autoincrement=True)
    JOB_NAME = Column('JOB_NAME', NVARCHAR(200),nullable = False)
    CODE_REPO_TYPE = Column('CODE_REPO_TYPE', NVARCHAR(300),nullable = False)
    SCMURL = Column('SCMURL', NVARCHAR(600),nullable = False)
    POLL = Column('POLL', NVARCHAR(200),nullable = False)
    SHELL = Column('SHELL', NVARCHAR(500),nullable = False)
    PROGRESSBAR = Column('PROGRESSBAR', NVARCHAR(300),nullable = False)
    STATUS = Column('STATUS', NVARCHAR(300),nullable = False)
    CREATEDATE = Column('CREATEDATE', DateTime,nullable=False)
    UPDATE_TIME = Column('UPDATE_TIME', DateTime,nullable=False)


class JENKINS_CI(BaseModel):
 
    __tablename__ = 'JENKINS_CI'
    JENKINSCIID = Column('JENKINSCIID', Integer,primary_key=True,nullable=False,autoincrement=True)
    JOBNAME = Column('JOBNAME', NVARCHAR(300),nullable = False)
    BUILDID = Column('BUILDID', NVARCHAR(300),nullable = False)
    CREATEDATE = Column('CREATEDATE', DateTime,nullable=False)
    UPDATEDATA = Column('UPDATEDATA', DateTime,nullable=False)
    LOGS = Column('LOGLIST', NVARCHAR(500))        
#     PackageType = Column('packagetype', NVARCHAR(30),nullable = False)

if __name__ == '__main__':
#     getservertaskinfo ()
   print "ok"
     
#     create_database()
   
#     drop_database()