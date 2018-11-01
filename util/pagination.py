# -- coding: utf-8 --

'''
分页管理
'''


class Pagination(object):
    def __init__(self):
        self.slice = 4
        # 每页显示100条
        self.limit = 100

    def set_property(self, data, page=1):
        self.__data = data
        self.__page = page

    # 得到总页数
    def get_total_pages(self):
        size = len(self.__data)
        threshold = size / self.slice
        if size > threshold * self.slice:
            threshold += 1
        return threshold

    # 获取某页的数据
    def get_page_of_data(self):
        threshold = self.get_total_pages()
        # 不是最后一页
        if self.__page < threshold:
            result = self.__data[(self.__page - 1) * self.slice:self.__page * self.slice]
        else:
            result = self.__data[(self.__page - 1) * self.slice:]

        return result

    # 得到总页数第二版
    def get_total_pages2(self):
        count = self.__get_total_num()
        threshold = count / self.limit
        if count > threshold * self.limit:
            threshold += 1
        return threshold

    # 获取某页的数据第二版
    def get_page_of_data2(self):
        flag = False
        datas = []
        lower = (self.__page - 1) * self.limit
        # 不是最后一页
        if self.__page < self.get_total_pages2():
            upper = lower + self.limit
        else:
            upper = self.__get_total_num()

        count = 0
        for d in self.__data:
            l = []
            for i in d[1]:
                if lower <= count < upper:
                    l.append(i)
                elif count == upper:
                    flag = True
                    break
                count += 1
            if flag:
                datas.append([d[0], l])
                break
            if l:
                datas.append([d[0], l])
        return datas
        # data = main.prioritize_data(2)

    # 得到数据总个数
    def __get_total_num(self):
        count = 0
        for d in self.__data:
            for i in d[1]:
                count += 1
        return count

        # print data


# p = Pagination()
# p.set_property([[1, [1, 2]], [2, [3, 4]], [3, [5, 6, 7]]], 1)
# print p.get_total_pages2()
# print p.get_page_of_data2()
