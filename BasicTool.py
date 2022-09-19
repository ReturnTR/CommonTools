# 基本的工具
# 包含内置类型的一些常用操作
# 该文件要求不能导入任何的包
# 如果是对特定类型进行操作，格式为（操作_类型）

def sort_dict(source_dict,use_key=False,reverse=True):
    """
    对字典排序，可按值或按键
    :param source_dict:原字典
    :param ues_key:使用字典的键作为排序的键
    :param reverse: True默认从大到小
    :return:排序后的字典
    """
    if use_key:
        return {k: v for k, v in sorted(source_dict.items(), key=lambda item: item[0], reverse=reverse)}
    else:
        return {k: v for k, v in sorted(source_dict.items(), key=lambda item: item[1], reverse=reverse)}

def count_list(l,reverse=True):
    """
    将列表出现的相同字符进行计数
    :param l:列表
    :return:字典{值:出现次数}
    """
    res=dict()
    for i in l:res[i]=res.setdefault(i,0)+1
    sort_dict(res,reverse=reverse)
    return res

def avg_list(l):
    """list平均值"""
    return sum(l)/len(l)

def percentage(num):
    """将小数转化成百分比格式,保留两位小数"""
    return str(int(num*10000)/100)+"%"

def cut_data(data,rate="default"):
    """
    切分列表（数据集常用）
    :param data:列表
    :param rate:切分比率，默认8:1:1 (不是严格的比率，会有整数问题)
    :param dev:是否需要dev
    :return:
    """
    if rate=="default":rate=[0.8,0.1,0.1]
    elif sum(rate)!=1: raise Exception("概率和不等于1")
    amount=[int(len(data)*i) for i in rate]
    for i in range(1,len(amount)):
        amount[i]+=amount[i-1]
    amount[-1]=len(data)
    amount=[0]+amount
    cutted_data=tuple()
    for i in range(len(amount)-1):
        cutted_data+=(data[amount[i]:amount[i+1]],)

    return cutted_data

class DictCount():

    def __init__(self):
        self.infobox=dict()
    def add(self,item):

        if item in self.infobox:
            self.infobox[item]+=1
        else:
            self.infobox[item]=1
    def get(self):
        self.infobox=sort_dict(self.infobox)
        return self.infobox