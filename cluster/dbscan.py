# -*- coding:utf-8 -*-

import numpy as np

import vsm
from data.dataGetter import DataGetter

'''
基于密度的DBSCAN聚类算法
'''


class DBSCAN(object):
    def __init__(self):
        self.__database = DataGetter.get__db()
        self.__clusterHelper = DataGetter.get__clusterHelper()
        # self.__category = category
        # self.__appId = appId
        # self.__data = self.__get_data()
        # # 初始化一个vsm对象
        # self.__vsm = vsm.VSM(self.__data)

    # 设置属性
    def set_property(self, category, appId):
        self.__category = category
        self.__appId = appId
        self.__data = self.__get_data()
        # 初始化一个vsm对象
        self.__vsm = vsm.VSM(self.__data)

    # DBSCAN算法
    def dbscan(self, Minpts=2, e=0.6):
        # 初始化核心对象集合T,聚类个数k,聚类集合C, 未访问集合P
        D = self.__data
        T = set()
        k = 0
        C = []
        P = set(D)
        for d in D:
            if len([i for i in D if self.__dist(d, i) <= e]) >= Minpts:
                T.add(d)
                # print d
        # 开始聚类
        while len(T):
            P_old = P
            o = list(T)[np.random.randint(0, len(T))]
            P = P - set(o)
            Q = []
            Q.append(o)
            while len(Q):
                q = Q[0]
                Nq = [i for i in D if self.__dist(q, i) <= e]
                if len(Nq) >= Minpts:
                    S = P & set(Nq)
                    Q += (list(S))
                    P = P - S
                Q.remove(q)
            k += 1
            Ck = list(P_old - P)
            T = T - set(Ck)
            C.append(Ck)
        return C

    # 记录聚簇数据
    def record_cluster(self, clusters):
        lis = []
        for cluster in clusters:
            l = []
            for c in cluster:
                l.append(c[0])
            lis.append(l)
        # file.record_clusters(lis, self.__category)
        # self.__clusterHelper.record_clusters(lis, self.__category)
        self.__clusterHelper.record_clusters_appId(lis, self.__category, self.__appId)
        # return list

    # 获取某类别数据
    def __get_data(self):
        # data = file.get_category_data(category)
        # data = self.__database.get_category_data(self.__category)
        data = self.__database.get_category_data_by_appId(self.__category, self.__appId)
        return data

    # 计算两个文本的距离，基于VSM
    def __dist(self, data1, data2):
        text1 = data1[1]
        text2 = data2[1]
        return 1 - self.__vsm.calculate_cos_similarity(text1, text2)
