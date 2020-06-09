# -*- coding: utf-8 -*-
'''融合生成人的特征数据，注意工作目录,将人的特征保存为mat格式'''

from cal_feature import MousefeaGet, click2move, FileOp, feaGet
import numpy
import os
import scipy.io as scio

HumDataPath=" "
# #python脚本复杂轨迹按键时间gauss
FileOp.RenameFileWithSessions(HumDataPath)#将txt文件重命名为_1_1格式
##################### 击键特征
ListKeyFeaHuman,ListKeyFeaHumanNames = feaGet.HumFeaFinal(modetype, HumDataPath)
KeyFeaHuman = numpy.array(ListKeyFeaHuman)
KeyFeaHumanNames = numpy.array(ListKeyFeaHumanNames)
print(ListKeyFeaHumanNames)
print(numpy.shape(ListKeyFeaHumanNames))
# print(type(KeyFeaHuman))
# print(len(KeyFeaHuman))
# # print(KeyFeaHuman[0])
print ('击键特征已获取')
####################### 鼠标特征
MouseFeaHuman,ListMouseFeaHumanNames = MousefeaGet.HumanSectionData(HumDataPath)
MouseFeaHumanNames = numpy.array(ListMouseFeaHumanNames)
# print(MouseFeaHumanNames)
# scio.savemat('sample30_d5.mat', {'sample30_d5': MouseFeaHumanNames})
# print(len(MouseFeaHuman))
# print(MouseFeaHuman)
print(type(MouseFeaHuman))
print(len(MouseFeaHuman))
print('人的鼠标特征已获取')
arry =[]
for name in MouseFeaHumanNames.tolist():
  arry.append(KeyFeaHumanNames.tolist().index(name))
arry1=KeyFeaHuman[arry]
aa=numpy.c_[MouseFeaHuman,arry1]
# print(MouseFeaHumanNames)
# print(aa)
# print(len(aa))
# print(numpy.shape(aa))
# print(type(aa))
# print(aa[0])
# print(ListMouseFeaHumanNames[2])

path = r'F:\\paper_old\\data\\HuamanData\\login\\'
users = os.listdir(path)
feature = []

namelist=[]
for user in users:
   timepath= path+user+'\\'
   timelist=os.listdir(timepath)
   for time in timelist:
       txtpath=timepath+time+'\\'

   # if timelist[5] == '6':  #(周次更改地方)
   #     txtpath=timepath+timelist[5]+'\\'

       txtlist=os.listdir(txtpath)
       for txt in txtlist:
           finallist=txtpath+txt
           time,time1,time2 = click2move.click2tomove(finallist)
           fea_fusion = click2move.Statistic_para(time) + click2move.Statistic_para(time1) + click2move.Statistic_para(time2)
           feature.append(fea_fusion)
           namelist.append(txt)
final = numpy.array(feature)
arry2=[]
nn = []
for name in MouseFeaHumanNames.tolist():
    arry2.append(namelist.index(name))
arry3=final[arry2]
finallist=numpy.c_[aa,arry3]
print(numpy.shape(finallist))
scio.savemat(r'F:\pycharm\feature\data_feature\human\h3.mat', {'h3': finallist})


###异常值处理
# idx = numpy.where(numpy.isnan(finallist))
# for i in range(len(idx[0])):
#     finallist[idx[0][i], idx[1][i]] = finallist[~numpy.isnan(finallist[:, idx[1][i]]), idx[1][i]].mean()
# d = []
# # print(finallist[0])
# print(numpy.shape(finallist))
# for i in range(len(finallist)):
#       if '-inf' not in str(finallist[i]): # 读取的数据类型为float64，取数数据时候，数据类型非常关键，否则无法进行判断
#           d.append(finallist[i])
# print(numpy.shape(d))
# scio.savemat('sample30_d5.mat', {'sample30_d5': d})




# print(finallist[2,14])
# scio.savemat('sample5_4.mat', {'human_feature': finallist})
# final = finallist[:,[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]]
# scio.savemat('sample150.mat', {'sample150': finallist})
# d =[]
# for i in range(len(final)):
#       if 'nan' not in str(final[i]): # 读取的数据类型为float64，取数数据时候，数据类型非常关键，否则无法进行判断
#           d.append(final[i])
# print(numpy.shape(d))
# scio.savemat('s6_5.mat', {'s6_5': d})
