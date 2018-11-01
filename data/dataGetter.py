# -- coding: utf-8 --
import db
import clusterHelper

'''
静态类，获取db和clusterHelper实例
'''


class DataGetter(object):
    @staticmethod
    def get__db():
        database = db.DB()
        return database

    @staticmethod
    def get__clusterHelper():
        ch = clusterHelper.ClusterHelper()
        return ch


        # print DataGetter.get__clusterHelper()
