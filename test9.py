# python的单例模式

#
# def singleton(cls):
#     instances = {}
#
#     def get_instance(*args,**kwargs):
#         if cls not in instances:
#             instances[cls] = cls(*args,**kwargs)
#         return instances[cls]
#     return get_instance
#
# @singleton
# class Singleton:
#     def __init__(self,value = None):
#         self.value = value
#
#
# s1 = Singleton('first')
# s2 = Singleton('second')
# print(s2.value)
# print(s1 == s2)


# 下面是一个使用装饰器来实现单例模式的例子
def singleton(cls):  # 这是一个装饰器函数，接受一个cls的类参数
    instances = {}

    def get_instance(*args,**kwargs):
        if cls not in instances:                # 假如没有实例，则创建一个新的。
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]                   # 假如有，就直接返回这个实例
    return get_instance


@singleton
class Singleton:                # 这个地方可以进行创建对象
    def __init__(self,value):
        self.value = None


s1 =Singleton('first')
s2 = Singleton('second')
print(s1 == s2)
