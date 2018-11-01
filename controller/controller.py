# -- coding: utf-8 --
from preprocess import preprocess
from prioritize import prioritize
from classify import bayes
from cluster import dbscan, center
from util import db_const as con
from data.dataGetter import DataGetter


class Controller(object):
    @staticmethod
    # 给数据贴标签
    def classify_data(lower, quantity):
        database = DataGetter.get__db()
        # 从原始数据中读取指定数量数据
        data = database.load_specified_quantity_data(lower, quantity)
        # 初始化预处理器和分类器
        p = preprocess.Preprocess()
        b = bayes.Bayes()
        for i in range(len(data)):
            # 将数据进行预处理
            p.set_sentence(data[i][1])
            sentence_processed = p.preprocess()
            if sentence_processed == '':
                category = con.USELESS
            else:
                # 朴素贝叶斯算法分类器对文本进行分类
                # print sentence_processed, data[i][2]
                b.set_property(sentence_processed, data[i][2])
                category = b.bayes_classifier_improved2()
            data[i] = [data[i][0], sentence_processed, data[i][2], category]
            # print data[i]
        # 持久化
        database.save_data(data)

    @staticmethod
    # 为同类数据聚簇
    def cluster_data(category, Minpts=2, e=0.6):
        # 获取应用id
        database = DataGetter.get__db()
        appIds = database.get_app_ids()
        d = dbscan.DBSCAN()
        for appId in appIds:
            # dbscan算法聚簇
            d.set_property(category, appId)
            clusters = d.dbscan(Minpts, e)
            # 持久化数据
            d.record_cluster(clusters)

    @staticmethod
    # 簇内排序
    def center(category):
        database = DataGetter.get__db()
        appIds = database.get_app_ids()
        c = center.Center()
        for appId in appIds:
            c.set_property(category, appId)
            data = c.calculate()
            c.record_data(data)

    @staticmethod
    # 排序展示数据
    def prioritize_data(category, appId):
        # 排序
        p = prioritize.Prioritize(category, appId)
        data = p.prioritize()
        # 展示
        show_data = p.show_to_frontend(data)
        # print show_data
        # for s in show_data:
        return show_data

    @staticmethod
    # 排序展示数据
    def prioritize_data_aborted(category, appId):
        # 排序
        p = prioritize.Prioritize(category, appId)
        p.setIsAborted(True)
        data = p.prioritize()
        # 展示
        show_data = p.show_to_frontend(data)
        # print show_data
        # for s in show_data:
        return show_data

    @staticmethod
    # 软删除含有id的簇
    def abort(id, category, appId):
        # print 'abort'
        c = DataGetter.get__clusterHelper()
        c.abort(id, category, appId)

    @staticmethod
    # 恢复含有id的簇
    def recover(id, category, appId):
        c = DataGetter.get__clusterHelper()
        c.recover(id, category, appId)

        # @staticmethod
        # # 比较1
        # def compare(version):
        #     list = []
        #
        #     p = preprocess.Preprocess()
        #     b = bayes.Bayes()
        #     database = DataGetter.get__db()
        #     data = database.load_specified_quantity_data(1500, 500)
        #     for d in data:
        #         p.set_sentence(d[1])
        #         sentence_processed = p.preprocess()
        #         b.set_property(sentence_processed, d[2])
        #         if version == 1:
        #             res = b.bayes_classifier()
        #         elif version == 2:
        #             res = b.bayes_classifier_improved()
        #         else:
        #             res = b.bayes_classifier_improved2()
        #         list.append([d[0], res])
        #
        # @staticmethod
        # def compare2():
        #     list3 = []
        #
        #     p = preprocess.Preprocess()
        #     b = bayes.Bayes()
        #     database = DataGetter.get__db()
        #     data = database.load_specified_quantity_data(1500, 500)
        #     bug, feature = 0, 0
        #     for d in data:
        #         p.set_sentence(d[1])
        #         sentence_processed = p.preprocess()
        #         b.set_property(sentence_processed, d[2])
        #         res = b.bayes_classifier_improved2()
        #         list3.append([d[0], res])
        #         if res == con.BUG:
        #             bug += 1
        #         elif res == con.FEATURE:
        #             feature += 1
        #
        #     print bug, feature, bug + feature
        #
        # # list2 = compare1()
        #
        # list1 = file.test()
        #
        # for i in range(100):
        #     if not (int(list1[i]) == list2[i][1] and int(list1[i]) == list3[i][1]):
        #         print list2[i][0], ':', list1[i], list2[i][1], list3[i][1]
        #
        # for i in range(400):
        #     if not (list2[i][1] == list3[i][1]):
        #         print list2[i][0], ':', list2[i][1], list3[i][1]
        # print 'end...'


# def compare():
#     list1, list2, list3 = [], [], []
#     p = preprocess.Preprocess()
#     b = bayes.Bayes()
#     database = DataGetter.get__db()
#     data = database.load_specified_quantity_data(1500, 500)
#     for d in data:
#         p.set_sentence(d[1])
#         sentence_processed = p.preprocess()
#         b.set_property(sentence_processed, d[2])
#         # 版本1
#         list1.append([d[0], b.bayes_classifier()])
#         # 版本2
#         list2.append([d[0], b.bayes_classifier_improved()])
#         # 版本3
#         list3.append([d[0], b.bayes_classifier_improved2()])
#     return list1, list2, list3
#
# list1, list2, list3 = compare()
# for i in range(500):
#     if not (list1[i][1] == list2[i][1] == list3[i][1]):
#         print 'id' + str(list2[i][0]), ':', list1[i][1], list2[i][1], list3[i][1]


#
# if __name__ == "__main__":
#
    # pass
# 数据分类
# 聚簇
# Controller.classify_data(4909, 3553)
# Controller.cluster_data(con.FEATURE, 2, 0.5)

# Controller.center(1)
# d = dbscan.DBSCAN()
# d.set_property(2, 481)
# da = d.dbscan(2, 0.75)
# for a in da:
#     print a
# d.record_cluster(da)
#     # prioritize_data(con.BUG)
#     # compare1()
#     # compare2()
#     with open('/Users/dongyibo/Desktop/script/nla_businessReview.sql', 'r') as fr:
#         lines = fr.readlines()
#     with open('/Users/dongyibo/Desktop/script/nla_businessReview2.sql', 'w+') as fw:
#         i = 1
#         for line in lines:
#             token = line.split('VALUES (')
#             sql = 'UPDATE raw_review set appId = ' + token[1][:3] + ' WHERE id = ' + str(i)
#             fw.write(sql + ';\n')
#             i += 1

# d = dbscan.DBSCAN()
# d.set_property(2, 482)
# clusters = d.dbscan(2, 0.6)
# list = []
# for cluster in clusters:
#     l = []
#     for c in cluster:
#         l.append(c[0])
#     list.append(l)
# for l in list:
#     print l