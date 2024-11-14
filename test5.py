import json
from typing import List

def quick_sort(val_list):
    """
    1.快拍
    """
    if len(val_list) < 2:
        return val_list
    key = val_list[0]

    small_key = [val for val in val_list[1:] if val <= key]
    big_key = [val for val in val_list[1:] if val > key]

    return quick_sort(small_key) + [key] + quick_sort(big_key)







def partition(arr, low, high):
    """
    1.这是排序的地方
    """
    # 选择最右边的元素作为基准点
    pivot = arr[high]
    # i 是较小元素的索引
    i = low - 1       # i = -1
    for j in range(low, high):
        # 如果当前元素小于或等于基准点
        if arr[j] <= pivot:
            # 增加较小元素的索引
            i = i + 1
            # 交换 arr[i] 和 arr[j]
            arr[i], arr[j] = arr[j], arr[i]
            # 交换 arr[i + 1] 和 arr[high] (或基准点)
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort_inplace(arr:List, low:int, high:int):
    """
    1.这是分治的地方
    """
    # 如果低索引小于高索引，则继续排序
    if low < high:
        # pi 是分区索引，arr[pi] 已经在正确的位置
        pi = partition(arr, low, high)     # arr,0,6
        # 分别对左右子数组进行排序
        quicksort_inplace(arr, low, pi - 1)
        quicksort_inplace(arr, pi + 1, high)



if __name__ == "__main__":
    sample_array = [3, 6, 8, 10, 1, 2, 4]
    print("未排序数组:", sample_array)
    quicksort_inplace(sample_array, 0, len(sample_array) - 1)
    print("已排序数组:", sample_array)


