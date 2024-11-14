# 1.
# 编写一个函数来查找字符串数组中的最长公共前缀。
# 示例 1：
# 输入：strs = ["flower","flow","flight"]
# 输出："fl"
# 示例 2：
# 输入：strs = ["dog","racecar","car"]
# 输出：""
# 解释：输入不存在公共前缀。不存在公共前缀，返回空字符串 ""。
# 2.
# 输入两个整数n和m，输出一个n行m列的矩阵，将数字 1 到 n*m 按照回字蛇形填充至矩阵中。
# 数据范围
# 1≤n,m≤100
# 示例
# 输入 3 3
# 输出
# 1 2 3
# 8 9 4
# 7 6 5
import time
from typing import List


def get_max_length(strs:List):
    """
    1. 获得最长公共前缀
    2. done
    """
    min_length = 1000
    for str in strs:
        if len(str) < min_length:
            min_length = len(str)    # 4

    # print(min_length)

    res = ""
    for i in range(min_length):  # 0,1,2,3
        val_list = []
        for str in strs:
            val_list.append(str[i])
            # print(val_list)
        if len(set(val_list)) > 1:
            return res
        else:
            res += val_list[0]
            # print(res)

    return res


def get_martix(n:int,m:int):
    """
    1. 根据输入的n,m返回蛇形矩阵
    """

    src_martix = [[0 for _ in range(m)] for _ in range(n)]

    is_martix = [[False for _ in range(m)] for _ in range(n)]
    print(src_martix)
    print(is_martix)

    src_key = 1
    i = 0
    j = 0
    src_martix[i][j] = src_key
    is_martix[i][j] = True
    while src_key < n*m :        # < 10
        # 根据右下左上进行遍历
        if j+1 < m and not is_martix[i][j+1]:
            src_key += 1
            src_martix[i][j+1] = src_key
            is_martix[i][j + 1] = True
            j = j+1
            continue
        if i + 1 < n and not is_martix[i+1][j]:
            src_key += 1
            src_martix[i+1][j] = src_key
            is_martix[i+1][j] = True
            i = i+1
            continue
        if j -1 >-1 and not is_martix[i][j-1]:
            src_key += 1
            src_martix[i][j-1] = src_key
            is_martix[i][j-1] = True
            j = j -1
            continue
        if i -1 > -1 and not is_martix[i-1][j]:
            src_key += 1
            src_martix[i-1][j] = src_key
            is_martix[i-1][j] = True
            i = i -1
            continue
        print(src_key)


    # print(src_martix)
    return src_martix


def cost_time(src):
    def wapper(*args,**kwargs):      # 不定长参数，不定长关键词参数（下去看一下）
        print(type(args))
        print(type(kwargs))
        now_time = time.time()
        src()
        end_time = time.time()
        print(end_time - now_time)
        return (end_time - now_time)/1000000
    return wapper


@cost_time
def print_hello():
    for i in range(100):
        print("hello")




# 实现一个生成器函数不断产生2的倍数
# 进程：计算密集型
# 线程：I/O密集型  gil锁
# 协程：I/O密集型

def get_val():
    """

    """
    # """
    # 1.实现一个生成器函数不断产生2的倍数
    # """

    # i = 1
    # num = i * 2
    # print(num)
    # yield num
    print_hello()


def generator(val):
    """
    1. 实现一个生成器函数不断产生2的倍数
    """
    yield val * 2




class Sigleton:
    def __init__(self,p):
        self.p = None

    def create(self):
        if self.p == None:
            self.p = Sigleton()



if __name__ == "__main__":
    # for i in range(5):
    #     get_val()

    for i in range(10):
        for val in generator(i):
            print(val)

