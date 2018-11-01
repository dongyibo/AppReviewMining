# -- coding: utf-8 --
from util import const

'''
簇与文件的接口
'''


class ClusterHelper(object):
    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(ClusterHelper, cls).__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        # self.lock = threading.Lock()
        pass

    # 记录某类别聚簇的数据（弃用）
    def record_clusters(self, lis, category):
        dic = {1: 'bug', 2: 'feature'}
        with open(const.CLUSTER_PATH + dic[category] + '.txt', 'w+') as fw:
            for cluster in lis:
                line = ''
                for c in cluster:
                    line += str(c) + ' '
                fw.write(line.strip() + '\n')

    # 记录某类别聚簇的数据根据appId
    def record_clusters_appId(self, lis, category, appId):
        dic = {1: 'bug', 2: 'feature'}
        with open(const.CLUSTER_PATH + dic[category] + '_' + str(appId) + '.txt', 'w+') as fw:
            for cluster in lis:
                line = ''
                for c in cluster:
                    line += str(c) + ' '
                fw.write(line.strip() + '\n')

    # 记录某类别内部排序聚簇的数据根据appId
    def record_clusters_appId_prioritize(self, lis, category, appId):
        dic = {1: 'bug', 2: 'feature'}
        with open(const.CLUSTER_PATH + dic[category] + '_' + str(appId) + '_p.txt', 'w+') as fw:
            for cluster in lis:
                line = ''
                for c in cluster:
                    line += str(c) + ' '
                fw.write(line.strip() + '\n')

    # 得到某类别和appId的聚簇的数据
    def get_clusters_appId(self, category, appId):
        dic = {1: 'bug', 2: 'feature'}
        lis = []
        with open(const.CLUSTER_PATH + dic[category] + '_' + str(appId) + '.txt', 'r') as fr:
            for line in fr:
                l = []
                token = line.split(' ')
                for id in token:
                    l.append(int(id))
                lis.append(l)
        return lis

    # 获取某类别聚簇的完整数据
    def get_category_all_custer_data(self, category, appId):
        dic = {1: 'bug', 2: 'feature'}
        path = const.CLUSTER_PATH + dic[category] + '_' + str(appId) + '_p.txt'

        lis = []
        with open(path, 'r') as f:
            for line in f:
                c = []
                l = line.split(' ')
                if '0' == l[len(l) - 1].strip():
                    continue
                for id in l:
                    id = id.strip()
                    c.append(id)
                lis.append(c)
        return lis

    # 获取某类别废弃聚簇的完整数据
    def get_category_all_custer_data_aborted(self, category, appId):
        dic = {1: 'bug', 2: 'feature'}
        path = const.CLUSTER_PATH + dic[category] + '_' + str(appId) + '_p.txt'

        lis = []
        with open(path, 'r') as f:
            for line in f:
                c = []
                l = line.split(' ')
                if '0' == l[len(l) - 1].strip():
                    l = l[0:len(l) - 1]
                    for id in l:
                        id = id.strip()
                        c.append(id)
                    lis.append(c)
                else:
                    continue
        return lis

    # 软删除app含有id的簇,标记0
    def abort(self, id, category, appId):
        # self.lock.acquire()  # 加锁，锁住相应的资源
        dic = {1: 'bug', 2: 'feature'}
        path = const.CLUSTER_PATH + dic[category] + '_' + str(appId) + '_p.txt'

        with open(path, 'r') as fr:
            lines = fr.readlines()
        with open(path, 'w+') as fw:
            for line in lines:
                l = line.split(' ')
                # l[len(l) - 1] = (l[len(l) - 1]).strip()
                if id == l[0].strip():
                    line = line.strip() + ' 0\n'
                fw.write(line)
                # self.lock.release()  # 解锁，离开该资源

    # 恢复app含有id的簇
    def recover(self, id, category, appId):
        # self.lock.acquire()  # 加锁，锁住相应的资源
        dic = {5: 'bug', 6: 'feature'}
        path = const.CLUSTER_PATH + dic[category] + '_' + str(appId) + '_p.txt'

        with open(path, 'r') as fr:
            lines = fr.readlines()
        with open(path, 'w+') as fw:
            for line in lines:
                l = line.split(' ')
                # l[len(l) - 1] = (l[len(l) - 1]).strip()
                if id == l[0].strip():
                    line = line[0:len(line) - 3] + '\n'
                fw.write(line)
                # self.lock.release()  # 解锁，离开该资源

# c = ClusterHelper()
# d = ClusterHelper()
# print c,d
# print c.get_clusters_appId(1,481)
