import random

def g_int(start,end):
    return random.randint(start, end)

def generate_unique_list(start,end,count,order=True):
    """生成在一定范围内不重复的随机数字列表
    
    例：
        0, 5, 2
        [3, 5]
    """
    used_numbers = set()
    while len(used_numbers) < count:
        number = random.randint(start, end)
        if number not in used_numbers:
            used_numbers.add(number)
    used_numbers=list(used_numbers)
    if order:used_numbers.sort(reverse=False)
    return list(used_numbers)


