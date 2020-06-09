# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 14:40:26 2016

@author: Administrator
"""

import os

def ReadDataFromTextFile(FilePath):
    HumanList = os.listdir(FilePath)    
    HumanData = []
    NameData = []
    extraStr = ''
    for i in range(len(HumanList)): 
        f = open(FilePath + extraStr + '\\' + HumanList[i], 'r')
        linesAll = f.readlines()
        f.close()
        SingleFileData = []
        SingleName = []
        SingleFileData.append(linesAll)
        SingleName.append(HumanList[i])
        HumanData.append(SingleFileData)    
        NameData.append(SingleName)
    return HumanData, NameData