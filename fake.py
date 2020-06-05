import os
import random
import time
from datetime import datetime


def MkDir():
    path = 'C:\\Users\\lanoipd\\Desktop\\feature\\data\\datas'#创建文件路径
    i = 0
    for i in range(200): #创建文件个数
        file_name = path + str(i)
        os.mkdir(file_name)
        i=i+1
        file_name_child = file_name + "/left_colorimages"
        os.mkdir(file_name_child)


def MkDir2():
    dirs = []
    path2='data/ '
    for dir in dirs:
        file_name = path2 + str(dir)
        os.mkdir(file_name)



def strTimeProp(start, end, prop, frmt):
    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))
    ptime = stime + prop * (etime - stime)
    return int(ptime)

def randomTimestamp(start, end, frmt='%Y-%m-%d %H:%M:%S'):
    return strTimeProp(start, end, random.random(), frmt)

def randomDate(start, end, frmt='%Y-%m-%d %H:%M:%S'):
    return time.strftime(frmt, time.localtime(strTimeProp(start, end, random.random(), frmt)))

def randomTimestampList(start, end, n, frmt='%Y-%m-%d %H:%M:%S'):
    return [randomTimestamp(start, end, frmt) for _ in range(n)]

def randomDateList(start, end, n, frmt='%Y-%m-%d %H:%M:%S'):
    return [randomDate(start, end, frmt) for _ in range(n)]



if __name__ == '__main__':


    # start = '2018-06-02 12:12:12'
    # end = '2018-11-01 00:00:00'
    # lenth = 10
    # print(randomTimestamp(start, end))
    # print(randomDate(start, end))
    # print(randomTimestampList(start, end, lenth))
    # print(randomDateList(start, end, lenth))
    MkDir()
