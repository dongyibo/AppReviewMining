# -*- coding:utf-8 -*-
from __future__ import division
import vsm
from data.dataGetter import DataGetter
import numpy as np

'''
文本中心计算
'''


class Center(object):
    def __init__(self):
        self.__clusterHelper = DataGetter.get__clusterHelper()
        self.__db = DataGetter.get__db()

        # self.__data = self.__get_data(category, appId)
        # self.__vsm = vsm.VSM(self.__data)

    def set_property(self, category, appId):
        self.__category = category
        self.__appId = appId
        self.__data = self.__get_data()

    # 计算
    def calculate(self):
        lis = []
        for cluster in self.__data:
            # 判断是否是小于两元素，若是则不用计算
            if len(cluster) <= 2:
                result = cluster
            else:
                self.__vsm = vsm.VSM(cluster)
                result = self.__calculate_detail(cluster)
            l = []
            for r in result:
                l.append(r[0])
            lis.append(l)
        return lis

    # 计算细节
    def __calculate_detail(self, data):
        length = len(data)
        matrix = np.zeros((length, length))
        i = 0
        while i < length - 1:
            j = i + 1
            while j < length:
                matrix[i][j] = self.__dist(data[i], data[j])
                matrix[j][i] = matrix[i][j]
                j += 1
            i += 1
        # return matrix
        dic = {}
        for c in range(length):
            dic[data[c][0]] = sum(matrix[c]) / length
        # 降序
        dic = sorted(dic.items(), key=lambda x: x[1], reverse=True)
        # print dic
        return dic

    # 记录
    def record_data(self, lis):
        self.__clusterHelper.record_clusters_appId_prioritize(lis, self.__category, self.__appId)

    # 计算两个文本的距离，基于VSM
    def __dist(self, data1, data2):
        text1 = data1[1]
        text2 = data2[1]
        return 1 - self.__vsm.calculate_cos_similarity(text1, text2)

    # 获取数据
    def __get_data(self):
        ids = self.__clusterHelper.get_clusters_appId(self.__category, self.__appId)
        return self.__db.get_content_by_id(ids)


# c = Center()
# c.set_property(2, 485)
# data = c.calculate()
# c.record_data(data)
