# -- coding: utf-8 --
from __future__ import division

import util.db_const as con
from data.dataGetter import DataGetter
from util import const

'''
朴素贝叶斯分类器
'''


class Bayes(object):
    def __init__(self):
        self.__database = DataGetter.get__db()

    def set_property(self, token, rate=None):
        self.__token = token
        self.__rate = rate

    # 贝叶斯分类算法
    def bayes_classifier(self):
        # 计算分类比例
        [bugC, featureC, otherC, totalCount] = self.__get_category_num()
        bugP = bugC / totalCount
        featureP = featureC / totalCount
        otherP = otherC / totalCount

        # 计算单词比例
        # 设置lambda
        lambd = 1
        wordP = []
        [bug_word_count, feature_word_count, other_word_count, total_word_count] = \
            self.__get_text_statistics()

        tokens = self.__token.split(' ')
        for word in tokens:  # 统计词频，可以改进
            [word_bug_frequency, word_feature_frequency, word_other_frequency] = \
                self.__get_word_frequency(word)

            word_bugP = (word_bug_frequency + lambd) / (bug_word_count + total_word_count * lambd)
            word_featureP = (word_feature_frequency + lambd) / (feature_word_count + total_word_count * lambd)
            word_otherP = (word_other_frequency + lambd) / (other_word_count + total_word_count * lambd)
            lis = [word_bugP, word_featureP, word_otherP]
            wordP.append(lis)

        # 计算概率
        token_bugP = 1 * bugP
        token_featureP = 1 * featureP
        token_otherP = 1 * otherP

        for i in range(len(tokens)):
            token_bugP *= wordP[i][0]
            token_featureP *= wordP[i][1]
            token_otherP *= wordP[i][2]

        dict = {con.BUG: token_bugP, con.FEATURE: token_featureP, con.OTHER: token_otherP}

        # 降序
        dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
        # print dict
        category = dict[0][0]
        return category

    # 提高版贝叶斯分类算法
    def bayes_classifier_improved(self):
        # 计算分类比例
        [bugC, featureC, otherC, totalCount] = self.__get_category_num()
        bugP = bugC / totalCount
        featureP = featureC / totalCount
        otherP = otherC / totalCount

        # 计算单词比例
        # 设置lambda
        lambd = 1
        wordP = []
        [bug_word_count, feature_word_count, other_word_count, total_word_count] = \
            self.__get_text_statistics()

        tokens = self.__token.split(' ')
        for word in tokens:  # 统计词频，可以改进
            [word_bug_frequency, word_feature_frequency, word_other_frequency] = \
                self.__get_word_frequency(word)

            word_bugP = (word_bug_frequency + lambd) / (bug_word_count + total_word_count * lambd)
            word_featureP = (word_feature_frequency + lambd) / (feature_word_count + total_word_count * lambd)
            word_otherP = (word_other_frequency + lambd) / (other_word_count + total_word_count * lambd)
            lis = [word_bugP, word_featureP, word_otherP]
            wordP.append(lis)

        # 获取各类的评分计数
        bug_rate, feature_rate, other_rate = self.__get_category_rate()
        bug_rateP = (bug_rate + lambd) / bugC
        feature_rateP = (feature_rate + lambd) / featureC
        other_rateP = (other_rate + lambd) / otherC

        # 计算概率
        token_bugP = 1 * bugP * bug_rateP
        token_featureP = 1 * featureP * feature_rateP
        token_otherP = 1 * otherP * other_rateP

        for i in range(len(tokens)):
            token_bugP *= wordP[i][0]
            token_featureP *= wordP[i][1]
            token_otherP *= wordP[i][2]

        dict = {con.BUG: token_bugP, con.FEATURE: token_featureP, con.OTHER: token_otherP}

        # 降序
        dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
        # print dict
        category = dict[0][0]
        return category

    # 提高版贝叶斯分类器2
    def bayes_classifier_improved2(self):
        # 计算分类比例
        [bugC, featureC, otherC, totalCount] = self.__get_category_num()
        bugP = bugC / totalCount
        featureP = featureC / totalCount
        otherP = otherC / totalCount

        # 计算单词比例
        # 设置lambda
        lambd = 1
        wordP = []
        [bug_word_count, feature_word_count, other_word_count, total_word_count] = \
            self.__get_text_statistics()

        tokens = self.__token.split(' ')
        for word in tokens:  # 统计词频，可以改进
            [word_bug_frequency, word_feature_frequency, word_other_frequency] = \
                self.__get_word_frequency(word)

            word_bugP = (word_bug_frequency + lambd) / (bug_word_count + total_word_count * lambd)
            word_featureP = (word_feature_frequency + lambd) / (feature_word_count + total_word_count * lambd)
            word_otherP = (word_other_frequency + lambd) / (other_word_count + total_word_count * lambd)
            lis = [word_bugP, word_featureP, word_otherP]
            wordP.append(lis)

        # 获取各类的评分计数
        bug_rate, feature_rate, other_rate = self.__get_category_rate()
        bug_rateP = (bug_rate + lambd) / bugC
        feature_rateP = (feature_rate + lambd) / featureC
        other_rateP = (other_rate + lambd) / otherC

        # 获取各类的长度计数
        bug_length, feature_length, other_length = self.__get_category_length(len(tokens))
        bug_lengthP = (bug_length + lambd) / bugC
        feature_lengthP = (feature_length + lambd) / featureC
        other_lengthP = (other_length + lambd) / otherC

        # 计算概率
        token_bugP = 1 * bugP * bug_rateP * bug_lengthP
        token_featureP = 1 * featureP * feature_rateP * feature_lengthP
        token_otherP = 1 * otherP * other_rateP * other_lengthP

        for i in range(len(tokens)):
            token_bugP *= wordP[i][0]
            token_featureP *= wordP[i][1]
            token_otherP *= wordP[i][2]

        dict = {con.BUG: token_bugP, con.FEATURE: token_featureP, con.OTHER: token_otherP}

        # 降序
        dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)
        # print dict
        category = dict[0][0]
        return category

    # 得到各类评分数目
    def __get_category_length(self, length):
        return self.__database.get_length_frequency(length)

    # 得到各类评分数目
    def __get_category_rate(self):
        return self.__database.get_rate_frequency(self.__rate)

    # 得到分类数目
    def __get_category_num(self):
        # return file.get_category_sentence_num()
        return self.__database.get_category_sentence_num()

    # 得到单词频率
    def __get_word_frequency(self, word):
        # return file.get_word_frequency(word)
        return self.__database.get_word_frequency(word)

    # 得到文本数据
    def __get_text_statistics(self):
        # return file.get_text_statistics()
        return self.__database.get_text_statistics()

# print bayes_classifier('a big bug')

# bayes = Bayes()
# bayes.set_property('bug', 1)
# # print bayes.bayes_classifier()
# # print bayes.bayes_classifier_improved()
# print bayes.bayes_classifier_improved2()
