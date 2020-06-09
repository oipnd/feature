"""
该code主要为键盘相关数据的提取
Author: 牛红峰
keycode 为 按键代号
"""
print(__doc__)

from cal_feature import feaEx
import os

def featureGet(modetype,path):
    keyHoldTime = {}
    keyDown_up = {}
    key_dd = {}
    key_uu = {}
    key_ud = {}
    f = open(path)
    keyDownList = []
    keyUpList = []
    keyCollect = []
    for line in f:
        string = line.split(' ')
        if string[0] == modetype:
            if string[1] == 'keydown' and string[2] != '13' and string[2] != '17': # 13 17 is special key
                if not keyCollect:     # Python中，None、空[]、空{}、空()、0等一系列代表空和无的对象会被转换成False ，如果是空的
                    flag = 0
                    for item in range(len(keyCollect)):      # 从不执行
                        if string[2] == list(keyCollect[item].keys())[0]:
                            flag = 1
                    if flag == 0:
                        keyCollect.append({string[2]:string[3][:-1]})
                else:
                    keyCollect.append({string[2]:string[3][:-1]})
        if string[1] =='keyup' or string[1] == 'keyUp' and string[2] != '13' and string[2] != '17':
            flag = -1
            for item in range(len(keyCollect)):
                if string[2] == list(keyCollect[item].keys())[0]:  # 保证down 与up的键是相同的
                    flag = item
            if flag != -1:
                if string[2] != '16' and string[2] != '8':
                    keyDownList.append(keyCollect[flag])
                    keyUpList.append({string[2]:string[3][:-1]})
                keyCode = string[2]                 # code 为按键代号
                if keyCode not in keyHoldTime.keys():
                    keyHoldTime[keyCode] = [int(int(string[3][:-1]) - int(keyCollect[flag][keyCode]))]

                else:
                    keyHoldTime[keyCode].append(int(int(string[3][:-1]) - int(keyCollect[flag][keyCode])))
                del keyCollect[flag]
    f.close()
    getKeyDown_Up(keyDown_up,key_dd,key_uu,key_ud,keyUpList,keyDownList)

    return keyHoldTime,keyDown_up,key_uu,key_dd




def getKeyDown_Up(keyDown_Up,key_dd,key_uu,key_ud,keyUpList,keyDownList):
    flag = 0
    for i in range(len(keyDownList)):
        if list(keyDownList[i].keys())[0] != list(keyUpList[i].keys())[0]:
            flag = 1
            break
    if flag !=1:
        # after down - front up
        for i in range(len(keyDownList) -1 ):
            keyCode_front = list(keyUpList[i].keys(0))[0]
            keyCode_after = list(keyDownList[i + 1].keys())[0]
            listValue = keyCode_front + '_'+keyCode_after
            keyTime = int(int(keyDownList[i+1][keyCode_after]) - int(keyUpList[i][keyCode_front]))
            if listValue not in keyDown_Up.keys():
                if abs(keyTime) < 1000:
                    keyDown_Up[listValue] = [keyTime]
            else:
                if abs(keyTime < 1000):
                    keyDown_Up[listValue].append(keyTime)


        # after up - front up
        for i in range(len(keyUpList) - 1):
            keyCode_front = list(keyUpList[i].keys())[0]
            keyCode_after = list(keyUpList[i+1].keys())[0]
            listValue = keyCode_front + '_' +keyCode_after
            keyTime = int(int(keyUpList[i+1][keyCode_after]) - int(keyUpList[i][keyCode_front]))
            if list not in key_uu.keys():
                if abs(keyTime) < 1000:
                    key_uu[listValue] = [keyTime]
            else:
                if abs(keyTime) < 1000:
                    key_uu[listValue].append(keyTime)
        # down - down
            keyCode_front = list(keyDownList[i].keys())[0]
            keyCode_after = list(keyDownList[i+1].keys())[0]
            listValue = keyCode_front + '_' + keyCode_after
            keyTime = int(int(keyDownList[i+1][keyCode_after]) -  int(keyDownList[i][keyCode_front]))
            if listValue not in key_dd.keys():
                if abs(keyTime) < 1000:
                    key_dd[listValue] = [keyTime]
            else:
                if abs(keyTime) <1000:
                    key_dd[listValue].append(keyTime)
    return keyDown_Up,key_uu,key_dd

def dict2list(dicttime):
    timelist = []
    for item in dicttime.keys():
        for time in dicttime[item]:
            timelist.append(time)
    return timelist

def HumFeaFinal(modetype,ori_path):
    fea = []
    HumanNames = []
    users = os.listdir(ori_path)
    i = 0
    for user in users:
        timepath = ori_path + user  + '\\'
        timelist = os.listdir(timepath)
        for time in timelist:
            txtpath = timepath + time + '\\'
            txtlist = os.listdir(txtpath)
            for txt in txtlist:
                path = txtpath + txt
                i =i + 1
                keyHoldTime,keyDown_Up,key_uu,key_dd = featureGet(modetype,path)
                keyholdtime = dict2list(keyHoldTime)
                keydown_up = dict2list(keyDown_Up)
                key_uu_trans = dict2list(key_uu)
                key_dd_trans = dict2list(key_dd)
                keyholdfea = feaEx.featureEx(keyholdtime)
                keyinterfea = feaEx.featureEx(keydown_up)
                key_uu_fea = feaEx.featureEx(key_uu_trans)
                key_dd_fea = feaEx.featureEx(key_dd_trans)
                featurevector = keyholdfea +keyinterfea + key_uu_fea + key_dd_fea
                fea.append(featurevector)
                HumanNames.append(txt)
    return fea,HumanNames

def BotFeaFinal(modetype,ori_path):
    Botfea = []
    BotNames  =[]
    txtlist = os.listdir(ori_path)
    for txt in txtlist:
        path = ori_path + '\\' + txt
        keyHoldtime,keyDown_up,key_uu,key_dd = featureGet(modetype,path)
        keyholdtime  = dict2list(keyHoldtime)
        keydown_up   = dict2list(keyDown_up)
        key_uu_trans = dict2list(key_uu)
        key_dd_trans = dict2list(key_dd)
        keyholdfea = feaEx.featureEx(keyholdfea)
        keyinterfea = feaEx.featureEx(keydown_up)
        key_uu_fea = feaEx.featureEx(key_uu_trans)
        key_dd_fea = feaEx.featureEx(key_dd_trans)
        featurevector = keyholdtime + keyinterfea + key_uu_fea + key_dd_fea
        Botfea.append(featurevector)
        BotNames.append(txt)
    return Botfea,BotNames








