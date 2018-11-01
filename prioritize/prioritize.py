# -- coding: utf-8 --
from __future__ import division

import math

from data.dataGetter import DataGetter

'''
给簇评论排序
'''


class Prioritize(object):
    def __init__(self, category, appId):
        self.__category = category
        self.__appId = appId
        self.__database = DataGetter.get__db()
        self.__clusterHelper = DataGetter.get__clusterHelper()
        self.__isAborted = False

    # 设置是否是废弃数据
    def setIsAborted(self, isAborted):
        self.__isAborted = isAborted

    # 排序
    def prioritize(self):
        # 获取数据
        clusters = self.__get_category_clusters()

        # 统计每个簇的评论总数和平均打分
        lis = []
        for cluster in clusters:
            quantity = len(cluster)
            sum_rate = 0
            sum_date = 0
            for c in cluster:
                # print c
                sum_rate += c[len(c) - 2]
                sum_date += self.__handle_date(c[1])
            average_date = sum_date / quantity
            average_rate = sum_rate / quantity
            # 计算得分
            score = self.__prioritize_formula(quantity, average_rate, average_date, 1.2)
            lis.append((cluster, score))

        # 根据得分降序排列
        lis = sorted(lis, key=lambda l: l[1], reverse=True)
        return lis

    # 给前端显示的数据
    def show_to_frontend(self, data):
        lis = []
        # 加序号
        i = 1
        for d in data:
            lis.append((i, d[0]))
            i += 1
        return lis

    # 处理日期
    def __handle_date(self, date):
        d = date.split('-')
        # if not d[0][3].isdigit() or not d[1].isdigit() or not d[2].isdigit():
        #     # print 'a'
        #     return 6.5
        tmp = int(d[0][3]) * 10000 + int(d[1]) * 100 + int(d[2])
        return tmp / 10000

    # 排序公式
    def __prioritize_formula(self, quantity, average_rate, average_date, k=1):
        y = quantity / (average_rate ** k) * math.sqrt(average_date)
        return y

    # 获取某类别的所有簇
    def __get_category_clusters(self):
        if not self.__isAborted:
            ids = self.__clusterHelper.get_category_all_custer_data(self.__category, self.__appId)
        else:
            ids = self.__clusterHelper.get_category_all_custer_data_aborted(self.__category, self.__appId)
        clusters = self.__database.get_data_by_id(ids)
        return clusters

# p = Prioritize(1)
# p.setIsAborted(True)
# d = p.show_to_frontend(p.prioritize())
# print d

# 209493
