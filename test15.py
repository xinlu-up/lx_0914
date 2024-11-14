def count_even_length_xor_subarrays(a, x):
    n = len(a)
    prefix_xor = [0] * (n + 1)
    count = 0
    xor_map = {}

    # 初始化前缀异或和数组
    for i in range(1, n + 1):
        prefix_xor[i] = prefix_xor[i - 1] ^ a[i - 1]

        # 遍历前缀异或和数组，查找满足条件的区间
    for i in range(n + 1):
        target = prefix_xor[i] ^ x
        if target in xor_map:
            # 由于我们需要偶数长度的区间，因此我们需要检查索引的奇偶性
            # 如果 i 和 xor_map[target] 中的索引具有相同的奇偶性，则它们之间的区间长度为偶数
            for idx in xor_map[target]:
                if (i - idx) % 2 == 0:
                    count += 1

                    # 将当前前缀异或和及其索引添加到哈希表中
        # 注意：我们存储的是索引列表，以便处理多个相同前缀异或和的情况
        if prefix_xor[i] not in xor_map:
            xor_map[prefix_xor[i]] = []
        xor_map[prefix_xor[i]].append(i)

    return count


# 测试输入
a = [1, 2, 3, 2, 1]
x = 2
print(count_even_length_xor_subarrays(a, x))  # 输出: 2