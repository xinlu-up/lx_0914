import sys

def get_max_sub(s:str)->int:
    length = len(s)

    max_len = 1
    for i in range(length):
        left = i
        right = i

        while left - 1 > -1 and right + 1 < length:
            while right + 1  < length and s[right + 1] == s[left]:
                right += 1
            if right + 1 < length and s[left-1] == s[right + 1]:
                right += 1
                left -= 1
            else:
                break
        if right - left + 1 > max_len:
            max_len = right - left + 1
    return max_len


def get_pop_sub(s:str):
    """
    1. 获取出栈的顺序
    """

if __name__ == "__main__":
    s = 'AB521112'
    res = get_max_sub(s)
    print(res)