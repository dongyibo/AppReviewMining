# -- coding: utf-8 --
import preprocess as pre
from util import const

'''
文件与逻辑的接口
'''


# 获取自定义停词列表
def get_stop_words_list():
    list = []
    with open(const.STOPWORDS_LIST_PATH) as f:
        for line in f:
            list.append(line.strip())
    return list


# 过滤掉过长的other类
def filter_long_other(limit=10):
    with open(const.FIRST_PROCESS_REVIEW_PATH, 'r') as fr:
        fw = open(const.PREPROCESS_REVIEW_PATH, 'w+')
        # count = 0
        for line in fr:
            l = line.split(',')
            s = l[len(l) - 2]
            tokens = s.split(' ')
            tokens_length = len(tokens)
            cla = l[len(l) - 1].strip()
            if cla == const.OTHER and tokens_length > limit:
                cla = const.USELESS
                # count += 1
            fw.write(l[0] + ',' + s + ',' + cla + '\n')
            # i += 1
            # if i == 1000:  # 100行
            #     break
        # print count
        fw.close()


# filter_long_other()


# 统计
def check_statistic():
    with open(const.PREPROCESS_REVIEW_PATH, 'r') as fr:
        i = 0
        bug, feature, other, useless = 0, 0, 0, 0
        for line in fr:
            l = line.split(',')
            cla = l[len(l) - 1].strip()
            if cla == const.BUG:
                bug += 1
            elif cla == const.FEATURE:
                feature += 1
            elif cla == const.OTHER:
                other += 1
            else:
                useless += 1
            i += 1
            # if i == 1000:  # 100行  211 112 669 8 / 305 128 856 11 / 305 128 699 168 1132
            #     break
        print bug, feature, other, useless


# check_statistic()


# 文本预处理
def write_preprocess_sentence():
    with open(const.MARKED_REVIEW_PATH, 'r') as fr:
        fw = open(const.FIRST_PROCESS_REVIEW_PATH, 'w+')
        i = 0
        p = pre.Preprocess()
        for line in fr:
            l = line.split(',')
            cla = l[len(l) - 1].strip()
            j = 5
            s = ''
            while j < len(l) - 2:
                s += l[j] + ','
                j += 1
            # print s
            # 预处理
            p.set_sentence(s)
            res = p.preprocess()
            # 如果出现非英文文本，处理为空文本，并标位第4类
            if res == '':
                cla = '4'
            fw.write(l[0] + ',' + s + res + ',' + cla + '\n')

            i += 1
            if i == 1300:
                break

        fw.close()


# write_preprocess_sentence()

# 文本预处理不含同义处理
def write_preprocess_sentence_without_synonymous():
    with open(const.FIRST_PROCESS_REVIEW_PATH, 'r') as fr:
        fw = open(const.REVIEW_FOR_CLUSTER_PATH, 'w+')
        p = pre.Preprocess()
        for line in fr:
            l = line.split(',')
            cla = l[len(l) - 1].strip()
            j = 1
            s = ''
            while j < len(l) - 2:
                if j == len(l) - 3:
                    s += l[j]
                else:
                    s += l[j] + ','
                j += 1
            # print s
            # 预处理
            p.set_sentence(s)
            res = p.preprocess(False)
            # 如果出现非英文文本，处理为空文本，并标位第4类
            if res == '':
                cla = '4'
            fw.write(l[0] + ',' + res + ',' + cla + '\n')

        fw.close()


# write_preprocess_sentence_without_synonymous()


# 获取给分类总数
def get_category_sentence_num():
    bug_count = 0
    feature_count = 0
    other_count = 0
    # total_count = 0
    with open(const.PREPROCESS_REVIEW_PATH, 'r') as f:
        for line in f:
            l = line.split(',')
            cla = l[len(l) - 1].strip()
            if cla == const.BUG:
                bug_count += 1
            elif cla == const.FEATURE:
                feature_count += 1
            elif cla == const.OTHER:
                other_count += 1
            else:
                pass
                # total_count += 1
        total_count = bug_count + feature_count + other_count
    return [bug_count, feature_count, other_count, total_count]


# 获取文本统计数据
def get_text_statistics():
    bug_word_count = 0
    feature_word_count = 0
    other_word_count = 0
    total_word_set = set()
    with open(const.PREPROCESS_REVIEW_PATH, 'r') as f:
        for line in f:
            l = line.split(',')
            cla = l[len(l) - 1].strip()
            token = l[len(l) - 2]
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
def get_word_frequency(word):
    bug_frequency = 0
    feature_frequency = 0
    other_frequency = 0
    with open(const.PREPROCESS_REVIEW_PATH, 'r') as f:
        for line in f:
            l = line.split(',')
            cla = l[len(l) - 1].strip()
            token = l[len(l) - 2]
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


# 加载统计数据（弃用）
def load_statistical_data(category):
    text_num = get_text_num(category)
    text_content = get_text_content(category)
    return text_num, text_content


# 获取指定类型文本内容（弃用）
def get_text_content(category):
    lis = []
    with open(const.REVIEW_FOR_CLUSTER_PATH, 'r') as f:
        for line in f:
            l = line.split(',')
            cla = l[len(l) - 1].strip()
            if cla == category:
                token = l[len(l) - 2]
                tokens = token.split(' ')
                lis.append(tokens)
    return lis


# 获取文本数量(弃用)
def get_text_num(category):
    count = 0
    with open(const.REVIEW_FOR_CLUSTER_PATH, 'r') as f:
        for line in f:
            l = line.split(',')
            cla = l[len(l) - 1].strip()
            if cla == category:
                count += 1
    # print count
    return count


# get_text_num()

# 获取包含单词的文本数目(弃用)
def get_text_num_contain_word(word, category):
    count = 0
    with open(const.REVIEW_FOR_CLUSTER_PATH, 'r') as f:
        for line in f:
            l = line.split(',')
            cla = l[len(l) - 1].strip()
            token = l[len(l) - 2]
            tokens = token.split(' ')
            if cla == category:
                for w in tokens:
                    if w == word:
                        count += 1
                        break
    # print count
    return count


# get_text_num_contain_word('bug')

# 获取某类别文本数据
def get_category_data(category):
    lis = []
    with open(const.REVIEW_FOR_CLUSTER_PATH, 'r') as f:
        for line in f:
            l = line.split(',')
            id = l[0]
            cla = l[len(l) - 1].strip()
            token = l[len(l) - 2]
            if cla == category:
                lis.append((id, token))
    return lis

    # print get_data('2')


# 记录某类别聚簇的数据
def record_clusters(lis, category):
    dic = {'1': 'bug', '2': 'feature'}
    with open(const.CLUSTER_PATH + dic[category] + '.txt', 'w+') as fw:
        for cluster in lis:
            line = ''
            for c in cluster:
                line += str(c) + ' '
            fw.write(line.strip() + '\n')


# 获取某类别聚簇的完整数据
def get_category_all_cluster_data(category):
    dic = {'1': 'bug', '2': 'feature'}
    path = const.CLUSTER_PATH + dic[category] + '.txt'

    lis = []
    with open(path, 'r') as f:
        for line in f:
            c = []
            l = line.split(' ')
            for id in l:
                id = id.strip()
                # 根据id 获取数据
                (author, time, review, rate) = get_data_by_id(id)
                c.append((author, time, review, rate))
            lis.append(c)
    return lis


# 根据id获取数据
def get_data_by_id(id):
    with open(const.RAW_REVIEW_PATH, 'r') as f:
        for line in f:
            l = line.split(',')
            d = l[0]
            if d == id:
                author = l[1]
                time = l[4]
                rate = l[len(l) - 1].strip()
                j = 5
                review = ''
                while j < len(l) - 1:
                    if j == len(l) - 2:
                        review += l[j]
                    else:
                        review += l[j] + ','
                    j += 1
                # print s
                break

    return author, time, review, rate


# aa = get_category_all_custer_data('1')
# for c in aa:
#     print c

# 加载指定数量数据
def load_specified_quantity_data(quantity):
    begin = 1300
    lis = []
    with open(const.RAW_REVIEW_PATH, 'r') as f:
        # i = 0
        for line in f.readlines()[begin:begin + quantity]:
            # if i >= 1000 and i < (1000 + quantity):
            l = line.split(',')
            j = 5
            s = ''
            while j < len(l) - 1:
                if j == len(l) - 2:
                    s += l[j]
                else:
                    s += l[j] + ','
                j += 1
            id, review = l[0], s
            lis.append([id, review])
    return lis


# 存储数据
def save_data(data):
    # 保留原评论
    save_data_to_retain_raw(data)
    # 不保留原评论
    save_data_to_without_raw(data)


# 保留原评论
def save_data_to_retain_raw(data):
    with open(const.FIRST_PROCESS_REVIEW_PATH, 'a+') as f:
        for d in data:
            f.write(d[0] + ',' + d[1] + ',' + d[2] + ',' + d[3] + '\n')


# 不保留原评论
def save_data_to_without_raw(data):
    with open(const.PREPROCESS_REVIEW_PATH, 'a+') as f:
        for d in data:
            f.write(d[0] + ',' + d[2] + ',' + d[3] + '\n')


def test():
    lis = []
    with open(const.PREPROCESS_REVIEW_PATH, 'r') as f:
        for line in f.readlines()[1300:1400]:
            l = line.split(',')
            lis.append(l[len(l) - 1].strip())
    return lis

# print test()
# with open('/Users/dongyibo/PycharmProjects/nlp/file/tmp2.csv', 'r') as fr:
    #     fw = open('/Users/dongyibo/PycharmProjects/nlp/file/tmp.csv', 'w+')
    #     count = 1
    #     for line in fr:
    #         l = line.strip()
    #         a = 'UPDATE nlp.raw_review SET category = ' + l + ' WHERE id = ' + str(count)+';'
    #         fw.write(a + '\n')
    #         # i += 1
    #         count += 1
    #         # if i == 1000:  # 100行
    #         #     break
    #     # print count
    #     fw.close()