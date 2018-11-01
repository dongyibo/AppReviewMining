# -- coding: utf-8 --
import nltk
import warnings
import enchant
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from textblob import Word
from nltk.stem import WordNetLemmatizer

'''
原始英文文本预处理
'''


class Preprocess(object):
    def __init__(self):
        self.__sentence = ''
        self.__tokens = ''

    # 预处理
    def preprocess(self, isSynonymous=True):
        # 忽略警告
        warnings.filterwarnings('ignore')
        try:
            return self.__preprocess_detail(isSynonymous)
        except UnicodeDecodeError:
            print '!!!!!'
            return ''

    # set sentence
    def set_sentence(self, sentence):
        self.__sentence = sentence

    # 预处理细节
    def __preprocess_detail(self, isSynonymous):
        # 转化为小写
        sentence = self.__sentence.lower()
        sentences = sentence.split(".")
        sentence = ""
        for single in sentences:
            sentence += single + " "
        # print sentence
        # 分词
        self.__tokens = nltk.word_tokenize(sentence)
        # print '分词', tokens
        # 去标点以及中文,但中文效率太低，选择摒弃
        self.__remove_punctuation()
        # 去停词以及过短单词
        self.__remove_stopwords_and_shortwords()
        # 拼写检查
        self.__word_check_pyEnchant()
        # 转换时态
        self.__convert_tense_porter()
        # 特别词义处理
        if isSynonymous:
            self.__handle_specialwords()
        # 二次清洗，去除停词和过短词
        self.__remove_stopwords_and_shortwords()
        # 导出结果
        result = ''
        i = 0
        while i < len(self.__tokens):
            if i == len(self.__tokens) - 1:
                result += self.__tokens[i]
            else:
                result += self.__tokens[i] + ' '
            i += 1
        return result

    # 去标点
    def __remove_punctuation(self):
        english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!',
                                '*', '@', '#', '$', '%', "'", '``']
        i = 0
        while i < len(self.__tokens):
            # flag = contain_zh(tokens[i])
            if self.__tokens[i] in english_punctuations or "'" in self.__tokens[i]:
                self.__tokens.pop(i)
                i -= 1
            i += 1
            # print '去标点和中文', tokens

    # 去停词以及过短单词
    def __remove_stopwords_and_shortwords(self):
        english_stopwords = stopwords.words('english')
        # english_stopwords = file.get_stop_words_list()
        i = 0
        while i < len(self.__tokens):
            if self.__tokens[i] in english_stopwords or len(self.__tokens[i]) < 3:
                self.__tokens.pop(i)
                i -= 1
            i += 1
            # print '去停词以及单个字符', tokens  # 拼写检查

    # 拼写检查，PyEnchant方法
    def __word_check_pyEnchant(self):
        d = enchant.Dict("en_US")
        i = 0
        while i < len(self.__tokens):
            if not d.check(self.__tokens[i]):
                self.__tokens.pop(i)
                i -= 1
            i += 1

    # 拼写检查，textblob方法
    def __word_check_textblob(self):
        i = 0
        while i < len(self.__tokens):
            spell = self.__word_check_detail(self.__tokens[i])
            if spell == '':
                self.__tokens.pop(i)
                i -= 1
            else:
                self.__tokens[i] = spell
            i += 1
            # print '拼写检查', tokens

    # 拼写检查细节
    def __word_check_detail(self, word):
        w = Word(word)
        lis = w.spellcheck()
        # 无形似词
        if lis[0][1] == 0:
            return ''
        return lis[0][0]

    # 转换时态，波特分词法
    def __convert_tense_porter(self):
        porter_stemmer = PorterStemmer()
        for i in range(len(self.__tokens)):
            tmp = porter_stemmer.stem(self.__tokens[i])
            self.__tokens[i] = tmp.encode('ascii')
            # print porter_stemmer.stem("'s")
            # print '转换时态', tokens

    # 转换时态，wordnet
    def __convert_tense_wordnet(self):
        lemmatizer = WordNetLemmatizer()
        for i in range(len(self.__tokens)):
            self.__tokens[i] = lemmatizer.lemmatize(self.__tokens[i])

    # 特殊词汇处理
    def __handle_specialwords(self):
        bug_list = ['freez', 'crash', 'bug', 'error', 'fail', 'glitch', 'problem', 'pester']
        feature_list = ['add', 'miss', 'lack', 'wish', 'hope', 'expect']
        for i in range(len(self.__tokens)):
            if self.__tokens[i] in bug_list:
                self.__tokens[i] = 'bug'
            elif self.__tokens[i] in feature_list:
                self.__tokens[i] = 'feature'

    # print 'dsdsdsa',Word('having').spellcheck()

    # 判断传入字符串是否包含中文
    def __contain_zh(self, word):
        for ch in word.decode('utf-8'):
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    # b = TextBlob("I havv goood speling!")
    # print(b.correct())
    # w = Word('freez')
    # print w.spellcheck()
    # print PorterStemmer().stem('freeze')


    # 返回一个单词的同义词列表
    def __word_synonyms(self, word):
        synonyms = []
        list_good = wordnet.synsets(word)
        for syn in list_good:
            for l in syn.lemmas():
                synonyms.append(l.name())
        return (set(synonyms))

    # 返回同义词列表中最短且字典序最大的单词
    def __word_synonyms_suit(self, word):
        sets = self.__word_synonyms(word)
        tmp = sorted(sets, lambda a, b: len(a) - len(b))
        # 没有近义词，返回本身
        if len(tmp) == 0:
            return word
        length = len(tmp[0])
        list = []
        for word in tmp:
            if len(word) == length:
                list.append(word)
            else:
                break
        return sorted(list)[0]


# # 转换时态，波特
# def convert_tense_porter(token):
#     time_start = time.time()
#     tokens = token.split(' ')
#     porter_stemmer = PorterStemmer()
#     for i in range(len(tokens)):
#         tmp = porter_stemmer.stem(tokens[i])
#         s = tmp.encode('ascii')
#     time_end = time.time()
#     return time_end - time_start
#
#
# # 转换时态，wordnet
# def convert_tense_wordnet(token):
#     time_start = time.time()
#     tokens = token.split(' ')
#     lemmatizer = WordNetLemmatizer()
#     for i in range(len(tokens)):
#         s = lemmatizer.lemmatize(tokens[i])
#     time_end = time.time()
#     return time_end - time_start
#
#
# sentence = 'Fantastic. I never really knew how much bloatware and unneeded processes ' \
#            'were on the phone until this app. Samsung Galaxy S6 Edge Plus and I shut over ' \
#            'a hundred and fifty things down LOL with no loss of function to the phone period ' \
#            'thank you very much for this excellent app. I love that you can Google search each entry' \
#            ' so you at least have a basic idea of what it is and what it does for non-tech guys like me. '
#
# times = 1000
# sum1, sum2 = 0, 0
# for i in range(times):
#     sum2 += convert_tense_wordnet(sentence)
#     sum1 += convert_tense_porter(sentence)
# print 'porter:',sum1 / times, ' wordnet:',sum2 / times