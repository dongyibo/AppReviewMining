# -- coding: utf-8 --
import MySQLdb

from preprocess import preprocess as pre
from util import db_const as const

'''
数据库单例
'''


class DB(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(DB, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __del__(self):
        self.__db.close()

    def __init__(self):
        self.__db = MySQLdb.connect(const.LOCAL_HOST, const.USERNAME, const.PASSWORD, const.DATABASE, charset='utf8')
        self.__cursor = self.__db.cursor()

    def test(self):
        self.__cursor.execute("SELECT * FROM raw_review WHERE id <= 10")
        data = self.__cursor.fetchall()
        print data

    # 统计
    def check_statistic(self):
        bug, feature, other, useless = 0, 0, 0, 0
        self.__cursor.execute("SELECT category FROM raw_review where 1 <= id and id <= 1300")
        data = self.__cursor.fetchall()
        for d in data:
            cla = d[0]
            if cla == const.BUG:
                bug += 1
            elif cla == const.FEATURE:
                feature += 1
            elif cla == const.OTHER:
                other += 1
            else:
                print cla
                useless += 1
        # self.__close_db()
        print bug, feature, other, useless

        # 统计

    def check_statistic2(self):
        self.__cursor.execute("SELECT content,category FROM process_review where 1 <= id and id <= 1300")
        data = self.__cursor.fetchall()
        for d in data:
            cla = d[1]
            if cla == const.BUG:
                token = d[0].split(' ')
                print len(token)

    # 文本预处理
    def write_preprocess_sentence(self):
        p = pre.Preprocess()
        self.__cursor.execute("SELECT id, content, rate, category FROM raw_review where 1 <= id and id <= 1300")
        data = self.__cursor.fetchall()
        for d in data:
            id = d[0]
            content = d[1]
            rate = d[2]
            category = d[3]
            # 预处理
            p.set_sentence(content)
            res = p.preprocess()

            if res == '':
                category = const.USELESS

            sql = "INSERT INTO process_review(id, content, rate, category) VALUES(%s, '%s', %s, %s)" % (
                id, res, rate, category)
            self.__cursor.execute(sql)
            self.__db.commit()

    # 获取给分类总数
    def get_category_sentence_num(self):
        self.__cursor.execute(
            "SELECT COUNT(*) FROM process_review WHERE category != %s GROUP BY category" % const.USELESS)
        data = self.__cursor.fetchall()
        lis = []
        total_count = 0
        for d in data:
            lis.append(d[0])
            total_count += d[0]
        lis.append(total_count)
        return lis

    # 获取文本统计数据
    def get_text_statistics(self):
        bug_word_count = 0
        feature_word_count = 0
        other_word_count = 0
        total_word_set = set()
        self.__cursor.execute("SELECT content, category FROM process_review")
        data = self.__cursor.fetchall()
        for d in data:
            cla = d[1]
            token = d[0]
            tokens = token.split(' ')
            if cla == const.BUG:
                bug_word_count += len(tokens)
            elif cla == const.FEATURE:
                feature_word_count += len(tokens)
            elif cla == const.OTHER:
                other_word_count += len(tokens)
            else:
                pass
            tokens_set = set(tokens)
            total_word_set |= tokens_set

        total_word_count = len(total_word_set)
        return [bug_word_count, feature_word_count, other_word_count, total_word_count]

    # 获取某单词频率
    def get_word_frequency(self, word):
        bug_frequency = 0
        feature_frequency = 0
        other_frequency = 0
        self.__cursor.execute("SELECT content, category FROM process_review")
        data = self.__cursor.fetchall()
        for d in data:
            cla = d[1]
            token = d[0]
            tokens = token.split(' ')
            for w in tokens:
                if word == w:
                    if cla == const.BUG:
                        bug_frequency += 1
                    elif cla == const.FEATURE:
                        feature_frequency += 1
                    elif cla == const.OTHER:
                        other_frequency += 1
                    else:
                        pass

        return [bug_frequency, feature_frequency, other_frequency]

    # 获取某打分在各类中的数量
    def get_rate_frequency(self, rate):
        lis = []
        self.__cursor.execute(
            "SELECT category, COUNT(*) FROM process_review WHERE rate = %s AND category != %s GROUP BY category" % (
                rate, const.USELESS))
        data = self.__cursor.fetchall()
        for d in data:
            lis.append(d[1])
        return lis

    # 获取文本长度在各类中的数量
    def get_length_frequency(self, length):
        bug_frequency = 0
        feature_frequency = 0
        other_frequency = 0
        self.__cursor.execute("SELECT category, content FROM process_review")
        data = self.__cursor.fetchall()
        for d in data:
            cla = d[0]
            tokens = d[1].split(' ')
            if len(tokens) == length:
                if cla == const.BUG:
                    bug_frequency += 1
                elif cla == const.FEATURE:
                    feature_frequency += 1
                elif cla == const.OTHER:
                    other_frequency += 1
                else:
                    pass
        return [bug_frequency, feature_frequency, other_frequency]

    # 加载指定数量数据
    def load_specified_quantity_data(self, begin, quantity):
        self.__cursor.execute(
            "SELECT id, content, rate FROM raw_review WHERE id > %d and id <= %d" % (begin, begin + quantity))
        data = self.__cursor.fetchall()
        lis = []
        for d in data:
            lis.append([d[0], d[1], d[2]])
        return lis

    # 保存数据
    def save_data(self, data):
        for d in data:
            id = d[0]
            res = d[1]
            rate = d[2]
            category = d[3]
            sql = "INSERT INTO process_review2(id, content, rate, category) VALUES(%s, '%s', %s, %s)" % (
                id, res, rate, category)
            self.__cursor.execute(sql)
        self.__db.commit()

    # 文本预处理不含同义处理
    def write_preprocess_sentence_without_synonymous(self, lower):
        p = pre.Preprocess()
        sql = "SELECT r.id, r.content, p.category FROM raw_review AS r, process_review2 AS p WHERE r.id = p.id AND r.id > %s" % lower
        self.__cursor.execute(sql)
        data = self.__cursor.fetchall()
        for d in data:
            cla = d[2]
            p.set_sentence(d[1])
            res = p.preprocess(False)
            if res == '':
                cla = const.USELESS
            self.__cursor.execute("INSERT INTO process_review3(id, content, category) VALUES(%s, '%s', %s)" % (
                d[0], res, cla))
        self.__db.commit()

    # 获取某类别文本数据（弃用）
    def get_category_data(self, category):
        self.__cursor.execute("SELECT id, content FROM process_review3 WHERE category = %s" % category)
        data = self.__cursor.fetchall()
        return data

    # 获取某类别文本数据根据appId
    def get_category_data_by_appId(self, category, appId):
        self.__cursor.execute(
            "SELECT p.id, p.content FROM process_review3 AS p, raw_review AS r WHERE p.category = %s AND r.appId = %s AND p.id = r.id" % (
            category, appId))
        data = self.__cursor.fetchall()
        return data

    # 根据id获取数据
    def get_data_by_id(self, ids):
        lis = []
        for id in ids:
            l = []
            for i in id:
                sql = "SELECT reviewer_name, `date`, content, rate, id FROM raw_review WHERE id = %s" % i
                self.__cursor.execute(sql)
                data = self.__cursor.fetchone()
                l.append(data)
            lis.append(l)
        return lis

    # 根据id获取数据
    def get_content_by_id(self, ids):
        lis = []
        for id in ids:
            l = []
            for i in id:
                sql = "SELECT id, content FROM process_review3 WHERE id = %s" % i
                self.__cursor.execute(sql)
                data = self.__cursor.fetchone()
                l.append(data)
            lis.append(l)
        return lis

    # 获取app的id
    def get_app_ids(self):
        self.__cursor.execute("SELECT id FROM app")
        data = self.__cursor.fetchall()
        lis = []
        for d in data:
            lis.append(d[0])
        return lis

# d = DB()
# d.check_statistic2()
# d.test()
# d.write_preprocess_sentence()
# print d.get_category_sentence_num()  # [305, 129, 866, 1300]
# print d.get_text_statistics()
# print d.get_word_frequency('bug') #[41, 1, 39]
# print d.get_rate_frequency(1)
# print d.load_specified_quantity_data(1300,2)
# print d.get_length_frequency(4)
# print d.get_category_data(2)
# d.write_preprocess_sentence_without_synonymous(4909)
# a= d.get_data_by_id([[1, 3], [4, 5, 7]])
# print d.get_app_ids()
# print len(d.get_category_data_by_appId(2,484))
# dd= d.get_content_by_id([[137, 201, 170, 174], [20, 37]])
# for d in dd:
#     print d


# @staticmethod
# def get_db():
#     # 打开数据库连接
#     db = MySQLdb.connect(const.LOCAL_HOST, const.USERNAME, const.PASSWORD, const.DATABASE, charset='utf8')
#     return db
#
# @staticmethod
# def close_db(db):
#     db.close()
