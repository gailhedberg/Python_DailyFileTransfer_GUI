#!/usr/bin/end python
from __future__ import unicode_literals

# gail hedberg - abc_utility_db.py
# july 19, 2015 - created
# 
# python drill #7

""" abc_utility_db.py  provides sqlite3 database access functions for the
abc_utility_db. this database was created for use with the file transfer python
drills.
"""

import sqlite3


def GetFileTransferDate():

    db = sqlite3.connect('abc_utility.db')
    cursor = db.execute("SELECT ft_timestamp FROM file_transfer_info ORDER BY ID DESC")
    row = cursor.fetchone()
    temp = str(row[0])
    #print(temp)
    db.close()
    return temp
    
def UpdateFileTransferDate(dt_time):
    print('in update utility - time is {}'.format(dt_time))

    db = sqlite3.connect('abc_utility.db')
    sql = "UPDATE file_transfer_info SET ft_timestamp = '{}'".format(dt_time)
    print( sql)
    db.execute(sql)
    db.commit()
    db.close()
    
#GetFileTransferDate()




        
        
