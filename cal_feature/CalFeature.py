# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 20:45:00 2016
#鼠标
@author: Administrator
"""
import math
import numpy
import scipy.stats as scit


def CalCurvature(Txtdata):
    TracePos = Txtdata[Txtdata[:, 0] == 2]
    if len(TracePos) < 3:
        CurvMtr = 'none'
    else:
        VecCur = TracePos[1:, 1:3] - TracePos[:-1, 1:3]
        CurvMtr = []
        InnerPr = numpy.zeros(numpy.size(VecCur, 0) - 1)
        VecMod = numpy.zeros(numpy.size(VecCur, 0) - 1)
        for i in range(numpy.size(VecCur, 0) - 1):
            InnerPr[i] = numpy.dot(-VecCur[i, :], VecCur[i + 1, :])
            VecMod[i] = numpy.sqrt(sum(VecCur[i, :] ** 2)) * numpy.sqrt(sum(VecCur[i + 1, :] ** 2))
            VecMod[VecMod == 0] = 1
        CurvMtr = InnerPr / VecMod
    return CurvMtr


def CalEntrop(Txtdata):
    TracePos = Txtdata[Txtdata[:, 0] == 2]
    if len(TracePos) < 3:
        ent = 'none'
    else:
        TimeSeries = list(TracePos[1:, 3] - TracePos[:-1, 3])
        length = len(TimeSeries)
        time_set = set(TimeSeries)
        ent = 0
        for i in time_set:
            p = TimeSeries.count(i) / length
            ent -= p * math.log2(p)
        return ent


def Cal2Point_vec(Txtdata):
    TracePos = Txtdata[Txtdata[:, 0] == 2]
    if len(TracePos) < 3:
        vec_mat = 'none'
    else:
        TimeSeries = list(TracePos[1:, 3] - TracePos[:-1, 3])
        dis_2point = numpy.array(TracePos[1:, 1:3] - TracePos[:-1, 1:3])
        dis_mat = numpy.sum(dis_2point ** 2, axis=1)
        vec = dis_mat / TimeSeries
        vec_mat = [numpy.mean(vec), numpy.std(vec), numpy.var(vec), numpy.median(vec), numpy.min(vec), numpy.max(vec),
                   numpy.max(vec) - numpy.min(vec), numpy.std(vec) / numpy.mean(vec), scit.kurtosis(vec),
                   scit.skew(vec), scit.kurtosis(dis_mat), scit.skew(dis_mat)]

        return vec_mat


def RatioBelowTh(Vec, th):
    if Vec == 'none':
        RBT = 'none'
    else:
        RBT = len(numpy.where(Vec < th)[0]) / float(len(Vec))
    return RBT


def GetVeloSeries(Txtdata):
    TracePos = Txtdata[Txtdata[:, 0] < 3]
    if len(TracePos) < 3:
        VeSer = 'none'
        timemean = 'none'
        timestd = 'none'
    else:
        DistSeries = numpy.sqrt(numpy.sum((TracePos[1:, 1:3] - TracePos[:-1, 1:3]) ** 2, 1))
        Dictmean = numpy.mean(DistSeries)
        TimeSeries = TracePos[1:, 3] - TracePos[:-1, 3]
        TimeSeries[TimeSeries == 0] = 1
        VeSer = DistSeries / TimeSeries
        TimeSeries = TimeSeries[TimeSeries[:] < 100]
        timemean = numpy.mean(TimeSeries)
        timestd = numpy.std(TimeSeries)
        move = numpy.where(TracePos[:, 0] == 2)[0]
        dis = TracePos[move[0], 1:3] - TracePos[move[-1], 1:3]
        a = numpy.sqrt(numpy.sum((dis) ** 2, 0))
        #        print a
        num = a / len(move)

    return (VeSer, timemean, timestd, Dictmean, num)


def CalAccelaration(Txtdata):
    pass
    TracePos = Txtdata[Txtdata[:, 0] < 3]
    if len(TracePos) < 3:
        AccSer = 'none'
    else:
        DistSeries = numpy.sqrt(numpy.sum((TracePos[1:, 1:3] - TracePos[:-1, 1:3]) ** 2, 1))
        TimeSeries = TracePos[1:, 3] - TracePos[:-1, 3]
        TimeSeries[TimeSeries == 0] = 1
        TTimeSeries = TimeSeries[1:] - TimeSeries[:-1]
        TTimeSeries[TTimeSeries == 0] = 1
        VeSer = DistSeries / TimeSeries
        VeSeries = VeSer[1:] - VeSer[:-1]
        AccSer = VeSeries / TTimeSeries
    return AccSer


def CalVeloVariation(VeloVec):
    if VeloVec == 'none':
        Varia = 'none'
    else:
        Varia = numpy.zeros(2)
        halfPos = int(len(VeloVec) / 2)
        q25 = int(len(VeloVec) / 4)
        q75 = int(len(VeloVec) * 3 / 4)
        v25 = numpy.mean(VeloVec[q25:q75]) / numpy.mean(VeloVec)
        v75 = numpy.mean(VeloVec[q75:]) / numpy.mean(VeloVec)
        if numpy.mean(VeloVec[:halfPos]) == 0:
            Varia[0] = 0
        else:
            Varia[0] = numpy.std(VeloVec[:halfPos]) / numpy.mean(VeloVec[:halfPos])
        if numpy.mean(VeloVec[halfPos:]) == 0:
            Varia[1] = 0
        else:
            Varia[1] = numpy.std(VeloVec[halfPos:]) / numpy.mean(VeloVec[halfPos:])
    return (Varia, v25, v75)


def CalAccVariation(AccVec):
    if AccVec == 'none':
        AccAccVaria = 'none'
    else:
        AccVec = numpy.abs(AccVec)
        #        AccAccVaria = numpy.zeros(1)
        #        if numpy.mean(AccVec) == 0:
        #            AccAccVaria = 0
        #        else:
        AccAccVaria = numpy.mean(AccVec)
    #        numpy.max(AccVec)-numpy.min(AccVec)
    #            numpy.mean(AccVec)
    #            numpy.std(AccVec)
    #            /numpy.mean(AccVec)
    #        halfPos = len(AccVec)/2
    #        if numpy.mean(AccVec[:halfPos]) == 0:
    #            AccAccVaria[0] = 0
    #        else:
    #            AccAccVaria[0] = numpy.std(AccVec[:halfPos])/numpy.mean(AccVec[:halfPos])
    #        if numpy.mean(AccVec[halfPos:]) == 0:
    #            AccAccVaria[1] = 0
    #        else:
    #            AccAccVaria[1] = numpy.std(AccVec[halfPos:])/numpy.mean(AccVec[halfPos:])
    return AccAccVaria


def CalTheta(Txtdata):
    TracePos = Txtdata[Txtdata[:, 0] == 2]
    if len(TracePos) < 2:
        Theta = 'none'
    else:
        PointSeries = TracePos[1:, 1:3] - TracePos[:-1, 1:3]
        Theta = numpy.zeros([len(PointSeries), 1])
        for item in range(len(PointSeries)):
            if PointSeries[item, 0] == 0:
                Theta[item] = math.pi / 2
            else:
                Theta[item] = math.atan(PointSeries[item, 1] / PointSeries[item, 0])
    return Theta


def CalOmiga(Txtdata, Theta):
    if Theta == 'none' or len(Theta) < 2:
        Omiga = 'none'
    else:
        TracePos = Txtdata[Txtdata[:, 0] == 2]
        PointSeries = TracePos[1:, 1:4] - TracePos[:-1, 1:4]
        TimeSeries = PointSeries[:, 2]
        TimeSeries[TimeSeries == 0] = 1
        TimeSeries = TimeSeries[0:-1]
        #        TimeSeries = numpy.array(TimeSeries)
        dtheta = Theta[1:] - Theta[:-1]
        dtheta = dtheta[:, 0]
        Omiga = abs(dtheta) / TimeSeries
    return Omiga


def CalCurvatureCurve(Txtdata, Theta):
    if Theta == 'none' or len(Theta) < 2:
        Curvature = 'none'
    else:
        TracePos = Txtdata[Txtdata[:, 0] == 2]
        DistSeries = numpy.sqrt(numpy.sum((TracePos[1:, 1:3] - TracePos[:-1, 1:3]) ** 2, 1))
        DistSeries[DistSeries == 0] = 1
        dtheta = Theta[1:] - Theta[:-1]
        dtheta = dtheta[:, 0]
        Curvature = abs(dtheta) / DistSeries[:-1]
    return Curvature


def CalCurvatureDiff(Txtdata):
    pass


def CalMovementEfficiency(Txtdata):
    TracePos = Txtdata[Txtdata[:, 0] == 2]
    if len(TracePos) < 2:
        MoveEfficiency = 'none'
        Caldistance = 'none'
        Time = 'none'
        time2dict = 'none'
    else:
        Time = TracePos[len(TracePos) - 1, 3] - TracePos[0, 3]
        VecCur = (TracePos[1:, 1:3] - TracePos[:-1, 1:3]) ** 2
        distance = numpy.sqrt(VecCur.sum(1))
        displacement = (TracePos[len(TracePos) - 1, 1:3] - TracePos[0, 1:3]) ** 2
        aTemp = list(displacement)
        Caldisplacement = numpy.sqrt(sum(aTemp))
        bTemp = list(distance)
        Caldistance = sum(bTemp)
        if Caldistance == 0:
            MoveEfficiency = 'none'
            time2dict = 'none'
        else:
            time2dict = Caldisplacement / Time
            MoveEfficiency = Caldistance / Caldisplacement
    return MoveEfficiency, Time, time2dict


def CalTimeMove2Click(Txtdata):
    #    pass
    MouseDownIndex = numpy.where(Txtdata[:, 0] == 0)[0]
    if (len(MouseDownIndex) == 0):
        TimeMove2Click = 'none'
    else:
        MouseDownIndex = MouseDownIndex[-1]
        if Txtdata[MouseDownIndex - 1, 0] == 2:
            TimeMove2Click = Txtdata[MouseDownIndex, 3] - Txtdata[MouseDownIndex - 1, 3]
        else:
            #        print Txtdata[MouseDownIndex-1,0]
            TimeMove2Click = 'none'
    return TimeMove2Click


def CalTimeKeyUp2Click(Txtdata):
    MouseDownIndex = numpy.where(Txtdata[:, 0] == 0)[0]
    if (len(MouseDownIndex) == 0):
        TimeKeyUp2Click = 'none'
    else:
        if Txtdata[MouseDownIndex - 1, 0] == 4:
            TimeKeyUp2Click = Txtdata[MouseDownIndex, 3] - Txtdata[MouseDownIndex - 1, 3]
        else:
            #        print Txtdata[MouseDownIndex-1,0]
            TimeKeyUp2Click = 'none'
    return TimeKeyUp2Click


def CalTimeClick2KeyDown(Txtdata):
    KeyDownIndex = numpy.where(Txtdata[:, 0] == 3)[0]
    if len(KeyDownIndex) == 0:
        TimeClick2KeyDown = 'none'
    elif KeyDownIndex[0] == 0:
        TimeClick2KeyDown = 'none'
    elif Txtdata[KeyDownIndex[0] - 1, 0] == 1:
        TimeClick2KeyDown = Txtdata[KeyDownIndex[0], 3] - Txtdata[KeyDownIndex[0] - 1, 3]
    else:
        #        print Txtdata[MouseDownIndex-1,0]
        TimeClick2KeyDown = 'none'
    return TimeClick2KeyDown


def CalWholeDuation(Txtdata):
    WholeTime = Txtdata[-1, 3] - Txtdata[0, 3]
    return WholeTime


def CalKeyFeatures(Txtdata):
    keyUpIdx = numpy.where(Txtdata[:, 0] == 4)[0]
    keyDownIdx = numpy.where(Txtdata[:, 0] == 3)[0]
    if len(keyDownIdx) == 0 and len(keyUpIdx) == 0:
        Duration_Key = 'none'
        Interval_Key = 'none'
    elif len(keyDownIdx) == 1 and len(keyUpIdx) == 1:
        #        print('only one event(key up and key down)')
        intraKeyTime = Txtdata[keyUpIdx, 3] - Txtdata[keyDownIdx, 3]
        Duration_Key = numpy.mean(intraKeyTime, 0)
        Interval_Key = 'none'
    else:
        if (len(keyUpIdx) == len(keyDownIdx)):
            intraKeyTime = Txtdata[keyUpIdx, 3] - Txtdata[keyDownIdx, 3]
            interKeyTime = Txtdata[keyDownIdx[1:], 3] - Txtdata[keyUpIdx[:-1], 3]
            Duration_Key = numpy.mean(intraKeyTime, 0)
            Interval_Key = numpy.mean(interKeyTime, 0)
        else:
            #            print('indices don''t match(key up and key down events)')
            Duration_Key = 'none'
            Interval_Key = 'none'
    return (Duration_Key, Interval_Key)


def DataFormation(AllData):
    RawData = []
    RawDataType = numpy.zeros(len(AllData))
    for i in range(len(AllData)):
        linesAll = AllData[i]
        lines = []
        for line in range(len(linesAll)):  # 去除浏览器信息行
            tmp = linesAll[line].split()
            if (len(tmp) != 0 and (tmp[0].startswith("mouse"))):
                # add flag

                lines.append("schulte\t" + linesAll[line])
        tmp = lines[-1].split()
        if (tmp[1] == 'keydown' or tmp[1] == 'keyDown') and tmp[2] == '13':
            del lines[len(lines) - 1]
        tmp = lines[0].split()
        if (tmp[1] == 'keyup' or tmp[1] == 'keyUp') and tmp[2] == '13':
            del lines[0]
        txtcont = numpy.zeros((len(lines), 4))
        for line in range(len(lines)):
            tmp = lines[line].split()
            if (line == 0):
                timeFirst = int(tmp[-1][-8:])
            keyFg = False
            if (tmp[1].startswith('mousedown')):
                txtcont[line][0] = 0
            elif (tmp[1].startswith('mouseup')):
                txtcont[line][0] = 1
            elif (tmp[1] == 'mousemove'):
                txtcont[line][0] = 2
            elif (tmp[1] == 'keyUp' or tmp[1] == 'keyup'):
                txtcont[line][0] = 4
                keyFg = True
            elif (tmp[1] == 'keydown'):
                txtcont[line][0] = 3
                keyFg = True
            if (keyFg):
                txtcont[line, 1] = tmp[2]
                txtcont[line, 2] = 0
                txtcont[line, 3] = int(tmp[3][-8:]) - timeFirst
            else:
                txtcont[line, 1] = tmp[2]
                txtcont[line, 2] = tmp[3]
                try:

                    txtcont[line, 3] = int(tmp[4][-8:]) - timeFirst
                except BaseException:
                    txtcont[line, 3] = 0
                else:
                    txtcont[line, 3] = 0
                # txtcont[line, 3] = int(tmp[4][-8:]) - timeFirst
        DownIn = txtcont[txtcont[:, 0] == 0, :]
        UpIn = txtcont[txtcont[:, 0] == 1, :]
        Dcnt = DownIn.shape[0]
        Ucnt = UpIn.shape[0]
        MoveIn = txtcont[txtcont[:, 0] == 2, :]
        Mcnt = MoveIn.shape[0]
        KeyDownIn = txtcont[txtcont[:, 0] == 3, :]
        KeyUpIn = txtcont[txtcont[:, 0] == 4, :]
        KeyDcnt = KeyDownIn.shape[0]
        KeyUcnt = KeyUpIn.shape[0]
        if Dcnt == 0 or Ucnt == 0:  # 没有鼠标数据
            RawDataType[i] = 0
        elif Dcnt != Ucnt:  # 鼠标Down和Up不均衡
            RawDataType[i] = 0.5
        elif Mcnt <= 6:  # 鼠标移动数据过少
            RawDataType[i] = 0.75
        elif KeyDcnt != KeyUcnt:  # 击键Down和Up不均衡
            RawDataType[i] = 1
        else:  # 可能完整的数据
            RawDataType[i] = 2
        RawData.append(txtcont)
    return RawData, RawDataType


# def SectionProc(FormatData):
#    SectionRawData = []
#    for SampleId in range(len(FormatData)):
#        SingleSampleRawData = []
#        thisSampleData=FormatData[SampleId]
#        MouseDownIdx = numpy.where(thisSampleData[:,0]==1)[0]
#        SecIdx = numpy.zeros([1+len(MouseDownIdx)],dtype=int)
#        SecIdx[0] = -1
#        SecIdx[1:] = MouseDownIdx
#        if(SecIdx[-1] < len(thisSampleData)-1):
#            numpy.append(SecIdx,len(thisSampleData)-1)
#        for kI in range(1,len(SecIdx)):
#            if(SecIdx[kI] - SecIdx[kI-1] > 6):
#                MovingDataSec = thisSampleData[SecIdx[kI-1]+1:SecIdx[kI]+1,:]
#                SingleSampleRawData.append(MovingDataSec)
#        SectionRawData.append(SingleSampleRawData)
#    return SectionRawData

def SectionProc(FormatData):
    SectionRawData = []
    for SampleId in range(len(FormatData)):
        SingleSampleRawData = []
        thisSampleData = FormatData[SampleId]
        MouseUpIdx = numpy.where(thisSampleData[:, 0] == 1)[0]
        if len(MouseUpIdx) == 0:
            SingleSampleRawData.append(thisSampleData)
        else:
            SecIdx = numpy.zeros([1 + len(MouseUpIdx)], dtype=int)
            SecIdx[0] = -1
            SecIdx[1:] = MouseUpIdx
            if (SecIdx[-1] < len(thisSampleData) - 1):
                SecIdx = numpy.append(SecIdx, len(thisSampleData) - 1)  # 将点完登陆后的鼠标移动也记录
            #                SecIdx.append(len(thisSampleData)-1)
            for kI in range(1, len(SecIdx)):
                if (SecIdx[kI] - SecIdx[kI - 1] > 10):
                    MovingDataSec = thisSampleData[SecIdx[kI - 1] + 1:SecIdx[kI] + 1, :]
                    #                    print MovingDataSec.shape
                    SingleSampleRawData.append(MovingDataSec)
        #     print len(SingleSampleRawData)
        SectionRawData.append(SingleSampleRawData)
    return SectionRawData


# todo
# 改变分段方式
def SectionProc1(Formation):
    SectionRawData = []
    #    print len(Formation)
    for SampleId in range(len(Formation)):
        thisSampleData = Formation[SampleId]
        #        print thisSampleData.shape
        mousem = []
        SingleSampleRawData = []
        for i in range(len(thisSampleData) - 1):
            if ((thisSampleData[i, 0] == 2 and thisSampleData[i + 1, 0] == 2) or (
                    thisSampleData[i, 0] == 2 and (thisSampleData[i + 1, 0] == 0 or thisSampleData[i + 1, 1] == 9))):
                mousem.append(thisSampleData[i, :])
            if (thisSampleData[i, 0] != 2):
                if (len(mousem) > 10):
                    mousem = numpy.array(mousem)
                    #                print mousem.shape
                    SingleSampleRawData.append(mousem)
                mousem = []
        #        print len(SingleSampleRawData)
        SectionRawData.append(SingleSampleRawData)
    return SectionRawData
