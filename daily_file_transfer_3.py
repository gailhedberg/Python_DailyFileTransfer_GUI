#!/usr/bin/end python

# gail hedberg - daily_file_transfer_3.py 
# july 14, 2015 - created 
# july 19, 2015 - version 3 - modified to interact with wx gui - python drill #7
#       modifications to create a database - stores the last file transfer date
#       - also - use last transfer date (not current datestamp) for
#            transfer starting point
#
#       python drill #7
# july 25, 2015 - update for python 3.4

""" daily_file_transfer_db.py copies files from a hard coded source folder to a
hard coded destination folder based on file age. The files must be new or
modified within the past 24 hours.
The 24 hour period is based on the field : last_run on the file_transfer_times
stored in the abc_utility_db."""


import shutil
import os
from os import path
import datetime
from datetime import date, time, timedelta
import abc_utility_db

archived_ctr = 0
ready_to_archive_ctr = 0
src_path = "c:\\users\\gail\\Desktop\\FolderA"
dst_path = "c:\\users\\gail\\Desktop\\FolderB"


def SetSrcPath(path):
    global src_path
    if os.path.exists(path):
        src_path = path
    else: return False


def SetDstPath(path):
    global dst_path
    if os.path.exists(path):
        dst_path = path
    else: return False


def file_has_changed(fname):

    global db_last_transfer_date
    global ready_to_archive_ctr
    
    # get file modified time
    file_m_time = datetime.datetime.fromtimestamp(path.getmtime(fname))
##    print('file time is {}'.format(file_m_time))
##    print('last_trans is {}'.format(db_last_transfer_date))
    
    # use the timestamp from the database abc_utility.db
    #  - if the file_mod_time is later than last_transfer_time,
    #  -  copy this file to the acrhives
    
    if file_m_time > db_last_transfer_date:
        ready_to_archive_ctr = ready_to_archive_ctr + 1
        return True
    else: return False


def GetFileTransferDate():
    global db_last_transfer_date    
    temp  = abc_utility_db.GetFileTransferDate()
##    print("date from db is {}".format(temp))
    db_last_transfer_date = datetime.datetime.strptime(temp, "%Y-%m-%d %H:%M:%S.%f")
##    print('db_last_transfer_date {}'.format(db_last_transfer_date))
    return db_last_transfer_date

    
def UpdateFileTransferDate():
   
    temp = '{}'.format(datetime.datetime.now())
##    print('update timestamp with datetime {}'.format(temp))
    abc_utility_db.UpdateFileTransferDate(temp)

    
def MainLoop():

    global archived_ctr
    global src_path
    global dst_path
    global db_last_transfer_date
    
    archived_ctr = 0

    GetFileTransferDate()

    for fname in os.listdir(src_path):

      src_fname = '{}\{}'.format(src_path, fname)
        
      if file_has_changed(src_fname):    
        dst_fname = '{}\{}'.format(dst_path, fname)
     
        try:
          shutil.copy2(src_fname, dst_path)
          archived_ctr = archived_ctr + 1
##          print('Copying file : {} '.format(src_fname))
##          print('      To loc : {} '.format(dst_fname))
        except IOError as e:
          print('could not open the file: {} '.format(e))
          
    UpdateFileTransferDate()


def PrintResults():
    global ready_to_archive_ctr
    global archived_ctr
     
    print('***   Archive Report for {}   ***'.format(datetime.datetime.now()))
    print('{} files ready for archiving '.format(ready_to_archive_ctr))
    print('{} files archived'.format(archived_ctr))
    print('***   End of Archive Report   ***')


def GetNumberFilesArchived():
    global archived_ctr
    return archived_ctr

def GetLastTransferDate():
    global db_last_transfer_date
    return db_last_transfer_date


if __name__ == "__main__":

    MainLoop()
    PrintResults()
 
  



