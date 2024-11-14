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
    # 方法肯定是回溯
    length = len(s)


    return 0

def generate_pop_sequences(sequence):
    def backtrack(stack, index, result):
        if index == len(sequence) and not stack:
            results.append(''.join(result))
            return

        if index < len(sequence):
            # 进栈操作
            stack.append(sequence[index])
            result.append('')  # Placeholder for future pop operation
            backtrack(stack, index + 1, result)
            # 回溯
            result.pop()
            stack.pop()

        if stack:
            # 出栈操作
            result.append(stack.pop())
            backtrack(stack, index, result)
            # 回溯
            stack.append(result.pop())

    results = []
    backtrack([], 0, [])
    return results



if __name__ == "__main__":
    # s = 'AB521112'
    # res = get_max_sub(s)
    # print(res)

    # s = 'qwe'
    # res = generate_pop_sequences(s)
    # print(res)

    my_dict = {1:'q',2:'w',3:'e'}
    if 4 not in my_dict.keys():
        print("no")
    if 1 in my_dict.keys():
        print("yes")
    print(my_dict.keys())
