# -*- coding: utf-8 -*-
"""
Created on Sat Dec 03 20:53:21 2016
# 键盘相关数据的提取
@author: Administrator
"""

from cal_feature import feaEx
import os


def getKeyDown_Up(keyDown_Up,key_dd,key_uu,key_ud,keyUpList,keyDownList):
    flag=0
    for i in range(len(keyDownList)):
        if list(keyDownList[i].keys())[0] != list(keyUpList[i].keys())[0]:
            flag=1
            break    
    if flag!=1:
        # after down - front up
        for i in range(len(keyDownList)-1):
            keyCode_front=list(keyUpList[i].keys())[0]
            keyCode_after=list(keyDownList[i+1].keys())[0]
            listValue=keyCode_front+'_'+keyCode_after
            keyTime=int(int(keyDownList[i+1][keyCode_after])-int(keyUpList[i][keyCode_front]))
            if(listValue not in keyDown_Up.keys()):
                if abs(keyTime)<1000:
                    keyDown_Up[listValue]=[keyTime]
            else:
                if abs(keyTime)<1000:
                    keyDown_Up[listValue].append(keyTime)


        # after up - front down
        for i in range(len(keyUpList)-1):
            keyCode_front=list(keyDownList[i].keys())[0]
            keyCode_after=list(keyUpList[i+1].keys())[0]
            listValue=keyCode_front+'_'+keyCode_after
            keyTime=int(int(keyUpList[i+1][keyCode_after])-int(keyDownList[i][keyCode_front]))
            if(listValue not in key_ud.keys()):
                if abs(keyTime)<1000:
                    key_ud[listValue]=[keyTime]
            else:
                if abs(keyTime)<1000:
                    key_ud[listValue].append(keyTime)

        #  after up - front up
        for i in range(len(keyUpList)-1):
            keyCode_front = list(keyUpList[i].keys())[0]
            keyCode_after = list(keyUpList[i+1].keys())[0]
            listValue = keyCode_front+'_'+keyCode_after

            keyTime = int(int(keyUpList[i+1][keyCode_after])-int(keyUpList[i][keyCode_front]))
            if listValue not in key_uu.keys():
                if abs(keyTime) < 1000:
                    key_uu[listValue] = [keyTime]
            else:
                if abs(keyTime) < 1000:
                    key_uu[listValue].append(keyTime)

        #     down -down
        for i in range(len(keyDownList)-1):
            keyCode_front = list(keyDownList[i].keys())[0]
            keyCode_after = list(keyDownList[i+1].keys())[0]
            listValue = keyCode_front + '_' +keyCode_after
#            print listValue
            keyTime = int(int(keyDownList[i+1][keyCode_after])-int(keyDownList[i][keyCode_front]))
            if listValue not in key_dd.keys():
                if abs(keyTime) < 1000:
                    key_dd[listValue] = [keyTime]
            else:
                if abs(keyTime) < 1000:
                    key_dd[listValue].append(keyTime)

    return keyDown_Up,key_ud,key_uu, key_dd




def featureGet(modetype,path):
    
    keyHoldTime={}
    keyDown_Up={}
    key_dd={}
    key_uu={}
    key_ud={}
    f=open(path)
    keyDownList = []
    keyUpList = []
    keyCollect = []
    for line in f:
        String=line.split(' ')
        if String[0] == modetype:
            if String[1] == 'keydown' and String[2] != '13' and String[2] != '17' :#enter键 ,7 13 为特殊键
                if not keyCollect:                                     # keyCollect 为记录down 数据
                    flag=0
                    for item in range(len(keyCollect)):
                        if String[2] == list(keyCollect[item].keys())[0]:
                            flag = 1
                    if flag == 0:
                        keyCollect.append({String[2]:String[3][:-1]})   
#                        print '-----'      
                else:
                    keyCollect.append({String[2]:String[3][:-1]})    # 有换行键
#                    print 'a'
            if (String[1] == 'keyup' or String[1] == 'keyUp') and String[2] != '13' and String[2] != '17':#string类型加引号
                flag = -1
                for item in range(len(keyCollect)):
                    if String[2] == list(keyCollect[item].keys())[0]:  # 第item个字典的，第一个键值
                        flag = item
                if flag != -1:
                    if String[2] != 16 and String[2] != 8:
                        keyDownList.append(keyCollect[flag])    
                        keyUpList.append({String[2]:String[3][:-1]})
                    keyCode = String[2]             # keycode为按键代码
                    if keyCode not in keyHoldTime.keys():
                        keyHoldTime[keyCode]=[int(int(String[3][:-1])-int(keyCollect[flag][keyCode]))]
#
                    else:
                        keyHoldTime[keyCode].append(int(int(String[3][:-1])-int(keyCollect[flag][keyCode])))
#
                    del keyCollect[flag]   
#
    f.close()  
                
    getKeyDown_Up(keyDown_Up,key_dd,key_uu,key_ud,keyUpList,keyDownList)
    return  keyHoldTime,keyDown_Up,key_uu, key_dd,key_ud
    
def dict2list(dicttime):
    timelist=[]
    for item in dicttime.keys():
        for time in dicttime[item]:
            timelist.append(time)
    return timelist

def HumFeaFinal(modetype,ori_path):
    fea=[]
    HumanNames = []
    users=os.listdir(ori_path)
    i=0
    for user in users:
        timepath=ori_path+user+'\\'
        timelist=os.listdir(timepath)
        for time in timelist:
            txtpath=timepath+time+'\\'
        #修改周次的地方
        # if timelist[5] == '6':
        #     txtpath=timepath+timelist[5]+'\\'


            txtlist=os.listdir(txtpath)
            for txt in txtlist:
                path=txtpath+txt
                i=i+1
                keyHoldTime,keyDown_Up,key_uu,key_dd,key_ud=featureGet(modetype,path)
                keyholdtime=dict2list(keyHoldTime)
                keydown_up=dict2list(keyDown_Up)
                key_uu_trans = dict2list(key_uu)
                key_dd_trans = dict2list(key_dd)
                key_ud_trans = dict2list(key_ud)
                keyholdfea  = feaEx.featureEx(keyholdtime)
                keyinterfea = feaEx.featureEx(keydown_up)
                key_uu_fea  = feaEx.featureEx(key_uu_trans)
                key_dd_fea  = feaEx.featureEx(key_dd_trans)
                key_ud_fea  = feaEx.featureEx(key_ud_trans)
                featurevector=keyholdfea+keyinterfea + key_uu_fea +key_dd_fea +key_ud_fea
                fea.append(featurevector)
                HumanNames.append(txt)
    return fea,HumanNames
    
def BotFeaFinal(modetype,ori_path):
    

    Botfea=[]
    BotNames = []
    txtlist=os.listdir(ori_path)

    for txt in txtlist:

        path=ori_path+'\\'+txt
        keyHoldTime, keyDown_Up, key_uu, key_dd,key_ud=featureGet(modetype,path)  # 这个时间段是字典
        keyholdtime = dict2list(keyHoldTime)
        keydown_up = dict2list(keyDown_Up)
        key_uu_trans = dict2list(key_uu)
        key_dd_trans = dict2list(key_dd)
        key_ud_trans = dict2list(key_ud)

        keyholdfea= feaEx.featureEx(keyholdtime)
        keyinterfea= feaEx.featureEx(keydown_up)
        key_uu_fea = feaEx.featureEx(key_uu_trans)
        key_dd_fea = feaEx.featureEx(key_dd_trans)
        key_ud_fea = feaEx.featureEx(key_ud_trans)


#        specialfea=feaEx.specialfeaEx(keyHoldTime,keyDown_Up)
#        featurevector=specialfea
        featurevector=keyholdfea+keyinterfea + key_uu_fea + key_dd_fea +key_ud_fea
        Botfea.append(featurevector)
        BotNames.append(txt)        

    return Botfea,BotNames
      

# if __name__ == '__main__':
#     modetype='login'
#     a,b,c=HumFeaFinal('login','F:\\paper\\data\\HuamanData\\'+modetype+'\\')
#     HumanPath=r'F:\paper\data\HuamanData\testdata\2150300072\1\2150300072_1_1.txt'
#     keyHoldTime,keyDown_Up,key_uu,key_dd=featureGet(modetype,HumanPath)
#     print(type(key_dd))
#     print(key_dd)

