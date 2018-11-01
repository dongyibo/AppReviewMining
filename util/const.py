# -- coding: utf-8 --
import os

'''
定义一些常量
'''
BASE_DIR = os.path.dirname(__file__)[:len(os.path.dirname(__file__)) - 5] + '/file'

BUG = '1'
FEATURE = '2'
OTHER = '3'
USELESS = '4'

STOPWORDS_LIST_PATH = os.path.join(BASE_DIR, 'stop_words.txt')
FIRST_PROCESS_REVIEW_PATH = os.path.join(BASE_DIR, 'preprocessReview2.csv')
PREPROCESS_REVIEW_PATH = os.path.join(BASE_DIR, 'preprocessReview3.csv')
REVIEW_FOR_CLUSTER_PATH = os.path.join(BASE_DIR, 'preprocessReview4.csv')
TEST_PATH = os.path.join(BASE_DIR, 'tmp.csv')

CLUSTER_PATH = os.path.join(BASE_DIR, 'cluster_')

RAW_REVIEW_PATH = os.path.join(BASE_DIR, 'businessReview.csv')
MARKED_REVIEW_PATH = os.path.join(BASE_DIR, 'businessReviewMarked.csv')
