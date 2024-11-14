import ast
with open('1.txt', 'r') as hil1:  # 从这过一遍名称和功能的代码
    for line in hil1:
        if '[' not in line or not line:
            continue
        vals = ast.literal_eval(line)  # [id,task_id]
        print(vals)
        print(vals[1])
        print(type(vals[1]))
        res = vals[1].split(',')
        print(res)