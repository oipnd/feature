import MousefeaGet
import numpy
import feaGet
import os
import click2move
import scipy.io as sio
# BotDataPath= r'F:\\paper\\data\\bot\\login\\rawbotdata\\weiang1231\\' # 机器数据必须到txt文件之前
modetype = 'login'
botfeat =[]
path = r'F:\paper_old\data\bot\login\rawbotdata\\'
userlist = os.listdir(path)
for user in userlist:
    Botdatapath = path +user + '\\'
    ListKeyFeaBot,ListKeyFeaBotNames = feaGet.BotFeaFinal(modetype,Botdatapath)
    KeyFeaBot = numpy.array(ListKeyFeaBot)
    KeyFeaBotNames = numpy.array(ListKeyFeaBotNames)
    MouseFeaBot,ListMouseFeaBotNames = MousefeaGet.BotSectionData(modetype,Botdatapath)
    MouseFeaBotNames = numpy.array(ListMouseFeaBotNames)
    botfea = list(numpy.concatenate([MouseFeaBot,KeyFeaBot],axis= 1))
    # print(botfea)
    botfeat.extend(botfea)
print(numpy.shape(botfeat))
# sio.savemat(r'F:\pycharm\feature\data_feature\bot\b_24.mat', {'b_24':botfea})
#
#  print(botfeat)
path = r'F:\paper_old\data\bot\login\rawbotdata\\'
users=os.listdir(path)
feature = []
for user in users:
    txtpath= path+user+'\\'
    # timelist=os.listdir(timepath)
    # for time in timelist:
    # if timelist[0] == '1':
    # txtpath=timepath+timelist+'\\'
        # txtpath=timepath+time+'\\'
    txtlist=os.listdir(txtpath)
    for txt in txtlist:
        finallist=txtpath+txt
        time,time1,time2= click2move.click2tomove(finallist)
        fea_fusion = click2move.Statistic_para(time) + click2move.Statistic_para(time1)+click2move.Statistic_para(time2)
        fea = numpy.array(feature.append(fea_fusion))
final = numpy.array(feature)
#
ff = numpy.concatenate([botfeat,final],axis= 1)
# print(ff)
sio.savemat('bot_gau.mat', {'bot_gau':ff})
print(numpy.shape(ff))
sio.savemat(r'F:\pycharm\feature\data_feature\bot\b_24.mat', {'b_24':ff})
# # print(ff[2])
# # d =[]
# print(numpy.shape(ff))
# for i in range(len(ff)):
#     if 'nan' not in str(ff[i]): # 读取的
# 数据类型为float64，取数数据时候，数据类型非常关键，否则无法进行判断
#         d.append(ff[i])
# print(numpy.shape(d))
# sio.savemat('bot_t.mat', {'bot_t':ff})
# numpy.savetxt('bot.csv', d, delimiter = ',')



