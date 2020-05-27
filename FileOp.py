# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 17:33:25 2016

@author: Administrator
"""
import os

def ReadDataFromTextFile(FilePath):
    HumanList = os.listdir(FilePath)
    HumanData = []
    NameData = []
    for i in range(len(HumanList)):
        SectionList = os.listdir(FilePath + '\\' + HumanList[i])
        # if SectionList[5] == '6':
        #     HumanPath = FilePath + '\\' + HumanList[i]
        #     each_file = HumanPath + os.sep + SectionList[5]
        #     txtList = os.listdir(each_file)        #修改周次
        for S in SectionList:
            extraStr = '\\' + S
            HumanPath = FilePath + '\\' + HumanList[i]
            each_file = HumanPath + os.sep + S
            txtList = os.listdir(HumanPath + extraStr)

            SingleFileData = []
            SingleName = []
            for j in range(len(txtList)):
                f = open(each_file +os.sep + txtList[j], 'r')
                linesAll = f.readlines()
                f.close()

                SingleFileData.append(linesAll)
                SingleName.append(txtList[j])
            HumanData.append(SingleFileData)    
            NameData.append(SingleName)
    return HumanData, NameData
    
def RenameFileWithSessions(FilePath): 
    HumanList = os.listdir(FilePath)
    for i in range(len(HumanList)):
        SectionList = os.listdir(FilePath + '\\' + HumanList[i])
        for S in SectionList:
            extraStr = '\\' + S
            HumanPath = FilePath + '\\' + HumanList[i]
#            print HumanPath
            
            FileList = os.listdir(HumanPath + extraStr)
            tmp = FileList[0].split('_')
            if tmp[-2] != S:
                for j in range(len(FileList)):
                    tmp = FileList[j].split('_')
                    NameChanged = ''
                    for t in range(len(tmp)-1):
                        NameChanged = NameChanged + tmp[t] + '_'
                    NameChanged = NameChanged + S + '_' +tmp[-1]
                    os.rename(HumanPath + extraStr+ '\\' + FileList[j], HumanPath + extraStr+ '\\' + NameChanged)
if __name__ == '__main__':
    path="D:\data\pc"
    data1,data2=ReadDataFromTextFile(path)
    print(data1)
    print(data2)
