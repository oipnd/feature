# # -*- coding: utf-8 -*-
#

import numpy

from cal_feature import FileOp, FileOpBot, CalFeature


def data_top(HumanData, top_num):
    human_data=[]
    for data in HumanData:
        cnt=1
        tmp_data=[]
        it=iter(data)
        for line in it:
            tmp_data.append(line)
            if line.startswith("mouse") and len(line.split())>4:
                cnt+=1
                if cnt>top_num:
                    break
        # 使mouseup和mousedown对应
        tmp_data.append(next(it))
        human_data.append(tmp_data)
    return human_data



def HumanSectionData(FilePath):
    AllUsers, AllNames = FileOp.ReadDataFromTextFile(FilePath)
    HumanData = []
    label_level = []
    for i in range(len(AllUsers)):  # 将Alluser多层变为一层[[],...[]]到[]
        HumanData.extend(AllUsers[i])  # 注意extend和append区别
        label_level.extend(AllNames[i])

    #取文件的前n个点击数据,其中包括最后的点为mouseup采集点
    human_data=data_top(HumanData,2)
    data, label = data_seg(human_data)
    HumanOperating, HumanOpType = CalFeature.DataFormation(data)
    idchosen = numpy.where(HumanOpType == 2)[0]  # np.where()
    # HumanOperatingChosen = [HumanOperating[x] for x in idchosen]  # 链式推导式，n*n*4 ,list
    # HumanNamesChosen = [label_level[x] for x in idchosen]  # 选择符合键鼠完整数据的矩阵
    SectionDataHuman = CalFeature.SectionProc1(HumanOperating)  # 通过mouseup将移动分段,返回一个多个n*4组成的矩阵
    SectionData = CalFeaFromSectionData(SectionDataHuman)
    return SectionData, label


def data_seg(file_data):
    all_data = []
    all_labels = []
    it = iter(file_data)
    for data in it:
        tmp_data = []
        cnt = 0
        start = end = 0
        for line in data:
            if line.startswith("mouse") and cnt <= 4:
                tmp_data.append(line)
                tmp_line = line.split()
                if cnt == 0:
                    start = int(tmp_line[3])
                if cnt == 4:
                    end = int(tmp_line[3])
                    label = end - start
                    all_data.append(tmp_data)
                    all_labels.append(label)
                    cnt=0
                    tmp_data=[]
                if len(tmp_line) > 4:
                    cnt += 1
    return all_data, all_labels


def calExtraFea(inputData):
    allData = []

    num = 0
    num1 = 0
    num2 = 0
    data1 = inputData
    data = []
    data2 = []
    for lines in data1:
        for n in range(4, lines.shape[0] - 8):
            if lines[n, 0] == 2 and lines[n - 1, 0] > 2 and any(lines[n + 1:n + 4, 0] > 2):
                lines[n, 0] = 3
    #            if lines[n,0]==2 and any(lines[n-3:n,0]>2) and any(lines[n+1:n+2,0]>2):
    #                lines[n,0]=3
    for j, item in enumerate(data1):
        fea = []
        feakey2mouse = []
        mouse2click = []
        nn = 0
        #        for i in range(2,item.shape[0]-6):
        #            if item[i,0]==2 and item[i+1,0]>2 and item[i-1,0]>2:
        #                del(item[i,:])
        for i in range(0, item.shape[0] - 8):
            if item[i, 0] == 1:
                nn = 1
            #            if(item[i,0]<3 and (item[i+1,0]==3 and item[i+1,1]!=9) and (item[i+1,1]==17 or how(item[i+1:i+8,0],'than',2,4))):
            #                timeTransition=item[i+1,3]-item[i,3]
            #                fea.append([i,timeTransition])
            if (item[i, 0] < 3 and ((item[i + 1, 0] == 3 and item[i + 1, 1] == 17) or all(item[i + 1:i + 5, 0] > 2))):
                if ((any(item[i - 8:i, 0] < 2) or all(item[i - 8:i, 0] == 2)) and item[
                    i - 1, 0] < 3):  # and (item[i+1,1]!=86 or all(item[i+1:i+4,0]>2))
                    timeTransition = item[i + 1, 3] - item[i, 3]
                    fea.append([i, timeTransition])
            if (item[i, 0] == 3 and item[i, 1] == 9 and all(item[i + 1:i + 4, 0] > 2)):
                fea.append([i, 0])
            if (i < item.shape[0] - 15 and item[i, 0] == 4 and all(item[i + 1:i + 12, 0] < 3) and nn == 1):
                if how(item[i - 5:i, 0], 'than', 2, 2) or item[i, 1] == 17:
                    timekey2mouse = item[i + 1, 3] - item[i, 3]
                    feakey2mouse.append([i, timekey2mouse])
                    nn = 0
            if (item[i, 0] == 4 and item[i, 1] == 9 and (
                    item.shape[0] - i < 5 or how(item[i + 1:i + 8, 0], 'than', 2, 5))):
                nn = 1
                feakey2mouse.append([i, 0])
            if i < item.shape[0] - 15 and item[i, 0] == 4 and nn == 1:
                if all(item[i + 1:i + 15, 0] < 3) and item[i, 1] < 106 and item[i, 1] > 47 and how(item[i - 5:i, 0],
                                                                                                   'less', 3, 1):
                    timekey2mouse = item[i + 1, 3] - item[i, 3]
                    feakey2mouse.append([i, timekey2mouse])
                    nn = 0
        if any(item[-3:, 0] == 4) and how(item[-5:-1, 0], 'than', 2, 2) and (all(item[-3:, 1] != 13)):
            feakey2mouse.append([item.shape[0], 0])
        for i in range(1, item.shape[0]):
            if item[i, 0] == 0 and item[i - 1, 0] == 2:
                if i > item.shape[0] - 20 or (
                        i < item.shape[0] - 25 and all(item[i + 1:i + 20, 0] > 0) and any(item[i + 1:i + 25, 0] > 2)):
                    timemouse2click = item[i, 3] - item[i - 1, 3]
                    mouse2click.append([i, timemouse2click])
            if item[i, 0] == 3 and item[i, 1] == 9:
                mouse2click.append([i, 0])

            #        if len(fea)==3:
        #            allData.append(fea)
        #        else:
        #            allData.append([0,0])
        data.append(feakey2mouse)
        allData.append(fea)
        data2.append(mouse2click)
        if len(fea) == 3:
            num = num + 1
        if len(feakey2mouse) == 3:
            num1 = num1 + 1
        if len(mouse2click) == 4:
            num2 = num2 + 1
    #        else:
    #            print j
    print(num, num1, num2)
    return allData, data, data2


def BotSectionData(modetype, FilePathBot):
    AllBots, BotAllNames = FileOpBot.ReadDataFromTextFile(FilePathBot)
    BotData = []
    BotNames = []
    for i in range(len(AllBots)):
        BotData.extend(AllBots[i])
        BotNames.extend(BotAllNames[i])
    BotOperating, BotOpType = CalFeature.DataFormation(BotData)
    BotOperatingChosen = BotOperating
    BotNamesChosen = BotNames
    SectionDataBot = CalFeature.SectionProc(BotOperatingChosen)
    SectionData = CalFeaFromSectionData(SectionDataBot)
    return SectionData, BotNamesChosen


def CalFeaFromSectionData(SectionData):  # n*n*n*4
    DataProc = SectionData
    # 修改为16个特征
    featureHuman = numpy.zeros([len(DataProc), 28])
    feature_new = numpy.zeros([len(DataProc), 12])
    #    features
    feaRatioStrai = numpy.zeros([len(DataProc), 1])
    feaVelocVar = numpy.zeros([len(DataProc), 2])
    #    feaAccVar = numpy.zeros([len(DataProc),1])
    feaMovementEfficiency = numpy.zeros([len(DataProc), 1])
    feaMovementTime = numpy.zeros([len(DataProc), 1])
    featime2dict = numpy.zeros([len(DataProc), 1])
    feav252v75 = numpy.zeros([len(DataProc), 11])
    # Ent = numpy.zeros([len(DataProc),1])
    #    acclerate=[]
    for i in range(len(DataProc)):
        #        acclerate1=[]
        time2dict = []
        RatioStraiIndividual = []
        q2575 = []
        VelocityVarIndividual = []
        feature_new0 = []

        #        AccVarIndividual = []
        #        MoveDistanceIndividual = []
        MoveEfficiencyIndividual = []
        for j in range(len(DataProc[i])):
            SingleSectionData = DataProc[i][j]
            CurV = CalFeature.CalCurvature(SingleSectionData)  # 计算相邻三点夹角余玹值
            Ent = CalFeature.CalEntrop(SingleSectionData)
            feature_new_vec = CalFeature.Cal2Point_vec(SingleSectionData)
            ##增加熵
            ent = numpy.mean(Ent)
            meancos = numpy.mean(CurV)
            stdcos = numpy.std(CurV)
            varcos = numpy.var(CurV)
            discos = meancos / varcos
            RBT = CalFeature.RatioBelowTh(CurV, -0.95)  # 夹角余玹值小于-0.95所占比例
            if RBT == 'none':
                pass
            else:
                RatioStraiIndividual.append(RBT)
            MEfficiency, time, time2 = \
                CalFeature.CalMovementEfficiency(SingleSectionData)  # 返回移动效率和时间
            if feature_new_vec == 'none':
                pass
            else:
                feature_new0.append(feature_new_vec)
            if MEfficiency == 'none':
                pass
            else:
                time2dict.append(time2)
                if (MEfficiency < 10):
                    MoveEfficiencyIndividual.append(MEfficiency)  # 起始点距离/每两点距离和
            #
            VeloSeries, timemean, timestd, Dictmean, num = CalFeature.GetVeloSeries(
                SingleSectionData)  # np.sum(),axis=1,按行想加，没有就全部加在一起 ，返回速度序列
            Vvari, v25, v75 = CalFeature.CalVeloVariation(VeloSeries)  # 两个元素矩阵，返回速度序列前一半和后一半各自的标准差/平均值
            if Vvari == 'none':
                pass  # if，pass
            else:
                VelocityVarIndividual.append(Vvari)
                # 增添ent
                q2575.append([v25, v75, timemean, timestd, Dictmean, num, meancos, stdcos, varcos, discos, ent])
            # if feature_new0 == 'none':
            #     pass                   #if，pass
            # else:
            #     VelocityVarIndividual.append(Vvari)
            #     # 增添ent
            #     q2575.append([v25,v75,timemean,timestd,Dictmean,num,meancos,stdcos,varcos,discos,ent])
        feav252v75[i, :] = numpy.mean(q2575, 0)
        featime2dict[i] = numpy.mean(time2dict, 0)  # 单位时间走的距离
        feaRatioStrai[i] = numpy.mean(RatioStraiIndividual, 0)  # 余弦比例
        feaVelocVar[i, :] = numpy.mean(VelocityVarIndividual, 0)  # 前后半速度稳定性
        #        feaAccVar[i] = numpy.mean(AccVarIndividual,0)#加速度平均值
        feaMovementEfficiency[i] = numpy.mean(MoveEfficiencyIndividual, 0)  # 移动效率
        feature_new[i] = numpy.mean(feature_new0, 0)

    featureHuman[:, 0:1] = feaRatioStrai
    featureHuman[:, 1:3] = feaVelocVar
    featureHuman[:, 3:4] = featime2dict
    #    featureHuman[:,3:4] = feaMovementEfficiency
    featureHuman[:, 4:5] = feaMovementEfficiency  # 每两点之间距离/直线距离
    #    featureHuman[:,5:6] = feaMovementTime
    featureHuman[:, 5:16] = feav252v75
    featureHuman[:, 16:28] = feature_new
    # featureHuman[:,15] = ent
    return featureHuman


def all(iterable):
    for element in iterable:
        if not element:
            return False
    return True


def any(iterable):
    for element in iterable:
        if element:
            return True
    return False


def how(listType, t, n, m):
    num = 0
    for item in listType:
        if t == 'less':
            if item < n:
                num = num + 1
        if t == 'than':
            if item > n:
                num = num + 1
    if num > m:
        return True
    else:
        return False


if __name__ == '__main__':
    a, b = HumanSectionData("D:\datatest\pc")
    print(a)
    print(b)
    print(len(a))
    print(len(b))
