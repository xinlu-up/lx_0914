def find_ip_addresses(s):
    def is_valid_ip_segment(segment):     # 判断字符是否为合法？
        try:
            num = int(segment)
            return 0 <= num <= 255
        except ValueError:
            return False

    n = len(s)
    # 我们需要找到四个部分，所以我们需要三个分割点
    # 分割点索引的范围是 [0, n-4] 因为最后一个部分不需要分割点
    for i1 in range(1, n - 3):  # 第一个分割点                             # i1 = 1
        for i2 in range(i1 + 1, n - 2):  # 第二个分割点（必须在第一个之后）    # i2 = 2
            for i3 in range(i2 + 1, n - 1):  # 第三个分割点（必须在第二个之后） # i3= 3
                # 分割成四个部分
                part1 = s[:i1]
                part2 = s[i1:i2]
                part3 = s[i2:i3]
                part4 = s[i3:]
                # print(part1,part2,part3,part4)
                # 检查所有部分是否都是有效的 IP 段
                if is_valid_ip_segment(part1) and is_valid_ip_segment(part2) and is_valid_ip_segment(
                        part3) and is_valid_ip_segment(part4):
                    # 找到一个有效的 IP 地址
                    ip_address = '.'.join([part1, part2, part3, part4])
                    print(ip_address)

                # 给定的字符串


def find_ip_addresses2(s):
    def backtrack(start, segments, path):
        # Base case: If we have found 4 segments and used all characters
        if len(segments) == 4 and start == len(s):
            # Join segments with dots to form an IP address
            # Only print if all segments are valid without leading zeros (unless they are 0)
            if all(str(seg) == '0' or not str(seg).startswith('0') for seg in segments):
                ip_address = '.'.join(map(str, segments))
                print(ip_address)
            return

            # Explore possible segments
        for i in range(1, 4 + 1):  # +1 because we might take up to 3 digits
            # If we exceed the string length or the number exceeds 255, stop
            if start + i > len(s) or int(s[start:start + i]) > 255:
                break

                # Recursively explore with the current segment
            # Do not use zfill here, as it would add leading zeros unnecessarily
            segment = int(s[start:start + i])
            # Convert segment back to string only for validation purposes later
            segment_str = str(segment) if segment != 0 else '0'
            backtrack(start + i, segments + [segment], path + [segment_str])

            # Start backtracking from the beginning of the string

    backtrack(0, [], [])


if __name__ == "__main__":
    # 给定的字符串
    s = '000256'
    # 查找并打印所有可能的 IP 地址
    find_ip_addresses2(s)


