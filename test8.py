# def singleton(cls):
#     instances = {}
#
#     def get_instance(*args, **kwargs):
#         if cls not in instances:
#             instances[cls] = cls(*args, **kwargs)
#         return instances[cls]
#
#     return get_instance
#
#
# @singleton
# class Singleton:
#     def __init__(self, value=None):
#         self.value = value
#
#     # 测试
def singleton(cls):
    instances = {}

    def get_instance(*args,**kwargs):
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]

    return get_instance

@singleton
class Singleton:
    def __init__(self, value=None):
        self.value = value






s1 = Singleton('first')
s2 = Singleton('second')

print(s1.value)  # 输出: first
print(s2.value)  # 输出: first（因为s1和s2是同一个实例）
print(s1 is s2)  # 输出: True





