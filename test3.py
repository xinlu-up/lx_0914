from typing import List

def findContentChildren(g: List[int], s: List[int]) -> int:

    g_length = len(g)
    s_length = len(s)

    g.sort()
    s.sort()

    s_index = 0
    for i in range(g_length):
        if s[s_index] - g[i] < s[s_index + 1]:
            pass


    return 0


if __name__ == "__main__":
    g = [1, 2]        # g表示胃口值
    s = [1, 2, 3]      # 表示饼干的的大小
    res = findContentChildren(g,s)
    print(res)
